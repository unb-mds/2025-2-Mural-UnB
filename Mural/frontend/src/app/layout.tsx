import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Mural UnB",
  icons: {
    icon: "/vite.svg",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
