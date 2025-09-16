'use client';

import { useQuery } from '@tanstack/react-query';
import apiClient from '@/lib/axios';

interface Product {
  id: number;
  codigo?: string;
  nombre: string;
  rubro_nombre: string;
  marca_nombre: string;
  precio_venta: string;
  precio_con_iva: string;
  stock_actual: number;
  activo: boolean;
}

interface ApiResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Product[];
}

interface SearchParams {
  page: number;
  pageSize: number;
  searchCode: string;
  searchName: string;
  searchRubro: string;
  searchMarca: string;
}

const fetchProducts = async (params: SearchParams): Promise<ApiResponse> => {
  const { page, pageSize, searchCode, searchName, searchRubro, searchMarca } = params;
  
  const urlParams = new URLSearchParams({
    page: page.toString(),
    page_size: pageSize.toString(),
  });
  
  // El backend no soporta filtros separados por campo, usamos search para todo
  // y luego filtramos en el frontend para búsqueda exacta de código
  if (searchCode || searchName) {
    urlParams.append('search', searchCode || searchName);
  }
  if (searchRubro) urlParams.append('rubro__nombre__icontains', searchRubro);
  if (searchMarca) urlParams.append('marca__nombre__icontains', searchMarca);

  const finalUrl = `/api/products/?${urlParams.toString()}`;

  console.log('🔍 API Call:', finalUrl);
  console.log('📋 Search params:', { searchCode, searchName, searchRubro, searchMarca });

  const response = await apiClient.get<ApiResponse>(finalUrl);
  
  console.log('📊 API Response:', { count: response.data.count, results: response.data.results.length });
  
  // Si se busca por código, filtrar resultados para coincidencia exacta
  if (searchCode) {
    const filteredResults = response.data.results.filter(product => 
      product.codigo?.toLowerCase() === searchCode.toLowerCase()
    );
    console.log('🔍 Filtered by exact code:', { original: response.data.results.length, filtered: filteredResults.length });
    return {
      ...response.data,
      results: filteredResults,
      count: filteredResults.length,
    };
  }
  
  return response.data;
};

export const useProducts = (params: SearchParams) => {
  return useQuery({
    queryKey: ['products', params],
    queryFn: () => fetchProducts(params),
    staleTime: 1000 * 60, // 1 minute
    gcTime: 1000 * 60 * 5, // 5 minutes (antes cacheTime)
    refetchOnWindowFocus: false,
    enabled: true, // Always enable, React Query will handle caching
  });
};