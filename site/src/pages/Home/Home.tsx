import Carousel from "components/Carousel"
import Logo from "assets/images/MuralLogo_M.svg"
import NotePad from "assets/images/NotePad.png"
import CampusFGA from "assets/images/fotos/CampusFGA.jpeg"
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="flex flex-col items-center">
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

      <div className="flex flex-col items-center gap-6 mt-10">
        <h1 className="text-4xl font-bold mb-2">Sobre Nós</h1>

        <div className="rounded-xl p-6 bg-base-100 flex flex-col items-center text-center w-234 drop-shadow-md">
          <h1 className="text-2xl font-gowunBold mb-2">Quem somos?</h1>
          <h2 className="whitespace-normal wrap-break-words text-base">
            O Mural UnB é uma plataforma digital projetada para centralizar e recomendar oportunidades acadêmicas e profissionais dentro da Universidade de Brasília (UnB).
          </h2>
        </div>

        <div className="flex flex-row gap-10">
          <div className="rounded-xl p-6 bg-base-100 flex flex-col items-center text-center max-w-md drop-shadow-md">
            <h1 className="text-2xl font-gowunBold mb-2">Objetivo?</h1>
            <h2 className="whitespace-normal wrap-break-words text-base">
              O objetivo é criar uma experiência personalizada, onde os estudantes possam facilmente descobrir oportunidades alinhadas aos seus interesses e histórico acadêmico.
            </h2>
          </div>

          <div className="rounded-xl p-6 bg-base-100 flex flex-col items-center text-center max-w-md drop-shadow-md">
            <h1 className="text-2xl font-gowunBold mb-2">Como?</h1>
            <h2 className="whitespace-normal wrap-break-words text-base">
              Analisamos os interesses e preferências do usuário utilizando machine learning para recomendar as opções mais relevantes e enviar notificações sobre novas oportunidades.
            </h2>
          </div>
        </div>
      </div>

      <Link to="/feed">
        <button className="btn btn-soft btn-primary p-10 rounded-full mt-10 mb-5 w-210">
          <h1 className="text-4xl">Acesse o Mural</h1>
        </button>
      </Link>

      <div className="w-full px-6">
        <section className="w-full py-8 bg-base-200 mt-10">
          <div className="container mx-auto px-4">
            <Carousel />
          </div>
        </section>
      </div>

      <div className="flex flex-row items-center justify-center gap-12 py-16 px-8 bg-base-100 rounded-2xl shadow-lg mx-6 mb-12 mt-8">
        <div className="flex-1 max-w-lg">
          <h1 className="text-2xl md:text-2xl leading-relaxed font-gowunBold text-primary">
            Aqui você encontra os detalhes sobre laboratórios, empresas juniores e equipes de competição da UnB-FGA de maneira simplificada e rápida!
          </h1>
        </div>
        <Link to="/feed">
          <div className="flex-shrink-0">
            <img
              src={NotePad}
              alt="Notepad illustration"
              className="w-64 h-auto        drop-shadow-xl"
            />
          </div>
        </Link>
      </div>

    </div>
  )
}