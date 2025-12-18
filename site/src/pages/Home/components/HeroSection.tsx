import Logo from "assets/images/MuralLogo_M.svg"
import CampusFGA from "assets/images/fotos/CampusFGA.jpeg"

const HeroSection = () => {
  return (
    <>
      <div className="w-full max-w-full px-6">
        <img src={Logo} className="mt-7 mb-12 w-95 h-48 mx-auto" alt="Logo Mural" />
        <h1 className="text-3xl font-gowunBold p-3 text-center">O mural digital da Universidade de Brasília!</h1>
      </div>

      <div className="w-screen mt-10">
        <img
          src={CampusFGA}
          alt="Banner Campus"
          className="w-full h-160 object-cover object-top"
        />
      </div>
    </>
  )
}

export default HeroSection
