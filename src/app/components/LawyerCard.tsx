export function LawyerCard() {
  return (
    <div className="bg-white rounded-xl border border-[#778DA9]/20 overflow-hidden hover:shadow-lg transition-all hover:border-[#415A77]/40">
      {/* Área de Imagem - Placeholder */}
      <div className="w-full h-64 bg-[#778DA9]/20 flex items-center justify-center">
        <span className="text-[#778DA9] text-sm">Imagem</span>
      </div>

      <div className="p-6 space-y-4">
        {/* Campo Nome */}
        <div className="space-y-2">
          <div className="h-6 bg-[#778DA9]/20 rounded w-3/4"></div>
          <div className="text-xs text-[#778DA9]">Nome</div>
        </div>

        {/* Campo Informação 1 */}
        <div className="space-y-2">
          <div className="h-5 bg-[#778DA9]/20 rounded w-full"></div>
          <div className="text-xs text-[#778DA9]">Informação 1</div>
        </div>

        {/* Campo Informação 2 */}
        <div className="space-y-2">
          <div className="h-5 bg-[#778DA9]/20 rounded w-2/3"></div>
          <div className="text-xs text-[#778DA9]">Informação 2</div>
        </div>

        {/* Campo Avaliação */}
        <div className="space-y-2">
          <div className="flex gap-1">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="w-4 h-4 bg-[#778DA9]/20 rounded"></div>
            ))}
          </div>
          <div className="text-xs text-[#778DA9]">Avaliação</div>
        </div>

        {/* Campo Valor */}
        <div className="space-y-2 pb-4 border-b border-[#E0E1DD]">
          <div className="h-5 bg-[#778DA9]/20 rounded w-1/2"></div>
          <div className="text-xs text-[#778DA9]">Valor</div>
        </div>

        {/* Botão */}
        <button className="w-full py-2.5 border border-[#415A77] text-[#415A77] rounded-lg hover:bg-[#415A77] hover:text-white transition-colors">
          Ver Perfil
        </button>
      </div>
    </div>
  );
}
