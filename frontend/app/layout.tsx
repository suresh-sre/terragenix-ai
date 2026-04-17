import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
};

export const metadata: Metadata = {
  title: "GenOpsLab | Build Cloud Infrastructure, Become DevOps Job-Ready with AI",
  description: "Generate Terraform, optimize cloud costs, and build real-world DevOps projects. AI-powered platform for students, professionals, and startups.",
  keywords: "DevOps, Terraform, Cloud Infrastructure, AWS, AI, FinOps, Career Building",
  robots: "follow, index",
  openGraph: {
    type: "website",
    url: "https://genopslab.com",
    title: "GenOpsLab | Build Cloud Infrastructure with AI",
    description: "Generate Terraform, optimize cloud costs, and build real-world DevOps projects.",
    images: [
      {
        url: "https://genopslab.com/og-image.png",
        width: 1200,
        height: 630,
      },
    ],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
