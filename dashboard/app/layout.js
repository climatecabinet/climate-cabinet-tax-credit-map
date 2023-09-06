import "./globals.css";
import { Open_Sans } from "next/font/google";

export const metadata = {
  title: "Climate Cabinet - Inflation Reduction Act (IRA) Credits",
  description:
    "Interactive map showing tax credit areas from the Inflation Reduction Act",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/public/favicon.ico" />
      </head>
      <body>
        <div className="flex justify-center max-w-screen-xl  mx-auto">
          {children}
        </div>
      </body>
    </html>
  );
}
