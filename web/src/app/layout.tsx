import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "OpsPilot",
  description: "智能运维助理",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body >{children}</body>
    </html>
  );
}
