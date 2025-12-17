interface OpportunityHeaderProps {
  logo?: string
  name: string
  category: string
  campus?: string
  shortDescription: string
}

const OpportunityHeader = ({
  logo,
  name,
  category,
  campus,
  shortDescription,
}: OpportunityHeaderProps) => {
  return (
    <header className="text-center mb-8 pb-8 border-b border-[#e5e5e5]">
      {logo && (
        <div className="w-[120px] h-[120px] mx-auto mb-6 rounded-xl overflow-hidden bg-[#f5f5f5] flex items-center justify-center">
          <img src={logo} alt={name} className="w-full h-full object-cover" />
        </div>
      )}

      <h1 className="text-[2.5rem] font-bold text-[#1a1a1a] m-0 mb-2 max-md:text-[2rem]">
        {name}
      </h1>

      <p className="text-base text-[#1a7f4e] font-semibold uppercase tracking-wide mb-4">
        {category}
        {campus && campus !== "N/A" && (
          <span className="opacity-90 font-normal"> • {campus}</span>
        )}
      </p>

      <p className="text-lg text-[#666] leading-relaxed m-0">
        {shortDescription}
      </p>
    </header>
  )
}

export default OpportunityHeader
