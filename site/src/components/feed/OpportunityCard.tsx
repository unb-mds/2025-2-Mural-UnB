
import { Link } from "react-router-dom"

interface Opportunity {
  id: string
  title: string
  description: string
  date: string
  location: string
  tags: string[]
  link: string
  logo?: string
}

interface OpportunityCardProps {
  opportunity: Opportunity
}

export default function OpportunityCard({ opportunity }: OpportunityCardProps) {
  return (
    <Link 
      to={`/feed/${opportunity.id}`} 
      className="flex flex-row items-center gap-6 bg-white rounded-xl p-6 border border-[#e5e5e5] transition-all duration-200 no-underline text-inherit w-full hover:-translate-y-0.5 hover:shadow-[0_4px_12px_rgba(0,0,0,0.1)] hover:border-[#1a7f4e]"
    >
      {opportunity.logo && (
        <div className="flex-shrink-0 w-20 h-20 rounded-lg bg-[#f5f5f5] flex items-center justify-center overflow-hidden border border-[#e5e5e5]">
          <img 
            src={opportunity.logo} 
            alt={`${opportunity.title} logo`}
            className="w-full h-full object-cover"
          />
        </div>
      )}
      
      <div className="flex-1 flex flex-col gap-2 min-w-0">
        <div className="flex justify-between items-start gap-4">
          <h3 className="text-xl font-bold text-[#1a1a1a] m-0 flex-1 leading-tight">{opportunity.title}</h3>
        </div>

        <p className="text-base text-[#666] leading-relaxed m-0">{opportunity.description}</p>

        <div className="flex flex-wrap gap-2 items-center mt-2">
          {opportunity.tags.slice(0, 2).map((tag) => (
            <span 
              key={tag} 
              className="inline-block py-1.5 px-3 bg-[#f0f9f4] border border-[#b8e6d0] rounded-2xl text-xs text-[#15663e] font-medium"
            >
              {tag.replace(/_/g, " ")}
            </span>
          ))}
          {opportunity.tags.length > 2 && (
            <span className="text-xs text-[#666] font-medium">+{opportunity.tags.length - 2}</span>
          )}
        </div>
      </div>
    </Link>
  )
}
