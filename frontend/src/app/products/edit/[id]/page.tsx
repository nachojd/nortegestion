'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { useRouter } from 'next/navigation';
import { useQueryClient } from '@tanstack/react-query';

interface Product {
  id: number;
  codigo: string;
  nombre: string;
  rubro_nombre: string;
  marca_nombre: string;
  precio_costo: string;
  precio_venta: string;
  precio_lista2: string;
  precio_lista3: string;
  stock_actual: number;
  stock_minimo: number;
  activo: boolean;
}

export default function EditProductPage({ params }: { params: { id: string } }) {
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const router = useRouter();
  const queryClient = useQueryClient();

  useEffect(() => {
    fetchProduct();
  }, []);

  const fetchProduct = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await axios.get(`${apiUrl}/api/products/${params.id}/`);
      setProduct(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching product:', error);
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!product) return;
    
    setSaving(true);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      await axios.patch(`${apiUrl}/api/products/${params.id}/`, {
        precio_costo: parseFloat(product.precio_costo) || 0,
        precio_venta: parseFloat(product.precio_venta) || 0,
        precio_lista2: parseFloat(product.precio_lista2) || 0,
        precio_lista3: parseFloat(product.precio_lista3) || 0,
        stock_actual: parseInt(product.stock_actual.toString()) || 0,
        stock_minimo: parseInt(product.stock_minimo.toString()) || 0,
      });
      
      // Invalidar cache de React Query para actualizar la lista
      queryClient.invalidateQueries({ queryKey: ['products'] });
      
      alert('¡Producto actualizado exitosamente!');
      router.push('/products');
    } catch (error) {
      console.error('Error updating product:', error);
      alert('Error al actualizar el producto');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col justify-center items-center h-64 space-y-4">
        <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
        <div className="text-xl text-gray-600 font-medium">Cargando producto...</div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="text-center py-16">
        <p className="text-xl text-red-600 font-medium">Producto no encontrado</p>
        <a href="/products" className="mt-4 inline-block bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors duration-200 font-medium">
          ← Volver a Productos
        </a>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-blue-700">Editar Producto</h1>
        <a href="/products" className="bg-gray-600 text-white px-6 py-3 rounded-lg hover:bg-gray-700 transition-colors duration-200 font-medium text-lg">
          ← Volver
        </a>
      </div>

      <div className="bg-white rounded-xl shadow-lg border-2 border-gray-200 p-8">
        {/* Info del producto */}
        <div className="mb-8 p-6 bg-gray-50 rounded-xl border-2 border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">{product.nombre}</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-lg">
            <p><span className="font-bold text-black">Código:</span> <span className="font-bold text-blue-700">#{product.codigo}</span></p>
            <p><span className="font-bold text-black">Rubro:</span> <span className="font-bold text-black">{product.rubro_nombre}</span></p>
            <p><span className="font-bold text-black">Marca:</span> <span className="font-bold text-black">{product.marca_nombre}</span></p>
          </div>
        </div>

        {/* Formulario de edición */}
        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Precios */}
          <div>
            <h3 className="text-2xl font-bold text-gray-900 mb-6">💰 Precios</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-2xl font-bold text-black mb-3">
                  Precio de Costo
                </label>
                <div className="relative">
                  <span className="absolute left-4 top-1/2 transform -translate-y-1/2 text-2xl font-black text-black">$</span>
                  <input
                    type="number"
                    step="0.01"
                    value={product.precio_costo}
                    onChange={(e) => setProduct({...product, precio_costo: e.target.value})}
                    onFocus={(e) => { const target = e.target as HTMLInputElement; target.select(); target.setSelectionRange(0, 0); }}
                    onClick={(e) => { const target = e.target as HTMLInputElement; target.setSelectionRange(0, 0); }}
                    className="w-full pl-12 pr-4 py-6 text-2xl font-bold text-black bg-white border-4 border-gray-600 rounded-lg focus:ring-4 focus:ring-blue-600 focus:border-blue-600"
                  />
                </div>
              </div>

              <div>
                <label className="block text-2xl font-bold text-black mb-3">
                  Precio de Venta
                </label>
                <div className="relative">
                  <span className="absolute left-4 top-1/2 transform -translate-y-1/2 text-2xl font-black text-black">$</span>
                  <input
                    type="number"
                    step="0.01"
                    value={product.precio_venta}
                    onChange={(e) => setProduct({...product, precio_venta: e.target.value})}
                    onFocus={(e) => { const target = e.target as HTMLInputElement; target.select(); target.setSelectionRange(0, 0); }}
                    onClick={(e) => { const target = e.target as HTMLInputElement; target.setSelectionRange(0, 0); }}
                    className="w-full pl-12 pr-4 py-6 text-2xl font-bold text-black bg-white border-4 border-gray-600 rounded-lg focus:ring-4 focus:ring-blue-600 focus:border-blue-600"
                  />
                </div>
              </div>

              <div>
                <label className="block text-2xl font-bold text-black mb-3">
                  Precio Lista 2
                </label>
                <div className="relative">
                  <span className="absolute left-4 top-1/2 transform -translate-y-1/2 text-2xl font-black text-black">$</span>
                  <input
                    type="number"
                    step="0.01"
                    value={product.precio_lista2}
                    onChange={(e) => setProduct({...product, precio_lista2: e.target.value})}
                    onFocus={(e) => { const target = e.target as HTMLInputElement; target.select(); target.setSelectionRange(0, 0); }}
                    onClick={(e) => { const target = e.target as HTMLInputElement; target.setSelectionRange(0, 0); }}
                    className="w-full pl-12 pr-4 py-6 text-2xl font-bold text-black bg-white border-4 border-gray-600 rounded-lg focus:ring-4 focus:ring-blue-600 focus:border-blue-600"
                  />
                </div>
              </div>

              <div>
                <label className="block text-2xl font-bold text-black mb-3">
                  Precio Lista 3
                </label>
                <div className="relative">
                  <span className="absolute left-4 top-1/2 transform -translate-y-1/2 text-2xl font-black text-black">$</span>
                  <input
                    type="number"
                    step="0.01"
                    value={product.precio_lista3}
                    onChange={(e) => setProduct({...product, precio_lista3: e.target.value})}
                    onFocus={(e) => { const target = e.target as HTMLInputElement; target.select(); target.setSelectionRange(0, 0); }}
                    onClick={(e) => { const target = e.target as HTMLInputElement; target.setSelectionRange(0, 0); }}
                    className="w-full pl-12 pr-4 py-6 text-2xl font-bold text-black bg-white border-4 border-gray-600 rounded-lg focus:ring-4 focus:ring-blue-600 focus:border-blue-600"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Stock */}
          <div>
            <h3 className="text-2xl font-bold text-gray-900 mb-6">📦 Stock</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-2xl font-bold text-black mb-3">
                  Stock Actual
                </label>
                <input
                  type="number"
                  value={product.stock_actual}
                  onChange={(e) => setProduct({...product, stock_actual: parseInt(e.target.value) || 0})}
                  onFocus={(e) => { const target = e.target as HTMLInputElement; target.select(); target.setSelectionRange(0, 0); }}
                  onClick={(e) => { const target = e.target as HTMLInputElement; target.setSelectionRange(0, 0); }}
                  className="w-full px-4 py-6 text-2xl font-bold text-black bg-white border-4 border-gray-600 rounded-lg focus:ring-4 focus:ring-blue-600 focus:border-blue-600"
                />
              </div>

              <div>
                <label className="block text-2xl font-bold text-black mb-3">
                  Stock Mínimo
                </label>
                <input
                  type="number"
                  value={product.stock_minimo}
                  onChange={(e) => setProduct({...product, stock_minimo: parseInt(e.target.value) || 0})}
                  onFocus={(e) => { const target = e.target as HTMLInputElement; target.select(); target.setSelectionRange(0, 0); }}
                  onClick={(e) => { const target = e.target as HTMLInputElement; target.setSelectionRange(0, 0); }}
                  className="w-full px-4 py-6 text-2xl font-bold text-black bg-white border-4 border-gray-600 rounded-lg focus:ring-4 focus:ring-blue-600 focus:border-blue-600"
                />
              </div>
            </div>
          </div>

          {/* Botones */}
          <div className="flex gap-4 pt-6">
            <button
              type="submit"
              disabled={saving}
              className="flex-1 bg-green-600 text-white py-4 px-6 rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-bold text-xl transition-colors duration-200"
            >
              {saving ? '💾 Guardando...' : '💾 Guardar Cambios'}
            </button>
            <a
              href="/products"
              className="bg-gray-600 text-white py-4 px-6 rounded-lg hover:bg-gray-700 font-bold text-xl transition-colors duration-200 text-center"
            >
              ❌ Cancelar
            </a>
          </div>
        </form>
      </div>
    </div>
  );
}