import { useState } from "react";

export function Sidebar() {
  const [selectedRegion, setSelectedRegion] = useState("");
  const [selectedAreas, setSelectedAreas] = useState<string[]>([]);
  const [priceRange, setPriceRange] = useState([0, 10000]);
  const [minRating, setMinRating] = useState(0);

  const areas = [
    "Opção 1",
    "Opção 2",
    "Opção 3",
    "Opção 4",
    "Opção 5",
    "Opção 6",
  ];

  const toggleArea = (area: string) => {
    setSelectedAreas((prev) =>
      prev.includes(area) ? prev.filter((a) => a !== area) : [...prev, area]
    );
  };

  return (
    <aside className="w-80 bg-white border-r border-[#778DA9]/30 p-6 h-[calc(100vh-180px)] overflow-y-auto">
      <h3 className="text-[#1B263B] mb-6">Filtros</h3>

      {/* Filtro 1 */}
      <div className="mb-8">
        <label className="text-[#1B263B] mb-3 block">Filtro 1</label>
        <select
          value={selectedRegion}
          onChange={(e) => setSelectedRegion(e.target.value)}
          className="w-full px-4 py-2 border border-[#778DA9]/30 rounded-lg focus:border-[#415A77] focus:outline-none bg-white text-[#1B263B]"
        >
          <option value="">Selecione uma opção</option>
          <option value="1">Opção 1</option>
          <option value="2">Opção 2</option>
          <option value="3">Opção 3</option>
          <option value="4">Opção 4</option>
          <option value="5">Opção 5</option>
          <option value="6">Opção 6</option>
        </select>
      </div>

      {/* Filtro 2 */}
      <div className="mb-8">
        <label className="text-[#1B263B] mb-3 block">Filtro 2</label>
        <div className="space-y-2 max-h-64 overflow-y-auto">
          {areas.map((area) => (
            <label key={area} className="flex items-center gap-2 cursor-pointer group">
              <input
                type="checkbox"
                checked={selectedAreas.includes(area)}
                onChange={() => toggleArea(area)}
                className="w-4 h-4 rounded border-[#778DA9] text-[#415A77] focus:ring-[#415A77]"
              />
              <span className="text-sm text-[#1B263B] group-hover:text-[#415A77]">
                {area}
              </span>
            </label>
          ))}
        </div>
      </div>

      {/* Filtro 3 */}
      <div className="mb-8">
        <label className="text-[#1B263B] mb-3 block">Filtro 3</label>
        <div className="space-y-3">
          <input
            type="range"
            min="0"
            max="10000"
            step="500"
            value={priceRange[1]}
            onChange={(e) => setPriceRange([0, parseInt(e.target.value)])}
            className="w-full h-2 bg-[#E0E1DD] rounded-lg appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-[#415A77]"
          />
          <div className="flex justify-between text-sm text-[#778DA9]">
            <span>0</span>
            <span>{priceRange[1]}</span>
          </div>
        </div>
      </div>

      {/* Filtro 4 */}
      <div className="mb-8">
        <label className="text-[#1B263B] mb-3 block">Filtro 4</label>
        <div className="flex gap-2">
          {[1, 2, 3, 4, 5].map((rating) => (
            <button
              key={rating}
              onClick={() => setMinRating(rating)}
              className="w-8 h-8 rounded border border-[#778DA9]/30 flex items-center justify-center transition-all hover:border-[#415A77]"
              style={{
                backgroundColor: rating <= minRating ? "#415A77" : "white",
                color: rating <= minRating ? "white" : "#778DA9"
              }}
            >
              {rating}
            </button>
          ))}
        </div>
      </div>

      {/* Botão Limpar Filtros */}
      <button className="w-full py-2 border border-[#415A77] text-[#415A77] rounded-lg hover:bg-[#415A77] hover:text-white transition-colors">
        Limpar Filtros
      </button>
    </aside>
  );
}
