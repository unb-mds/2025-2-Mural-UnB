import Carousel from "components/Carousel";
import Logo from "assets/images/MuralLogo_M.svg";
import CampusFGA from "assets/images/fotos/CampusFGA.jpeg";

export default function Home() {
  return (
    <div className="flex flex-col items-center">
      <div className="w-full max-w-full px-6">
        <img src={Logo} className='mt-7 mb-12 w-95 h-48 mx-auto' alt="Logo Mural" />
        <h1 className="text-3xl font-gowunBold p-3 text-center">O mural digital da Universidade de Brasília!</h1>
      </div>
      
      <div className="w-screen mt-10">
        <img
          src={CampusFGA}
          alt="Banner Campus"
          className="w-full h-190 object-cover object-top"
        />
      </div>

      <div className="flex flex-col items-center gap-6 mt-10">
        <h1 className="text-4xl font-bold mb-2">Sobre Nós</h1>
 
        <div className="rounded-xl p-6 bg-base-100 flex flex-col items-center text-center w-full max-w-2xl drop-shadow-md">
          <h1 className="text-2xl font-bold mb-2">Quem somos?</h1>
          <h2 className="whitespace-normal wrap-break-words text-base">
            O Mural UnB é uma plataforma digital projetada para centralizar e recomendar oportunidades acadêmicas e profissionais dentro da Universidade de Brasília (UnB).
          </h2>
        </div>

        <div className="flex flex-row gap-10">
          <div className="rounded-xl p-6 bg-base-100 flex flex-col items-center text-center max-w-md drop-shadow-md">
            <h1 className="text-2xl font-bold mb-2">Objetivo?</h1>
            <h2 className="whitespace-normal wrap-break-words text-base">
              O objetivo é criar uma experiência personalizada, onde os estudantes possam facilmente descobrir oportunidades alinhadas aos seus interesses e histórico acadêmico.
            </h2>
          </div>

          <div className="rounded-xl p-6 bg-base-100 flex flex-col items-center text-center max-w-md drop-shadow-md">
            <h1 className="text-2xl font-bold mb-2">Como?</h1>
            <h2 className="whitespace-normal wrap-break-words text-base">
              Analisamos os interesses e preferências do usuário utlizando machine learn para recomenda as opções mais relevantes e envia notificações sobre novas oportunidades.
            </h2>
          </div>
        </div>
      </div>



      <div className="w-full px-6">
        <section className="w-full py-8 bg-base-200 mt-10">
          <div className="container mx-auto px-4">
            <Carousel />
          </div>
        </section>
      </div>
    </div>
  );
}