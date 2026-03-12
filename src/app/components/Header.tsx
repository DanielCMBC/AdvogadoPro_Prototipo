import { HelpCircle } from "lucide-react";
import { useState } from "react";

export function Header() {
  const [userType, setUserType] = useState<"cliente" | "advogado">("cliente");

  return (
    <header className="bg-white border-b border-[#778DA9]/30 px-6 py-4">
      <div className="max-w-[1400px] mx-auto flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 bg-[#1B263B] rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-xl">A</span>
          </div>
          <h1 className="text-2xl font-bold text-[#1B263B]">AdvoLog</h1>
        </div>

        {/* Toggle de Perfil */}
        <div className="flex items-center gap-1 bg-[#E0E1DD] rounded-lg p-1">
          <button
            onClick={() => setUserType("cliente")}
            className={`px-6 py-2 rounded-md transition-all ${
              userType === "cliente"
                ? "bg-white text-[#1B263B] shadow-sm"
                : "text-[#415A77] hover:text-[#1B263B]"
            }`}
          >
            Sou Cliente
          </button>
          <button
            onClick={() => setUserType("advogado")}
            className={`px-6 py-2 rounded-md transition-all ${
              userType === "advogado"
                ? "bg-white text-[#1B263B] shadow-sm"
                : "text-[#415A77] hover:text-[#1B263B]"
            }`}
          >
            Sou Advogado
          </button>
        </div>

        {/* Botão de Ajuda */}
        <button className="flex items-center gap-2 text-[#415A77] hover:text-[#1B263B] transition-colors">
          <HelpCircle size={20} />
          <span>Ajuda</span>
        </button>
      </div>
    </header>
  );
}
