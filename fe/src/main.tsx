import { createRoot } from 'react-dom/client'
import './globals.css'
import { BrowserRouter } from 'react-router-dom'
import App from './App.tsx'

// biome-ignore lint/style/noNonNullAssertion: Default value by react team
createRoot(document.getElementById('root')!).render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
)
