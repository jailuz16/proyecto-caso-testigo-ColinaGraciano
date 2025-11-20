import React, { useState } from 'react'
import './App.css'

function App() {
  const [a, setA] = useState('')
  const [b, setB] = useState('')
  const [result, setResult] = useState('')

  const calculate = () => {
    if (a && b) {
      setResult(`Resultado: ${parseFloat(a) + parseFloat(b)}`)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🧮 Calculadora Empresarial</h1>
        <p>Sistema de cálculos con historial integrado</p>
      </header>

      <div className="calculator">
        <div className="input-group">
          <input
            type="number"
            value={a}
            onChange={(e) => setA(e.target.value)}
            placeholder="Primer número"
            className="number-input"
          />
          
          <span>+</span>

          <input
            type="number"
            value={b}
            onChange={(e) => setB(e.target.value)}
            placeholder="Segundo número"
            className="number-input"
          />
        </div>

        <button onClick={calculate} className="calculate-btn">
          🚀 Calcular
        </button>

        {result && (
          <div className="result">
            <h3>{result}</h3>
          </div>
        )}
      </div>
    </div>
  )
}

export default App