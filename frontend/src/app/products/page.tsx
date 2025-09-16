'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useDebounce } from 'use-debounce';
import { useProducts } from '@/hooks/useProducts';
<<<<<<< HEAD

export default function ProductsPage() {
=======
import ProtectedRoute from '@/components/ProtectedRoute';

function ProductsContent() {
>>>>>>> main
  const router = useRouter();
  
  // Estados de búsqueda
  const [searchCode, setSearchCode] = useState('');
  const [searchName, setSearchName] = useState('');
  const [searchRubro, setSearchRubro] = useState('');
  const [searchMarca, setSearchMarca] = useState('');
  
  // Estados de paginación
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(50);
  
  // Debounce para búsquedas suaves (300ms)
  const [debouncedSearchCode] = useDebounce(searchCode, 300);
  const [debouncedSearchName] = useDebounce(searchName, 300);
  const [debouncedSearchRubro] = useDebounce(searchRubro, 300);
  const [debouncedSearchMarca] = useDebounce(searchMarca, 300);
  
  // React Query hook - automáticamente refetch cuando cambien los parámetros
  const { data, isLoading, error, isFetching } = useProducts({
    page: currentPage,
    pageSize,
    searchCode: debouncedSearchCode,
    searchName: debouncedSearchName,
    searchRubro: debouncedSearchRubro,
    searchMarca: debouncedSearchMarca,
  });
  
  const products = data?.results || [];
  const totalCount = data?.count || 0;
  const totalPages = Math.ceil(totalCount / pageSize);
  
  // Reset a página 1 cuando cambien los filtros de búsqueda
  const handleSearchChange = (setter: (value: string) => void) => (value: string) => {
    setter(value);
    if (currentPage > 1) {
      setCurrentPage(1);
    }
  };
  
  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };
  
  const handlePageSizeChange = (newPageSize: number) => {
    setPageSize(newPageSize);
    setCurrentPage(1);
  };
  
  const clearFilters = () => {
    setSearchCode('');
    setSearchName('');
    setSearchRubro('');
    setSearchMarca('');
    setCurrentPage(1);
  };
  
  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 text-lg font-semibold mb-4">
          Error al cargar los productos
        </div>
        <p className="text-gray-600">Por favor, intenta recargar la página</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header con indicador de carga */}
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center mb-6 gap-4">
        <div>
          <h1 className="text-3xl font-bold text-blue-700 mb-2">
            📦 Gestión de Productos
            {isFetching && <span className="ml-2 text-sm text-blue-500 animate-pulse">🔄</span>}
          </h1>
          <p className="text-gray-800">
            Total: <span className="font-bold text-blue-600">{totalCount.toLocaleString()}</span> productos
          </p>
        </div>
        <button className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors duration-200 font-medium">
          + Agregar Producto
        </button>
      </div>

      {/* Filtros */}
      <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6 shadow-sm">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">🔍 Filtros de Búsqueda</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
          <div>
            <label className="block text-sm font-semibold text-gray-800 mb-1">Código</label>
            <input
              type="text"
              placeholder="Buscar por código..."
              value={searchCode}
              onChange={(e) => handleSearchChange(setSearchCode)(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-input-dark"
            />
          </div>
          
          <div>
            <label className="block text-sm font-semibold text-gray-800 mb-1">Nombre</label>
            <input
              type="text"
              placeholder="Buscar por nombre..."
              value={searchName}
              onChange={(e) => handleSearchChange(setSearchName)(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-input-dark"
            />
          </div>
          
          <div>
            <label className="block text-sm font-semibold text-gray-800 mb-1">Rubro</label>
            <input
              type="text"
              placeholder="Buscar por rubro..."
              value={searchRubro}
              onChange={(e) => handleSearchChange(setSearchRubro)(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-input-dark"
            />
          </div>
          
          <div>
            <label className="block text-sm font-semibold text-gray-800 mb-1">Marca</label>
            <input
              type="text"
              placeholder="Buscar por marca..."
              value={searchMarca}
              onChange={(e) => handleSearchChange(setSearchMarca)(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-input-dark"
            />
          </div>
        </div>

        <div className="flex justify-between items-center">
          <button
            onClick={clearFilters}
            className="px-4 py-2 text-gray-800 hover:text-blue-600 underline font-medium"
          >
            Limpiar filtros
          </button>
          
          <div className="flex items-center gap-2">
            <label className="text-sm font-semibold text-gray-800">Productos por página:</label>
            <select
              value={pageSize}
              onChange={(e) => handlePageSizeChange(parseInt(e.target.value))}
              className="px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value={25}>25</option>
              <option value={50}>50</option>
              <option value={100}>100</option>
              <option value={200}>200</option>
            </select>
          </div>
        </div>
      </div>

      {/* Loading state mejorado */}
      {isLoading && (
        <div className="flex items-center justify-center py-12">
          <div className="flex items-center space-x-2">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
            <span className="text-gray-600 font-medium">Cargando productos...</span>
          </div>
        </div>
      )}

      {/* Tabla de productos */}
      {!isLoading && (
        <div className="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-100 border-b border-gray-300">
                <tr>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-800 uppercase tracking-wider">Código</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-800 uppercase tracking-wider">Descripción</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-800 uppercase tracking-wider">Rubro</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-800 uppercase tracking-wider">Marca</th>
                  <th className="px-4 py-3 text-right text-sm font-semibold text-gray-800 uppercase tracking-wider">Precio</th>
                  <th className="px-4 py-3 text-center text-sm font-semibold text-gray-800 uppercase tracking-wider">Estado</th>
                  <th className="px-4 py-3 text-center text-sm font-semibold text-gray-800 uppercase tracking-wider">Acciones</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {products.map((product, index) => (
                  <tr key={product.id} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                    <td className="px-4 py-3 text-sm font-medium text-gray-900">{product.codigo}</td>
                    <td className="px-4 py-3 text-sm text-gray-900">{product.nombre}</td>
                    <td className="px-4 py-3 text-sm text-gray-700">{product.rubro_nombre}</td>
                    <td className="px-4 py-3 text-sm text-gray-700">{product.marca_nombre}</td>
                    <td className="px-4 py-3 text-sm text-right font-medium text-green-600">
                      ${parseFloat(product.precio_venta || '0').toFixed(2)}
                    </td>
                    <td className="px-4 py-3 text-sm text-center">
                      {(() => {
                        const hasPrice = parseFloat(product.precio_venta || '0') > 0;
                        const isActive = hasPrice; // Activo solo si tiene precio
                        return (
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                            isActive ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                          }`}>
                            {isActive ? 'Activo' : 'Inactivo'}
                          </span>
                        );
                      })()}
                    </td>
                    <td className="px-4 py-3 text-sm text-center">
                      <div className="flex justify-center space-x-2">
                        <button 
                          onClick={() => router.push(`/products/edit/${product.id}`)}
                          className="text-blue-600 hover:text-blue-900 font-medium"
                        >
                          Editar
                        </button>
                        <button className="text-red-600 hover:text-red-900 font-medium">
                          Eliminar
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Empty state */}
      {!isLoading && products.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.034 0-3.9.785-5.291 2.09M6.343 6.343L4.93 4.93m0 0L3.515 3.515M4.929 4.929L3.515 6.343" />
            </svg>
          </div>
          <p className="text-lg font-semibold text-gray-800">No se encontraron productos</p>
          <p className="text-gray-600 mt-2">Prueba ajustando los filtros de búsqueda</p>
          <button
            onClick={clearFilters}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Limpiar filtros
          </button>
        </div>
      )}

      {/* Paginación */}
      {!isLoading && products.length > 0 && (
        <div className="mt-6 flex flex-col sm:flex-row justify-between items-center gap-4">
          <div className="text-sm text-gray-800 font-medium">
            Mostrando {((currentPage - 1) * pageSize) + 1} a {Math.min(currentPage * pageSize, totalCount)} de {totalCount.toLocaleString()} productos
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={() => handlePageChange(currentPage - 1)}
              disabled={currentPage <= 1}
              className="px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Anterior
            </button>
            
            <div className="flex space-x-1">
              {[...Array(Math.min(10, totalPages))].map((_, index) => {
                const pageNumber = Math.max(1, currentPage - 5) + index;
                if (pageNumber <= totalPages) {
                  return (
                    <button
                      key={pageNumber}
                      onClick={() => handlePageChange(pageNumber)}
                      className={`px-3 py-2 text-sm font-medium rounded-md ${
                        currentPage === pageNumber
                          ? 'bg-blue-600 text-white'
                          : 'text-gray-700 bg-white border border-gray-300 hover:bg-gray-50'
                      }`}
                    >
                      {pageNumber}
                    </button>
                  );
                }
                return null;
              })}
            </div>
            
            <button
              onClick={() => handlePageChange(currentPage + 1)}
              disabled={currentPage >= totalPages}
              className="px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Siguiente
            </button>
          </div>
        </div>
      )}
    </div>
  );
<<<<<<< HEAD
=======
}

export default function ProductsPage() {
  return (
    <ProtectedRoute>
      <ProductsContent />
    </ProtectedRoute>
  );
>>>>>>> main
}