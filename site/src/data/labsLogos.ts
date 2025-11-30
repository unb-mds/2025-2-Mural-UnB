// Helper para resolver caminhos de imagem com base path do Vite
function resolveImagePath(path: string): string {
  const base = import.meta.env.BASE_URL || '/'
  return base.endsWith('/') ? `${base}${path.slice(1)}` : `${base}${path}`
}

const labLogoMapRaw: Record<string, string> = {
  '200001': '/images/labs/200001.png',
  '200002': '/images/labs/200002.png',
  '200003': '/images/labs/200003.png',
  '200004': '/images/labs/200004.png',
  '200005': '/images/labs/200005.jpeg',
  '200007': '/images/labs/200007.png',
  '200008': '/images/labs/200008.png',
  '200009': '/images/labs/200009.png',
  '200010': '/images/default/1.png',
  '200011': '/images/default/1.png',
  '200012': '/images/labs/200012.png',
  '200013': '/images/labs/200013.png',
  '200015': '/images/labs/200015.png',
  '200018': '/images/labs/200018.jpeg',
  '200019': '/images/default/1.png',
  '200020': '/images/labs/200020.png',
  '200026': '/images/labs/200026.jpeg',
  '200027': '/images/labs/200027.png',
  '200028': '/images/labs/200028.png',
  '200029': '/images/labs/200029.png',
  '200030': '/images/labs/200030.png',
  '200031': '/images/labs/200031.png',
  '200035': '/images/labs/200035.jpeg',
  '200036': '/images/labs/200036.png',
  '200037': '/images/labs/200037.png',
  '200038': '/images/labs/200038.png',
  '200039': '/images/labs/200039.jpg',
  '200040': '/images/labs/200040.png',
  '200041': '/images/labs/200041.png',
  '200042': '/images/labs/200042.jpg',
  '200043': '/images/labs/200043.png',
  '200044': '/images/labs/200044.png',
  '200045': '/images/labs/200045.png',
}

// Processa os caminhos com o base path correto
const labLogoMap: Record<string, string> = Object.entries(labLogoMapRaw).reduce(
  (acc, [key, value]) => {
    acc[key] = resolveImagePath(value)
    return acc
  },
  {} as Record<string, string>
)

export default labLogoMap