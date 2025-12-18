import {
  PageTitle,
  DevelopersGrid,
  AboutDescription,
} from "./components"

export default function Sobre() {
  return (
    <div className="flex flex-col items-center">
      <PageTitle />
      <DevelopersGrid />
      <AboutDescription />
    </div>
  )
}
