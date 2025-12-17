interface DescriptionSectionProps {
  title: string
  content: string
}

const DescriptionSection = ({ title, content }: DescriptionSectionProps) => {
  return (
    <section className="mb-8">
      <h2 className="text-2xl font-bold text-[#1a1a1a] mb-4 pb-2 border-b-2 border-[#e5e5e5]">
        {title}
      </h2>
      <p className="text-lg text-[#666] leading-[1.8] m-0">{content}</p>
    </section>
  )
}

export default DescriptionSection
