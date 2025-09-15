'use client';

import { useState, useEffect } from 'react';
import apiClient from '@/lib/axios';
import ProtectedRoute from '@/components/ProtectedRoute';

interface Quote {
  id: number;
  numero: string;
  cliente_nombre: string;
  fecha: string;
  fecha_vencimiento: string;
  total: string;
  activo: boolean;
}

function QuotesContent() {
  const [quotes, setQuotes] = useState<Quote[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchQuotes();
  }, []);

  const fetchQuotes = async () => {
    try {
      const response = await apiClient.get('/api/quotes/');
      setQuotes(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching quotes:', error);
      // Fallback data for demo
      setQuotes([
        {
          id: 1,
          numero: "P00001",
          cliente_nombre: "Juan Pérez",
          fecha: "2025-09-09T04:18:22.013529Z",
          fecha_vencimiento: "2025-10-09",
          total: "29610.66",
          activo: true
        }
      ]);
      setLoading(false);
    }
  };

  const downloadPDF = async (quoteId: number) => {
    try {
      window.open(`${process.env.NEXT_PUBLIC_API_URL}/api/quotes/${quoteId}/pdf/`, '_blank');
    } catch (error) {
      console.error('Error downloading PDF:', error);
    }
  };

  const shareWhatsApp = async (quote: Quote) => {
    const phone = prompt("Ingrese número de teléfono:", "+5491123456789");
    if (phone) {
      try {
        const response = await apiClient.post(`/api/quotes/${quote.id}/whatsapp/`, {
          phone: phone.replace(/[^0-9]/g, '')
        });
        window.open(response.data.whatsapp_url, '_blank');
      } catch (error) {
        console.error('Error sharing on WhatsApp:', error);
        // Fallback
        const message = `Presupuesto ${quote.numero} - Total: $${parseFloat(quote.total).toLocaleString('es-AR')}`;
        const whatsappUrl = `https://wa.me/${phone.replace(/[^0-9]/g, '')}?text=${encodeURIComponent(message)}`;
        window.open(whatsappUrl, '_blank');
      }
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('es-AR');
  };

  if (loading) {
    return (
      <div className="flex flex-col justify-center items-center h-64 space-y-4">
        <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
        <div className="text-lg text-gray-600 font-medium">Cargando presupuestos...</div>
      </div>
    );
  }

  return (
    <div>
      <div className="flex flex-col sm:flex-row justify-between items-center mb-6 gap-4">
        <h1 className="text-2xl sm:text-3xl font-bold text-blue-700">
          📋 Presupuestos
        </h1>
        <a href="/quotes/new" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200 font-medium">
          + Nuevo Presupuesto
        </a>
      </div>

      <div className="space-y-4">
        {quotes.map((quote) => (
          <div key={quote.id} className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow duration-200">
            <div className="flex flex-col sm:flex-row justify-between gap-4 mb-4">
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-gray-800 mb-1">
                  Presupuesto {quote.numero}
                </h3>
                <p className="text-gray-600 mb-2">Cliente: {quote.cliente_nombre}</p>
                <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                  <span>Creado: {formatDate(quote.fecha)}</span>
                  <span>Vence: {formatDate(quote.fecha_vencimiento)}</span>
                  <span className={`px-2 py-1 rounded text-xs font-medium ${
                    quote.activo ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'
                  }`}>
                    {quote.activo ? 'Activo' : 'Inactivo'}
                  </span>
                </div>
              </div>
              <div className="text-right">
                <p className="text-2xl font-bold text-gray-800">
                  ${parseFloat(quote.total).toLocaleString('es-AR', { minimumFractionDigits: 2 })}
                </p>
              </div>
            </div>
            
            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => downloadPDF(quote.id)}
                className="px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700 transition-colors duration-200 text-sm"
              >
                PDF
              </button>
              <button
                onClick={() => shareWhatsApp(quote)}
                className="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700 transition-colors duration-200 text-sm"
              >
                WhatsApp
              </button>
              <button className="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors duration-200 text-sm">
                Email
              </button>
              <button className="px-3 py-1 bg-gray-600 text-white rounded hover:bg-gray-700 transition-colors duration-200 text-sm">
                Duplicar
              </button>
              <button className="px-3 py-1 bg-yellow-600 text-white rounded hover:bg-yellow-700 transition-colors duration-200 text-sm">
                Editar
              </button>
            </div>
          </div>
        ))}
      </div>

      {quotes.length === 0 && (
        <div className="text-center py-16 bg-white border-2 border-dashed border-gray-200 rounded-lg">
          <div className="text-gray-600 text-xl font-medium mb-6">📋 No hay presupuestos creados</div>
          <a href="/quotes/new" className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors duration-200 font-medium">
            + Crear Primer Presupuesto
          </a>
        </div>
      )}
    </div>
  );
}

export default function QuotesPage() {
  return (
    <ProtectedRoute>
      <QuotesContent />
    </ProtectedRoute>
  );
}