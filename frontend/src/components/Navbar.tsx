'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';
import { useRouter, usePathname } from 'next/navigation';

export default function Navbar() {
  const { isAuthenticated, user, logout } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  // Don't show navbar on login page
  if (pathname === '/login') {
    return null;
  }

  // Don't show navbar if not authenticated
  if (!isAuthenticated) {
    return null;
  }

  return (
    <nav className="bg-white shadow-lg border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between h-16">
          {/* Logo/Brand */}
          <div className="flex items-center">
            <h1 className="text-lg sm:text-xl font-bold text-blue-700">
              🌐 <span className="hidden sm:inline">NorteGestión</span>
            </h1>
          </div>

          {/* Navigation Links */}
          <div className="flex items-center space-x-1 sm:space-x-4">
            <Link
              href="/"
              className={`text-gray-600 hover:text-blue-700 hover:bg-blue-50 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                pathname === '/' ? 'text-blue-700 bg-blue-50' : ''
              }`}
            >
              🏠 <span className="hidden sm:inline">Inicio</span>
            </Link>
            <Link
              href="/products"
              className={`text-gray-600 hover:text-blue-700 hover:bg-blue-50 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                pathname === '/products' ? 'text-blue-700 bg-blue-50' : ''
              }`}
            >
              📦 <span className="hidden sm:inline">Productos</span>
            </Link>

            {/* User Info & Logout */}
            <div className="flex items-center space-x-2 ml-4 pl-4 border-l border-gray-200">
              <div className="hidden sm:block">
                <span className="text-sm text-gray-600">
                  Hola, {user?.first_name || user?.email?.split('@')[0] || user?.username}
                </span>
              </div>
              <button
                onClick={handleLogout}
                className="text-gray-600 hover:text-red-600 hover:bg-red-50 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
                title="Cerrar sesión"
              >
                🚪 <span className="hidden sm:inline">Salir</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}