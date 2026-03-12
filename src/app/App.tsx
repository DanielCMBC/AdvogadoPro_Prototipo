import { Header } from "./components/Header";
import { SearchBar } from "./components/SearchBar";
import { Sidebar } from "./components/Sidebar";
import { LawyerCard } from "./components/LawyerCard";

export default function App() {
  return (
    <div className="min-h-screen bg-[#E0E1DD]">
      <Header />
      <SearchBar />
      
      <div className="flex max-w-[1400px] mx-auto">
        <Sidebar />
        
        <main className="flex-1 p-6">
          <div className="mb-6 flex items-center justify-between">
            <div>
              <h2 className="text-[#1B263B] mb-1">
                Resultados
              </h2>
              <p className="text-[#778DA9]">
                9 resultados encontrados
              </p>
            </div>
            
            <select className="px-4 py-2 border border-[#778DA9]/30 rounded-lg focus:border-[#415A77] focus:outline-none bg-white text-[#1B263B]">
              <option>Ordenar por</option>
              <option>Opção 1</option>
              <option>Opção 2</option>
              <option>Opção 3</option>
            </select>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(9)].map((_, i) => (
              <LawyerCard key={i} />
            ))}
          </div>
        </main>
      </div>
    </div>
  );
}
