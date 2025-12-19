import TB from "assets/images/fotos/devs/TB.jpeg"
import LF from "assets/images/fotos/devs/LF.jpeg"
import JG from "assets/images/fotos/devs/JG.jpeg"
import LL from "assets/images/fotos/devs/LL.jpeg"
import MS from "assets/images/fotos/devs/MS.jpeg"
import MG from "assets/images/fotos/devs/MG.jpeg"

export interface Developer {
  id: string
  name: string
  role: string
  image: string
  imageAlt: string
  githubUrl?: string
  linkedinUrl?: string
}

export const developers: Developer[] = [
  {
    id: "tiago",
    name: "Tiago Bittencourt",
    role: "SM • Desenvolvedor",
    image: TB,
    imageAlt: "TiagoB",
    githubUrl: "https://github.com/TiagoSBittencourt",
    linkedinUrl: "https://www.linkedin.com/in/tiagosbittencourt/",
  },
  {
    id: "joao",
    name: "João Gonzaga",
    role: "PO •Desenvolvedor",
    image: JG,
    imageAlt: "JoaoG",
    githubUrl: "https://github.com/Karmantinedev",
  },
  {
    id: "lucas",
    name: "Lucas Fujimoto",
    role: "Desenvolvedor",
    image: LF,
    imageAlt: "LucasF",
    githubUrl: "https://github.com/Lucasft16",
  },
  {
    id: "maria",
    name: "Maria Gontijo",
    role: "Desenvolvedora",
    image: MG,
    imageAlt: "MariaG",
    githubUrl: "https://github.com/MariaClara-Canuto",
  },
  {
    id: "matheus",
    name: "Matheus Saraiva",
    role: "Desenvolvedor",
    image: MS,
    imageAlt: "MatheusS",
    githubUrl: "https://github.com/apptrx",
  },
  {
    id: "luan",
    name: "Luan Ludry",
    role: "Desenvolvedor",
    image: LL,
    imageAlt: "LuanL",
    githubUrl: "https://github.com/luanludry",
  },
]
