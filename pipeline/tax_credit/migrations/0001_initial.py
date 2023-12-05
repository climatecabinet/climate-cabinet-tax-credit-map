# Generated by Django 4.2.5 on 2023-10-03 19:40

import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CensusBlockGroup",
            fields=[
                (
                    "id",
                    models.CharField(max_length=255, primary_key=True, serialize=False),
                ),
                ("centroid", django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ("population", models.IntegerField()),
            ],
            options={
                "db_table": "tax_credit_census_block_group",
            },
        ),
        migrations.CreateModel(
            name="CensusTract",
            fields=[
                (
                    "id",
                    models.CharField(max_length=255, primary_key=True, serialize=False),
                ),
                ("centroid", django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ("population", models.IntegerField()),
            ],
            options={
                "db_table": "tax_credit_census_tract",
            },
        ),
        migrations.CreateModel(
            name="GeographyType",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255, unique=True)),
            ],
            options={
                "db_table": "tax_credit_geography_type",
            },
        ),
        migrations.CreateModel(
            name="Program",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255, unique=True)),
                ("agency", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("base_benefit", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Geography",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                (
                    "boundary",
                    django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326),
                ),
                (
                    "simple_boundary",
                    django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326),
                ),
                ("as_of", models.DateField()),
                ("source", models.CharField(max_length=255)),
                ("fips_info", models.CharField(max_length=255, null=True)),
                (
                    "geography_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tax_credit.geographytype",
                    ),
                ),
            ],
            options={
                "db_table": "tax_credit_geography",
                "unique_together": {("name", "geography_type")},
            },
        ),
        migrations.CreateModel(
            name="TargetBonusAssoc",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("target_geography_type", models.CharField(max_length=255)),
                ("bonus_geography_type", models.CharField(max_length=255)),
                (
                    "bonus_geography",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bonus_geo_set",
                        to="tax_credit.geography",
                    ),
                ),
                (
                    "target_geography",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="target_geo_set",
                        to="tax_credit.geography",
                    ),
                ),
            ],
            options={
                "db_table": "tax_credit_target_bonus_assoc",
                "unique_together": {("target_geography", "bonus_geography")},
            },
        ),
        migrations.CreateModel(
            name="GeographyTypeProgram",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("amount_description", models.TextField()),
                (
                    "geography_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tax_credit.geographytype",
                    ),
                ),
                (
                    "program",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tax_credit.program",
                    ),
                ),
            ],
            options={
                "db_table": "tax_credit_geography_type_program",
                "unique_together": {("geography_type", "program")},
            },
        ),
    ]
