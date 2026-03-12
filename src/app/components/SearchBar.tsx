import { Search, Sparkles } from "lucide-react";
import { useState } from "react";

export function SearchBar() {
  const [searchQuery, setSearchQuery] = useState("");

  return (
    <div className="bg-gradient-to-br from-[#1B263B] to-[#415A77] py-12 px-6">
      <div className="max-w-[900px] mx-auto">
        <h2 className="text-white text-center mb-6">
          Descreva seu caso e nossa IA encontrará o advogado ideal
        </h2>
        
        <div className="relative">
          <div className="absolute left-4 top-1/2 -translate-y-1/2 text-[#778DA9]">
            <Search size={20} />
          </div>
          
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Ex: Preciso de um advogado para divórcio consensual em São Paulo..."
            className="w-full pl-12 pr-32 py-4 rounded-lg border-2 border-transparent focus:border-white focus:outline-none text-[#1B263B] placeholder:text-[#778DA9]"
          />
          
          <button className="absolute right-2 top-1/2 -translate-y-1/2 bg-[#415A77] hover:bg-[#1B263B] text-white px-6 py-2.5 rounded-md transition-colors flex items-center gap-2">
            <Sparkles size={18} />
            <span>Buscar</span>
          </button>
        </div>

        <p className="text-white/80 text-sm text-center mt-4">
          Powered by IA • Resultados personalizados em segundos
        </p>
      </div>
    </div>
  );
}
