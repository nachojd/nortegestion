import type { Metadata } from "next";
import "./globals.css";
import QueryProvider from "@/components/QueryProvider";
import { AuthProvider } from "@/context/AuthContext";
import Navbar from "@/components/Navbar";

export const metadata: Metadata = {
  title: "NorteGestión - Sistema Integral",
  description: "Sistema de gestión profesional e integral",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body className="bg-gray-50 font-sans antialiased min-h-screen">
        <AuthProvider>
          <Navbar />
          <QueryProvider>
            <main className="max-w-7xl mx-auto py-6 sm:py-8 px-4 transition-all duration-300">
              {children}
            </main>
          </QueryProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
