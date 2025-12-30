const idMap: { [key: string]: { headerName: string; ejId: string } } = {
  "ej-100022": { headerName: "engnet", ejId: "100022" },
  "ej-100021": { headerName: "enetec", ejId: "100021" },
  "ej-100019": { headerName: "embragea", ejId: "100019" },
  "ej-100018": { headerName: "eletrojun", ejId: "100018" },
}

const nameMap: { [key: string]: string } = {
  engnet: "engnet.png",
  enetec: "enetec.png",
  embragea: "embragea.png",
  eletronjun: "eletrojun.png",
  eletrojun: "eletrojun.png",
  cjr: "cjr.png",
  apuama: "apuama.png",
  unball: "unball.png",
  unbeatables: "unbeatables.jpg",
  unbeattles: "unbeattles.jpg",
  draco: "draco.png",
  piratas: "piratas.png",
  engrena: "engrena.png",
  aess: "aess.png",
  ailab: "ailab.png",
  matriz: "matriz.png",
  "ai lab": "ailab.png",
  "cube": "cubedesign.png",
  comsoc: "comsoc.png",
  cs: "cs.png",
  struct: "struct.png",
  labmicro: "labmicro.png",
  edra: "edra.png",
  "labtelecom/lcept": "labtelecom.png",
  gmec: "GMEC.png",
  lappis: "lappis.png",
  "capital rocket": "rocketcapital.png",
  cedis: "cedis.png",
  "rocket capital": "rocketcapital.png",
  "rocket team": "rocketcapital.png",
  cenia: "cenia.png",
  mamutes: "MAMUTES.png",
  mecajun: "mecajun.png",
  droid: "droid.png",
  titans: "titans.png",
  "computational intelligence": "cis-ieee.jpg",
  cis: "cis-ieee.jpg",
  nanotec: "NANOTEC.png",
  itrac: "itrac.png",
  circuit: "cas.png",
  o2: "o2.png",
  orc: "orc.png",
  unbaja: "unbaja.png",
  lara: "lara.png",
  "orc'estra": "orc.png",
  woman: "woman-engineering.png",
  orcestra: "orc.png",
  tecmec: "TECMEC.png",
}

export function resolveHeaderImage(id: string, name: string): string | null {
  if (!id && !name) return null

  const base = import.meta.env.BASE_URL || "/"
  const resolvePath = (path: string) =>
    base.endsWith("/") ? `${base}${path.slice(1)}` : `${base}${path}`

  if (id && idMap[id]) {
    const { headerName } = idMap[id]
    return resolvePath(`/images/headers/${headerName}.png`)
  }

  const n = name?.toLowerCase().trim() || ""

  for (const [key, filename] of Object.entries(nameMap)) {
    if (n.includes(key)) {
      return resolvePath(`/images/headers/${filename}`)
    }
  }

  return null
}

export function getEjFallbackPath(opportunityId: string): string | null {
  const ejId = opportunityId.replace("ej-", "")
  if (!ejId) return null

  const base = import.meta.env.BASE_URL || "/"
  const resolvePath = (path: string) =>
    base.endsWith("/") ? `${base}${path.slice(1)}` : `${base}${path}`

  return resolvePath(`/images/ejs/${ejId}.jpeg`)
}
