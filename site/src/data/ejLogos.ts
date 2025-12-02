function resolveImagePath(path: string): string {
  const base = import.meta.env.BASE_URL || '/'
  return base.endsWith('/') ? `${base}${path.slice(1)}` : `${base}${path}`
}

const ejLogoMapRaw: Record<string, string> = {
  '100001': '/images/ejs/100001.png',
  '100002': '/images/ejs/100002.jpeg',
  '100003': '/images/ejs/100003.jpeg',
  '100004': '/images/ejs/100004.jpeg',
  '100005': '/images/ejs/100005.png',
  '100006': '/images/ejs/100006.jpeg',
  '100007': '/images/ejs/100007.jpeg',
  '100008': '/images/ejs/100008.jpeg',
  '100009': '/images/ejs/100009.jpeg',
  '100010': '/images/ejs/100010.jpeg',
  '100011': '/images/ejs/100011.jpeg',
  '100012': '/images/ejs/100012.png',
  '100013': '/images/ejs/100013.png',
  '100014': '/images/ejs/100014.jpeg',
  '100015': '/images/ejs/100015.jpeg',
  '100016': '/images/ejs/100016.jpeg',
  '100017': '/images/ejs/100017.png',
  '100018': '/images/ejs/100018.jpeg',
  '100019': '/images/ejs/100019.jpeg',
  '100020': '/images/ejs/100020.jpeg',
  '100021': '/images/ejs/100021.jpeg',
  '100022': '/images/ejs/100022.jpeg',
  '100023': '/images/ejs/100023.png',
  '100024': '/images/ejs/100024.png',
  '100025': '/images/ejs/100025.jpeg',
  '100026': '/images/ejs/100026.jpeg',
  '100027': '/images/ejs/100027.jpeg',
  '100028': '/images/ejs/100028.jpeg',
  '100029': '/images/ejs/100029.jpeg',
  '100030': '/images/ejs/100030.jpeg',
  '100031': '/images/ejs/100031.jpeg',
  '100032': '/images/ejs/100032.jpeg',
  '100033': '/images/ejs/100033.jpeg',
  '100034': '/images/ejs/100034.png',
  '100035': '/images/ejs/100035.jpeg',
  '100036': '/images/ejs/100036.jpeg',
  '100037': '/images/ejs/100037.jpeg',
  '100038': '/images/ejs/100038.jpeg',
  '100039': '/images/ejs/100039.jpeg',
  '100040': '/images/ejs/100040.jpeg',
  '100041': '/images/ejs/100041.png',
  '100042': '/images/ejs/100042.jpeg',
  '100043': '/images/ejs/100043.png',
  '100044': '/images/ejs/100044.jpeg',
  '100045': '/images/ejs/100045.jpeg',
  '100046': '/images/ejs/100046.png',
  '100047': '/images/ejs/100047.jpeg',
  '100048': '/images/ejs/100048.jpeg',
  '100049': '/images/ejs/100049.jpeg',
  '100050': '/images/ejs/100050.png',
}

const ejLogoMap: Record<string, string> = Object.entries(ejLogoMapRaw).reduce(
  (acc, [key, value]) => {
    acc[key] = resolveImagePath(value)
    return acc
  },
  {} as Record<string, string>
)

export default ejLogoMap
