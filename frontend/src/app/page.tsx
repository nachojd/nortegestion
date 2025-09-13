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
