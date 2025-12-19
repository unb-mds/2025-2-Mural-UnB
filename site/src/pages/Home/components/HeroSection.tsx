import Logo from "assets/images/MuralLogo_M.svg"
import CampusFGA from "assets/images/fotos/CampusFGA.jpeg"

const HeroSection = () => {
  return (
    <div className="relative w-full">
      {/* Banner de fundo */}
      <div className="w-full h-[50vw] min-h-[16rem] max-h-[32rem]">
        <img
          src={CampusFGA}
          alt="Banner Campus"
          className="w-full h-full object-cover object-top"
        />
      </div>

      {/* Logo e subtítulo sobrepostos - à direita */}
      <div className="absolute top-1/2 -translate-y-1/2 right-[12%]">
        <div className="flex flex-col items-center">
          <img 
            src={Logo} 
            className="w-[30vw] min-w-[10rem] max-w-[24rem] h-auto drop-shadow-2xl" 
            alt="Logo Mural" 
          />
          <h1 className="text-[clamp(1rem,2.5vw,1.725rem)] font-gowunBold text-center text-white drop-shadow-lg mt-[1vw] w-[28vw] min-w-[9rem] max-w-[22rem] leading-tight">
            O mural digital da Universidade de Brasília!
          </h1>
        </div>
      </div>
    </div>
  )
}

export default HeroSection
