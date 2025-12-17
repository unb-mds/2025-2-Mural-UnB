interface EmptyStateProps {
  onClearFilters: () => void
}

const EmptyState = ({ onClearFilters }: EmptyStateProps) => {
  return (
    <div className="col-span-full text-center py-16 px-8 bg-white rounded-xl border border-[#e5e5e5]">
      <p className="text-lg text-[#666] mb-6">Nenhuma oportunidade encontrada.</p>
      <button
        onClick={onClearFilters}
        className="py-3 px-6 bg-[#1a7f4e] text-white border-none rounded-lg text-base font-semibold cursor-pointer transition-colors hover:bg-[#15663e]"
      >
        Limpar Busca
      </button>
    </div>
  )
}

export default EmptyState
