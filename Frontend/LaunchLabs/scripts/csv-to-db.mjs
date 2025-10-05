import fs from 'fs'
import path from 'path'
import Papa from 'papaparse'

const inputPath = process.argv[2]
if (!inputPath) {
  console.error('Uso: npm run import-csv -- <ruta CSV>  (o edita el script con la ruta por defecto)')
  process.exit(1)
}

// Lee CSV como texto
const csv = fs.readFileSync(inputPath, 'utf8')

// Parseo robusto (maneja comillas y comas internas)
const parsed = Papa.parse(csv, { header: true, skipEmptyLines: true })
if (parsed.errors && parsed.errors.length) {
  console.error('Errores al parsear CSV:', parsed.errors.slice(0, 3))
}

// Normaliza claves para evitar espacios y caracteres raros
const normalizeKey = (k) => String(k || '')
  .trim()
  .replaceAll('\u00A0', ' ')
  .replace(/\s+/g, ' ')

// Mapea columnas del csv de NASA TechPort a un esquema más usable
const projects = parsed.data.map((row, idx) => {
  const r = {}
  for (const [k, v] of Object.entries(row)) {
    r[normalizeKey(k)] = typeof v === 'string' ? v.trim() : v
  }

  return {
    id: Number(r['TechPort ID']) || idx + 1,
    title: r['Project Title'] || '',
    description: r['Project Description'] || '',
    program: r['Responsible NASA Program'] || '',
    taxonomy: r['Primary Taxonomy'] || '',
    lastUpdated: r['Project Last Updated'] || '',
    url: r['Project URL'] || '',
    apiUrl: r['Project API URL'] || ''
  }
}).filter(p => p.title)

const out = { projects }
const outPath = path.resolve(process.cwd(), 'db.json')
fs.writeFileSync(outPath, JSON.stringify(out, null, 2), 'utf8')
console.log(`db.json generado con ${projects.length} proyectos -> ${outPath}`)

// También generar un archivo estático para despliegue (Netlify, etc.)
try {
  const publicDir = path.resolve(process.cwd(), 'public')
  if (!fs.existsSync(publicDir)) fs.mkdirSync(publicDir)
  const staticPath = path.join(publicDir, 'projects.json')
  // Guardar solo el array para consumo directo en el frontend
  fs.writeFileSync(staticPath, JSON.stringify(projects, null, 2), 'utf8')
  console.log(`projects.json estático generado -> ${staticPath}`)
} catch (e) {
  console.warn('No se pudo escribir public/projects.json:', e?.message || e)
}




