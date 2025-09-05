import React from 'react'
import { createRoot } from 'react-dom/client'

function App() {
  return (
    <div style={{ padding: 16, fontFamily: 'system-ui, sans-serif' }}>
      <h1>Imobiliária</h1>
      <p>Frontend iniciado. API em {import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}</p>
    </div>
  )
}

const container = document.getElementById('root')!
createRoot(container).render(<App />)

