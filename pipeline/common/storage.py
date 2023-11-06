import csv
import os
import tempfile
from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Any, Iterator, Optional

from django.conf import settings
from pyarrow import parquet as pq

from .logger import LoggerFactory

logger = LoggerFactory.get(__name__)


class FileSystemHelper(ABC):
    @abstractmethod
    def get_data_bucket_contents(self) -> Iterator[str]:
        """Pulls the contents from the data bucket defined in settings"""
        raise NotImplementedError

    @abstractmethod
    @contextmanager
    def get_file(self, filename: str, mode="rt"):
        raise NotImplementedError


class _LocalFileSystemHelper(FileSystemHelper):
    def get_data_bucket_contents(self) -> list[str]:
        return os.listdir(settings.DATA_DIR)

    @contextmanager
    def get_file(self, filename: str, mode="rt"):
        f = open(settings.DATA_DIR / filename, mode)
        try:
            yield f
        finally:
            f.close()


class _CloudFileSystemHelper(FileSystemHelper):
    def __init__(self):
        from google.cloud import storage

        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(settings.CLOUD_STORAGE_BUCKET)

    def get_data_bucket_contents(self) -> Iterator[str]:
        blobs: Iterator[str] = [
            item.name for item in self.storage_client.list_blobs(self.bucket)
        ]
        return blobs

    @contextmanager
    def get_file(self, filename: str, mode="rt"):
        # if it's a csv file, save it to a temp file and return it open
        tempdir = tempfile.gettempdir()
        if filename not in os.listdir(tempdir):
            blob = self.bucket.blob(filename)
            with open(f"{tempdir}/{filename}", "wb") as f:
                blob.download_to_file(f)

        f = open(f"{tempdir}/{filename}", mode)
        try:
            yield f
        finally:
            f.close()


class FileSystemHelperFactory:
    _fileSystemHelper: Optional[FileSystemHelper] = None

    @staticmethod
    def get() -> FileSystemHelper:
        if not FileSystemHelperFactory._fileSystemHelper:
            env = os.environ.get("ENV", "DEV")

            if env in ("DEV", "unittest"):
                FileSystemHelperFactory._fileSystemHelper = (
                    _LocalFileSystemHelper()
                )
                return FileSystemHelperFactory._fileSystemHelper
            elif env == "PROD":
                FileSystemHelperFactory._fileSystemHelper = (
                    _CloudFileSystemHelper()
                )
                return FileSystemHelperFactory._fileSystemHelper
            else:
                raise RuntimeError(
                    f"Unable to instantiate FileSystemHelper, invalid "
                    f"environment variable passed for 'ENV'. Value passed : {env} ."
                )

        return FileSystemHelperFactory._fileSystemHelper


class DataReader(ABC):
    def __init__(self):
        self.fileSystemHelper: FileSystemHelper = FileSystemHelperFactory.get()

    @abstractmethod
    def col_names(self, filename, delimiter="|") -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def iterate(self, filename, delimiter="|") -> Iterator[dict[str, Any]]:
        raise NotImplementedError

    def get_data_bucket_contents(self):
        return self.fileSystemHelper.get_data_bucket_contents()


class _CsvDataReader(DataReader):
    def col_names(self, filename, delimiter="|") -> list[str]:
        logger.info(f"Getting col names : {filename}")
        with self.fileSystemHelper.get_file(filename) as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            fieldnames = reader.fieldnames
            logger.info(f"Fields for {filename} : {fieldnames}")
            return fieldnames

    def iterate(self, filename, delimiter="|") -> Iterator[dict[str, Any]]:
        with self.fileSystemHelper.get_file(filename) as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            for row in reader:
                yield row


class _ParquetDataReader(DataReader):
    def col_names(self, filename, delimiter="|") -> list[str]:
        with self.fileSystemHelper.get_file(filename, mode="rb") as f:
            pf: pq.ParquetFile = pq.ParquetFile(f)
            try:
                return [c.name for c in pf.schema]
            finally:
                pf.close()

    def iterate(self, filename, delimiter="|") -> Iterator[dict[str, Any]]:
        with self.fileSystemHelper.get_file(filename, mode="rb") as f:
            pf = pq.ParquetFile(f)
            pf_iter = pf.iter_batches(settings.READ_CHUNK_SIZE)
            for batch in pf_iter:
                row_list = batch.to_pylist()
                for row in row_list:
                    yield row


class DataReaderFactory:
    csv_data_reader = _CsvDataReader()
    parquet_data_reader = _ParquetDataReader()

    @staticmethod
    def get(type: str) -> DataReader:
        if not type:
            raise TypeError(
                "A value of { csv, parquet, geoparquet } must be given to DataReaderFactory for type"
            )

        if type.lower() in ["parquet", "geoparquet"]:
            return DataReaderFactory.parquet_data_reader
        if type.lower() == "csv":
            return DataReaderFactory.csv_data_reader
        raise TypeError(
            f"A valid value must be given to DataReaderFactory. Value given : {type} ."
        )
