"use client";
import Image from "next/image";

export default function Header() {
  return (
    <div className="flex flex-row text-center">
      <div className="w-[200px]">
        <Image
          src="/images/climate-cabinet-logo.png"
          alt="Description"
          width={424} // width of the original image
          height={276} // height of the original image
        />
      </div>
      <div className="flex-1">
        <h1 className="text-2xl">Climate Cabinet's Good Site</h1>
      </div>
    </div>
  );
}
