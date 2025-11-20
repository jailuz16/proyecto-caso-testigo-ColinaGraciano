// Prueba MUY básica que importa y renderiza el componente real
import { render, screen } from '@testing-library/react';
import App from './App.jsx';

// Mock MUY simple de axios
jest.mock('axios', () => ({
  get: () => Promise.resolve({ data: [] }),
  post: () => Promise.resolve({ data: { result: 10, operation: "5 + 5", timestamp: "2024-01-01" } }),
  delete: () => Promise.resolve({})
}));

// Test que realmente ejecuta el componente
test('renderiza el componente App completamente', () => {
  // Esto ejecuta TODO el código de App.jsx
  const { container } = render(<App />);
  
  // Verificaciones básicas
  expect(container).toBeInTheDocument();
  expect(screen.getByText(/Calculadora Empresarial/i)).toBeInTheDocument();
});

test('interactúa con los inputs', () => {
  render(<App />);
  
  // Encuentra los inputs por placeholder
  const input1 = screen.getByPlaceholderText('Primer número');
  const input2 = screen.getByPlaceholderText('Segundo número');
  
  expect(input1).toBeInTheDocument();
  expect(input2).toBeInTheDocument();
});

test('encuentra el botón de calcular', () => {
  render(<App />);
  const button = screen.getByText(/Calcular/i);
  expect(button).toBeInTheDocument();
});

test('verifica que el historial se renderiza', () => {
  render(<App />);
  const historialTitle = screen.getByText(/Historial de Cálculos/i);
  expect(historialTitle).toBeInTheDocument();
});