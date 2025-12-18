import GitHubIcon from "./GitHubIcon"

interface DeveloperCardProps {
  name: string
  image: string
  imageAlt: string
  githubUrl: string
}

const DeveloperCard = ({ name, image, imageAlt, githubUrl }: DeveloperCardProps) => {
  return (
    <div className="card bg-base-100 w-65 shadow-xl max-h-100 scale-75">
      <figure>
        <img src={image} alt={imageAlt} />
      </figure>
      <div className="card-body items-center">
        <h1 className="card-title pb-2 font-gowunBold">{name}</h1>
        <div className="card-actions items-center">
          <button className="btn btn-circle bg-black text-white border-black">
            <a href={githubUrl}>
              <GitHubIcon />
            </a>
          </button>
        </div>
      </div>
    </div>
  )
}

export default DeveloperCard
