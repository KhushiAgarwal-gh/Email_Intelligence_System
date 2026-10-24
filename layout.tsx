import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Email Intelligence",
  description: "Classify, prioritize, and summarize email with a simple dashboard.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
