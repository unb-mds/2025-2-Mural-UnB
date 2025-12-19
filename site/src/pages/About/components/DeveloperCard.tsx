import GitHubIcon from "./GitHubIcon"
import LinkedInIcon from "./LinkedInIcon"

interface DeveloperCardProps {
  name: string
  role: string
  image: string
  imageAlt: string
  githubUrl?: string
  linkedinUrl?: string
}

const DeveloperCard = ({ name, role, image, imageAlt, githubUrl, linkedinUrl, className }: DeveloperCardProps & { className?: string }) => {
  return (
    <div className={`group [perspective:1000px] ${className || 'w-64 h-80'} cursor-pointer`}>
      {/* Container do flip */}
      <div className="relative w-full h-full transition-transform duration-700 [transform-style:preserve-3d] group-hover:[transform:rotateY(180deg)]">
        
        {/* Frente do card */}
        <div className="absolute w-full h-full [backface-visibility:hidden] rounded-2xl overflow-hidden shadow-xl">
          {/* Imagem */}
          <div className="relative w-full h-full">
            <img 
              src={image} 
              alt={imageAlt} 
              className="w-full h-full object-cover"
            />
            {/* Overlay com nome e role */}
            <div className="absolute bottom-0 left-0 right-0 bg-primary p-4">
              <h3 className="text-white font-bold text-lg">{name}</h3>
              <p className="text-white/80 text-sm">{role}</p>
            </div>
          </div>
        </div>

        {/* Verso do card */}
        <div className="absolute w-full h-full [backface-visibility:hidden] [transform:rotateY(180deg)] rounded-2xl overflow-hidden shadow-xl bg-base-100 flex flex-col items-center justify-center p-6 text-center">
          {/* Decoração de fundo */}
          <div className="absolute top-0 right-0 w-32 h-32 bg-primary/5 rounded-full -translate-y-1/2 translate-x-1/2"></div>
          <div className="absolute bottom-0 left-0 w-28 h-28 bg-secondary/5 rounded-full translate-y-1/2 -translate-x-1/2"></div>

          <div className="w-25 h-25 rounded-full overflow-hidden border-3 border-blue mb-4">
            <img 
              src={image} 
              alt={imageAlt} 
              className="w-full h-full object-cover"
            />
          </div>
          <h3 className="text-white font-bold text-xl mb-1">{name}</h3>
          <p className="text-white/80 text-sm mb-6">{role}</p>
          
      {/* Ícones sociais */}
      <div className="absolute bottom-4 right-4 flex gap-3">
        {githubUrl && (
          <a
            href={githubUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="text-black hover:scale-110 transition-transform"
            aria-label="GitHub"
          >
            <GitHubIcon className="w-6 h-6" />
          </a>
        )}

        {linkedinUrl && (
          <a
            href={linkedinUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="text-black hover:scale-110 transition-transform"
            aria-label="LinkedIn"
          >
            <LinkedInIcon className="w-6 h-6" />
          </a>
          )}
        </div>

        </div>
      </div>
    </div>
  )
}

export default DeveloperCard
