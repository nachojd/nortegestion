import type { Metadata } from "next";
<<<<<<< HEAD
import Link from "next/link";
import "./globals.css";
import QueryProvider from "@/components/QueryProvider";

export const metadata: Metadata = {
  title: "Norte Gestión - Sistema Integral de Gestión",
  description: "Sistema de gestión empresarial multi-sector",
=======
import "./globals.css";
import QueryProvider from "@/components/QueryProvider";
import { AuthProvider } from "@/context/AuthContext";
import Navbar from "@/components/Navbar";

export const metadata: Metadata = {
  title: "NorteGestión - Sistema Integral",
  description: "Sistema de gestión profesional e integral",
>>>>>>> main
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body className="bg-gray-50 font-sans antialiased min-h-screen">
<<<<<<< HEAD
        <nav className="bg-white shadow-lg border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <h1 className="text-lg sm:text-xl font-bold text-blue-700">🌐 <span className="hidden sm:inline">Norte Gestión</span></h1>
              </div>
              <div className="flex items-center space-x-1 sm:space-x-4">
                <Link href="/" className="text-gray-600 hover:text-blue-700 hover:bg-blue-50 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">🏠 <span className="hidden sm:inline">Inicio</span></Link>
                <Link href="/products" className="text-gray-600 hover:text-blue-700 hover:bg-blue-50 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">📦 <span className="hidden sm:inline">Productos</span></Link>
              </div>
            </div>
          </div>
        </nav>
        <QueryProvider>
          <main className="max-w-7xl mx-auto py-6 sm:py-8 px-4 transition-all duration-300">
            {children}
          </main>
        </QueryProvider>
=======
        <AuthProvider>
          <Navbar />
          <QueryProvider>
            <main className="max-w-7xl mx-auto py-6 sm:py-8 px-4 transition-all duration-300">
              {children}
            </main>
          </QueryProvider>
        </AuthProvider>
>>>>>>> main
      </body>
    </html>
  );
}
