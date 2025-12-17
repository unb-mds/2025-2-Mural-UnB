import TB from "assets/images/fotos/devs/TB.jpeg"
import LF from "assets/images/fotos/devs/LF.jpeg"
import JG from "assets/images/fotos/devs/JG.jpeg"
import LL from "assets/images/fotos/devs/LL.jpeg"
import MS from "assets/images/fotos/devs/MS.jpeg"
import MG from "assets/images/fotos/devs/MG.jpeg"

export interface Developer {
  id: string
  name: string
  image: string
  imageAlt: string
  githubUrl: string
}

export const developers: Developer[] = [
  {
    id: "tiago",
    name: "Tiago Bittencourt",
    image: TB,
    imageAlt: "TiagoB",
    githubUrl: "https://github.com/TiagoSBittencourt",
  },
  {
    id: "joao",
    name: "João Gonzaga",
    image: JG,
    imageAlt: "JoaoG",
    githubUrl: "https://github.com/Karmantinedev",
  },
  {
    id: "lucas",
    name: "Lucas Fujimoto",
    image: LF,
    imageAlt: "LucasF",
    githubUrl: "https://github.com/Lucasft16",
  },
  {
    id: "maria",
    name: "Maria Gontijo",
    image: MG,
    imageAlt: "MariaG",
    githubUrl: "https://github.com/MariaClara-Canuto",
  },
  {
    id: "matheus",
    name: "Matheus Saraiva",
    image: MS,
    imageAlt: "MatheusS",
    githubUrl: "https://github.com/apptrx",
  },
  {
    id: "luan",
    name: "Luan Ludry",
    image: LL,
    imageAlt: "LuanL",
    githubUrl: "https://github.com/luanludry",
  },
]
