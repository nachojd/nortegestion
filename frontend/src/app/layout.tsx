import type { Metadata } from "next";
import "./globals.css";
import QueryProvider from "@/components/QueryProvider";

export const metadata: Metadata = {
  title: "MotoCenter - Gestión de Presupuestos",
  description: "Sistema de gestión para MotoCenter",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body className="bg-gray-50 font-sans antialiased min-h-screen">
        <nav className="bg-white shadow-lg border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <h1 className="text-lg sm:text-xl font-bold text-blue-700">🏍️ <span className="hidden sm:inline">MotoCenter</span></h1>
              </div>
              <div className="flex items-center space-x-1 sm:space-x-4">
                <a href="/" className="text-gray-600 hover:text-blue-700 hover:bg-blue-50 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">🏠 <span className="hidden sm:inline">Inicio</span></a>
                <a href="/products" className="text-gray-600 hover:text-blue-700 hover:bg-blue-50 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">📦 <span className="hidden sm:inline">Productos</span></a>
              </div>
            </div>
          </div>
        </nav>
        <QueryProvider>
          <main className="max-w-7xl mx-auto py-6 sm:py-8 px-4 transition-all duration-300">
            {children}
          </main>
        </QueryProvider>
      </body>
    </html>
  );
}
