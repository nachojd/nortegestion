'use client';

import { useState, useEffect } from 'react';
import apiClient from '@/lib/axios';

interface Product {
  id: number;
  codigo: string;
  nombre: string;
  precio_venta: string;
  precio_con_iva: string;
}


interface Cliente {
  id: number;
  nombre: string;
  email: string;
  telefono: string;
}

interface QuoteItem {
  tipo: 'producto';
  id: number;
  nombre: string;
  cantidad: number;
  precio: number;
  subtotal: number;
}

export default function NewQuotePage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [selectedCliente, setSelectedCliente] = useState<number | null>(null);
  const [quoteItems, setQuoteItems] = useState<QuoteItem[]>([]);
  const [fechaVencimiento, setFechaVencimiento] = useState('');
  const [observaciones, setObservaciones] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
    // Set default expiration date (30 days from now)
    const futureDate = new Date();
    futureDate.setDate(futureDate.getDate() + 30);
    setFechaVencimiento(futureDate.toISOString().split('T')[0]);
  }, []);

  const fetchData = async () => {
    try {
      const [productsRes, clientesRes] = await Promise.all([
        apiClient.get('/api/products/'),
        apiClient.get('/api/clientes/')
      ]);
      
      setProducts(productsRes.data);
      setClientes(clientesRes.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  const addProduct = (product: Product) => {
    const existingItem = quoteItems.find(item => 
      item.tipo === 'producto' && item.id === product.id
    );

    if (existingItem) {
      setQuoteItems(items => 
        items.map(item => 
          item === existingItem 
            ? { ...item, cantidad: item.cantidad + 1, subtotal: (item.cantidad + 1) * item.precio }
            : item
        )
      );
    } else {
      const newItem: QuoteItem = {
        tipo: 'producto',
        id: product.id,
        nombre: product.nombre,
        cantidad: 1,
        precio: parseFloat(product.precio_venta),
        subtotal: parseFloat(product.precio_venta)
      };
      setQuoteItems(items => [...items, newItem]);
    }
  };


  const updateQuantity = (index: number, quantity: number) => {
    if (quantity <= 0) {
      removeItem(index);
      return;
    }

    setQuoteItems(items => 
      items.map((item, i) => 
        i === index 
          ? { ...item, cantidad: quantity, subtotal: quantity * item.precio }
          : item
      )
    );
  };

  const removeItem = (index: number) => {
    setQuoteItems(items => items.filter((_, i) => i !== index));
  };

  const calculateTotal = () => {
    const total = quoteItems.reduce((sum, item) => sum + item.subtotal, 0);
    
    return { total };
  };

  const createQuote = async () => {
    if (!selectedCliente || quoteItems.length === 0) {
      alert('Debe seleccionar un cliente y agregar al menos un item');
      return;
    }

    try {
      const quoteData = {
        cliente: selectedCliente,
        fecha_vencimiento: fechaVencimiento,
        observaciones,
        items: quoteItems.map(item => ({
          producto: item.id,
          servicio: null,
          cantidad: item.cantidad
        }))
      };

      const response = await apiClient.post('/api/quotes/', quoteData);
      
      alert('¡Presupuesto creado exitosamente!');
      window.location.href = '/quotes';
    } catch (error) {
      console.error('Error creating quote:', error);
      alert('Error al crear el presupuesto');
    }
  };

  const totals = calculateTotal();

  if (loading) {
    return (
      <div className="flex flex-col justify-center items-center h-64 space-y-4">
        <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
        <div className="text-lg text-gray-600 font-medium">Cargando datos...</div>
      </div>
    );
  }

  return (
    <div>
      <div className="flex flex-col sm:flex-row justify-between items-center mb-6 gap-4">
        <h1 className="text-2xl sm:text-3xl font-bold text-blue-700">
          Nuevo Presupuesto
        </h1>
        <a href="/quotes" className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors duration-200 font-medium">
          ← Volver
        </a>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Selection */}
        <div className="lg:col-span-2 space-y-6">
          {/* Cliente Selection */}
          <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Seleccionar Cliente</h3>
            <select 
              value={selectedCliente || ''} 
              onChange={(e) => setSelectedCliente(Number(e.target.value))}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-900"
            >
              <option value="">Seleccione un cliente...</option>
              {clientes.map(cliente => (
                <option key={cliente.id} value={cliente.id}>
                  {cliente.nombre} - {cliente.telefono}
                </option>
              ))}
            </select>
          </div>

          {/* Products */}
          <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">📦 Productos Disponibles</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-h-96 overflow-y-auto">
              {products.map(product => (
                <div key={product.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow duration-200">
                  <h4 className="font-medium text-sm text-gray-800">{product.nombre}</h4>
                  <p className="text-xs text-gray-500">{product.codigo}</p>
                  <p className="text-lg font-semibold text-gray-800">
                    ${parseFloat(product.precio_venta).toLocaleString('es-AR')}
                  </p>
                  <button 
                    onClick={() => addProduct(product)}
                    className="w-full mt-2 bg-blue-600 text-white py-2 px-2 rounded-lg text-sm hover:bg-blue-700 transition-colors duration-200 font-medium"
                  >
                    Agregar
                  </button>
                </div>
              ))}
            </div>
          </div>

        </div>

        {/* Right Column - Quote Summary */}
        <div className="space-y-6">
          {/* Quote Items */}
          <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">📋 Items del Presupuesto</h3>
            
            {quoteItems.length === 0 ? (
              <p className="text-gray-500 text-center py-4">
                Agregue productos o servicios
              </p>
            ) : (
              <div className="space-y-3">
                {quoteItems.map((item, index) => (
                  <div key={index} className="bg-gray-50 border border-gray-200 rounded-lg p-3 hover:shadow-sm transition-shadow duration-200">
                    <div className="flex justify-between items-start mb-2">
                      <div className="flex-1">
                        <h5 className="font-medium text-sm text-gray-800">{item.nombre}</h5>
                        <span className="text-xs text-gray-600">
                          📦 ${item.precio.toLocaleString('es-AR')} c/u
                        </span>
                      </div>
                      <button 
                        onClick={() => removeItem(index)}
                        className="text-red-600 hover:text-red-700 text-sm transition-colors duration-200"
                      >
                        🗑️
                      </button>
                    </div>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <button 
                          onClick={() => updateQuantity(index, item.cantidad - 1)}
                          className="bg-red-600 text-white px-2 py-1 rounded text-xs hover:bg-red-700 transition-colors duration-200 font-medium"
                        >
                          -
                        </button>
                        <span className="text-sm font-medium text-gray-800">{item.cantidad}</span>
                        <button 
                          onClick={() => updateQuantity(index, item.cantidad + 1)}
                          className="bg-green-600 text-white px-2 py-1 rounded text-xs hover:bg-green-700 transition-colors duration-200 font-medium"
                        >
                          +
                        </button>
                      </div>
                      <span className="font-semibold text-gray-800">
                        ${item.subtotal.toLocaleString('es-AR')}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Totals */}
          {quoteItems.length > 0 && (
            <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">💰 Totales</h3>
              <div className="space-y-2">
                <div className="flex justify-between font-bold text-lg">
                  <span className="text-gray-800">Total:</span>
                  <span className="text-gray-800">
                    ${totals.total.toLocaleString('es-AR', { minimumFractionDigits: 2 })}
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* Quote Details */}
          <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">📝 Detalles</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Fecha de Vencimiento
                </label>
                <input 
                  type="date" 
                  value={fechaVencimiento}
                  onChange={(e) => setFechaVencimiento(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-900"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Observaciones
                </label>
                <textarea 
                  value={observaciones}
                  onChange={(e) => setObservaciones(e.target.value)}
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-900"
                  placeholder="Observaciones adicionales..."
                />
              </div>
            </div>
          </div>

          {/* Action Button */}
          <button 
            onClick={createQuote}
            disabled={!selectedCliente || quoteItems.length === 0}
            className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium text-lg transition-colors duration-200"
          >
            ✨ Crear Presupuesto
          </button>
        </div>
      </div>
    </div>
  );
}