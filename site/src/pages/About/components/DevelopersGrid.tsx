import DeveloperCard from "./DeveloperCard"
import { developers } from "../data/developers"

const DevelopersGrid = () => {
  return (
    <div className="flex flex-row -m-5">
      {developers.map((dev) => (
        <DeveloperCard
          key={dev.id}
          name={dev.name}
          image={dev.image}
          imageAlt={dev.imageAlt}
          githubUrl={dev.githubUrl}
        />
      ))}
    </div>
  )
}

export default DevelopersGrid
