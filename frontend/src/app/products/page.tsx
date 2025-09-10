'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';

interface Product {
  id: number;
  codigo: string;
  nombre: string;
  rubro_nombre: string;
  marca_nombre: string;
  precio_venta: string;
  precio_con_iva: string;
  stock_actual: string;
  activo: boolean;
}

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/products/');
      setProducts(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching products:', error);
      // Fallback data for demo
      setProducts([
        {
          id: 1,
          codigo: "2294",
          nombre: "CADENA OSAKA 520H X 118",
          rubro_nombre: "Cadenas",
          marca_nombre: "Osaka",
          precio_venta: "9735.81",
          precio_con_iva: "11780.33",
          stock_actual: "5.00",
          activo: true
        },
        {
          id: 2,
          codigo: "2313",
          nombre: "JAULA EMBRAGUE DAELIM 14X20X16",
          rubro_nombre: "Embragues", 
          marca_nombre: "Daelim",
          precio_venta: "1724.96",
          precio_con_iva: "2087.20",
          stock_actual: "3.00",
          activo: true
        }
      ]);
      setLoading(false);
    }
  };

  const filteredProducts = products.filter(product =>
    product.nombre.toLowerCase().includes(search.toLowerCase()) ||
    product.codigo.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) {
    return (
      <div className="flex flex-col justify-center items-center h-64 space-y-4">
        <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
        <div className="text-lg text-gray-600 font-medium">Cargando productos...</div>
      </div>
    );
  }

  return (
    <div>
      <div className="flex flex-col sm:flex-row justify-between items-center mb-6 gap-4">
        <h1 className="text-2xl sm:text-3xl font-bold text-blue-700">
          📦 Productos
        </h1>
        <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200 font-medium">
          + Agregar Producto
        </button>
      </div>

      <div className="mb-6">
        <input
          type="text"
          placeholder="🔍 Buscar productos..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-900 placeholder-gray-500"
        />
      </div>

      <div className="space-y-6">
        {filteredProducts.map((product) => (
          <div key={product.id} className="bg-white border-2 border-gray-300 rounded-xl p-6 hover:shadow-lg transition-shadow duration-200">
            <div className="flex flex-col lg:flex-row justify-between gap-6">
              <div className="flex-1">
                <div className="mb-4">
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">{product.nombre}</h3>
                  <div className="flex items-center gap-4 text-lg">
                    <span className="text-gray-700 font-medium">Código: <span className="font-bold text-blue-700">#{product.codigo}</span></span>
                  </div>
                </div>
                <div className="mb-4">
                  <p className="text-xl text-gray-700 font-medium">{product.rubro_nombre} • {product.marca_nombre}</p>
                </div>
                <div className="flex flex-wrap gap-4">
                  <div className="bg-green-50 border-2 border-green-200 rounded-lg px-4 py-3">
                    <span className="text-xl font-bold text-green-800">
                      Precio: ${parseFloat(product.precio_venta).toLocaleString('es-AR', { minimumFractionDigits: 2 })}
                    </span>
                  </div>
                </div>
              </div>
              <div className="flex flex-col gap-3">
                <a href={`/products/edit/${product.id}`} className="px-6 py-3 bg-blue-600 text-white text-lg font-medium rounded-lg hover:bg-blue-700 transition-colors duration-200 text-center">
                  ✏️ Editar
                </a>
                <button className="px-6 py-3 bg-red-600 text-white text-lg font-medium rounded-lg hover:bg-red-700 transition-colors duration-200">
                  🗑️ Eliminar
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredProducts.length === 0 && (
        <div className="text-center py-12 bg-white border-2 border-dashed border-gray-200 rounded-lg mt-8">
          <p className="text-lg font-medium text-gray-600">🔍 No se encontraron productos</p>
          <p className="text-gray-400 mt-2">Prueba con otros términos de búsqueda</p>
        </div>
      )}
    </div>
  );
}