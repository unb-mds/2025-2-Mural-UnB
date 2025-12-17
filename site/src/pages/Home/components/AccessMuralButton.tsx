import { Link } from "react-router-dom"

const AccessMuralButton = () => {
  return (
    <Link to="/feed">
      <button className="btn btn-soft btn-primary p-10 rounded-full mt-10 mb-5 w-210">
        <h1 className="text-4xl">Acesse o Mural</h1>
      </button>
    </Link>
  )
}

export default AccessMuralButton
