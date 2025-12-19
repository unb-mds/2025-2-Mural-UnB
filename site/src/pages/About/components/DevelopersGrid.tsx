import DeveloperCard from "./DeveloperCard"
import { developers } from "../data/developers"

const DevelopersGrid = () => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 px-2 sm:px-4 py-8 w-full max-w-5xl mx-auto place-items-center">
      {developers.map((dev) => (
        <DeveloperCard
          key={dev.id}
          name={dev.name}
          role={dev.role}
          image={dev.image}
          imageAlt={dev.imageAlt}
          githubUrl={dev.githubUrl}
          linkedinUrl={dev.linkedinUrl}
          className="w-56 h-72" // menor que w-64 h-80
        />
      ))}
    </div>
  )
}

export default DevelopersGrid
