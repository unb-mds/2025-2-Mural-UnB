import { Link } from "react-router-dom"

const NotFoundState = () => {
  return (
    <div className="max-w-[1200px] mx-auto p-8 min-h-[calc(100vh-80px)] max-md:p-4">
      <div className="text-center py-16 px-8">
        <h1 className="text-[2rem] text-[#1a1a1a] mb-4">
          Oportunidade não encontrada
        </h1>
        <Link
          to="/"
          className="inline-flex items-center gap-2 text-[#1a7f4e] no-underline font-semibold mb-8 transition-colors hover:text-[#15663e]"
        >
          Voltar para oportunidades
        </Link>
      </div>
    </div>
  )
}

export default NotFoundState
