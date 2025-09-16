<<<<<<< HEAD
export default function Home() {
  return (
    <div className="text-center py-20">
      <h1 className="text-4xl font-bold text-blue-700 mb-8">
        🌐 Norte Gestión
      </h1>
      <p className="text-2xl text-gray-600 mb-12">
        Sistema integral de gestión empresarial
      </p>
      <a 
        href="/products" 
        className="inline-block bg-blue-600 text-white text-xl font-bold py-4 px-8 rounded-xl hover:bg-blue-700 transition-colors duration-200 shadow-lg hover:shadow-xl"
      >
        📦 Ver Productos
      </a>
    </div>
  );
}
=======
'use client';

import ProtectedRoute from '@/components/ProtectedRoute';
import { useAuth } from '@/context/AuthContext';

function HomeContent() {
  const { user } = useAuth();

  return (
    <div className="text-center py-20">
      <h1 className="text-4xl font-bold text-blue-700 mb-8">
        🌐 NorteGestión
      </h1>
      <p className="text-2xl text-gray-600 mb-4">
        Sistema de Gestión Profesional
      </p>
      <p className="text-lg text-gray-500 mb-12">
        Hola, <strong>{user?.first_name || user?.email?.split('@')[0] || user?.username}</strong>
      </p>

      <div className="flex justify-center max-w-2xl mx-auto">
        <a
          href="/products"
          className="block bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-200 border border-gray-200 hover:border-blue-300"
        >
          <div className="text-3xl mb-3">📦</div>
          <h3 className="text-xl font-bold text-gray-800 mb-2">Productos</h3>
          <p className="text-gray-600">Gestiona tu inventario</p>
        </a>

      </div>
    </div>
  );
}

export default function Home() {
  return (
    <ProtectedRoute>
      <HomeContent />
    </ProtectedRoute>
  );
}
>>>>>>> main
