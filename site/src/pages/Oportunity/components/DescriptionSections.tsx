import DescriptionSection from "./DescriptionSection"

interface DescriptionSectionsProps {
  about?: string
  mission?: string
  vision?: string
  values?: string
  services?: string
}

const DescriptionSections = ({
  about,
  mission,
  vision,
  values,
  services,
}: DescriptionSectionsProps) => {
  const hasContent = about || mission || vision || values || services

  if (!hasContent) return null

  return (
    <div className="leading-[1.8] text-[#333]">
      {about && <DescriptionSection title="Sobre" content={about} />}
      {mission && <DescriptionSection title="Missão" content={mission} />}
      {vision && <DescriptionSection title="Visão" content={vision} />}
      {values && <DescriptionSection title="Valores" content={values} />}
      {services && <DescriptionSection title="Serviços" content={services} />}
    </div>
  )
}

export default DescriptionSections
