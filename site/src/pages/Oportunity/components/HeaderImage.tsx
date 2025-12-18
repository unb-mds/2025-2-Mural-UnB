import { getEjFallbackPath } from "../utils/resolveHeaderImage"

interface HeaderImageProps {
  imageUrl: string | null
  name: string
  opportunityId: string
}

const HeaderImage = ({ imageUrl, name, opportunityId }: HeaderImageProps) => {
  const handleImageError = (e: React.SyntheticEvent<HTMLImageElement>) => {
    const img = e.currentTarget
    const src = img.getAttribute("src") || ""

    if (src.includes("/images/ejs/") || !src.includes("/images/headers/")) {
      const parent = img.parentElement
      if (parent) {
        parent.className =
          "w-full h-[400px] bg-[#003366] rounded-t-xl mb-0 max-md:h-[250px] max-md:rounded-t-lg"
        img.style.display = "none"
      }
      return
    }

    const ejPath = getEjFallbackPath(opportunityId)
    if (ejPath) {
      img.src = ejPath
    } else {
      const parent = img.parentElement
      if (parent) {
        parent.className =
          "w-full h-[400px] bg-[#003366] rounded-t-xl mb-0 max-md:h-[250px] max-md:rounded-t-lg"
        img.style.display = "none"
      }
    }
  }

  if (!imageUrl) {
    return (
      <div className="w-full h-[400px] bg-[#003366] rounded-t-xl mb-0 max-md:h-[250px] max-md:rounded-t-lg" />
    )
  }

  return (
    <div className="w-full h-[400px] overflow-hidden rounded-t-xl mb-0 bg-[#003366] relative max-md:h-[250px] max-md:rounded-t-lg">
      <img
        src={imageUrl}
        alt={`${name} header`}
        className="w-full h-full object-cover block"
        onError={handleImageError}
      />
    </div>
  )
}

export default HeaderImage
