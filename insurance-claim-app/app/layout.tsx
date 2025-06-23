import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "EIS Claim Form",
  description: "Interactive Claim Form for EIS",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
