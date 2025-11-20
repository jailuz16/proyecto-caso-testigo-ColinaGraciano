import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestCalculatorAPI:
    """Suite de pruebas para la API de la calculadora"""
    
    def setup_method(self):
        """Limpiar historial antes de cada prueba"""
        client.delete("/history")

    def test_add_operation(self):
        """Prueba operación de suma"""
        response = client.post("/calculate", json={
            "a": 10.5,
            "b": 5.2,
            "operation": "add"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 15.7
        assert "10.5 + 5.2" in data["operation"]

    def test_subtract_operation(self):
        """Prueba operación de resta"""
        response = client.post("/calculate", json={
            "a": 15,
            "b": 7,
            "operation": "subtract"
        })
        assert response.status_code == 200
        assert response.json()["result"] == 8

    def test_multiply_operation(self):
        """Prueba operación de multiplicación"""
        response = client.post("/calculate", json={
            "a": 6,
            "b": 7,
            "operation": "multiply"
        })
        assert response.status_code == 200
        assert response.json()["result"] == 42

    def test_divide_operation(self):
        """Prueba operación de división"""
        response = client.post("/calculate", json={
            "a": 20,
            "b": 4,
            "operation": "divide"
        })
        assert response.status_code == 200
        assert response.json()["result"] == 5

    def test_divide_by_zero(self):
        """Prueba división por cero"""
        response = client.post("/calculate", json={
            "a": 10,
            "b": 0,
            "operation": "divide"
        })
        assert response.status_code == 400
        assert "No se puede dividir por cero" in response.json()["detail"]

    def test_invalid_operation(self):
        """Prueba operación inválida"""
        response = client.post("/calculate", json={
            "a": 10,
            "b": 5,
            "operation": "invalid_operation"
        })
        assert response.status_code == 422

    def test_history_management(self):
        """Prueba gestión del historial"""
        # Realizar cálculos
        client.post("/calculate", json={"a": 1, "b": 2, "operation": "add"})
        client.post("/calculate", json={"a": 3, "b": 4, "operation": "multiply"})
        
        # Verificar historial
        response = client.get("/history")
        assert response.status_code == 200
        history = response.json()
        assert len(history) == 2
        
        # Limpiar historial
        clear_response = client.delete("/history")
        assert clear_response.status_code == 200
        
        # Verificar historial vacío
        history_response = client.get("/history")
        assert len(history_response.json()) == 0

    def test_health_check(self):
        """Prueba endpoint de health check"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data

    def test_root_endpoint(self):
        """Prueba endpoint raíz"""
        response = client.get("/")
        assert response.status_code == 200
        assert "Bienvenido" in response.json()["message"]

class TestInputValidation:
    """Pruebas de validación de entrada"""
    
    def test_missing_fields(self):
        """Prueba campos faltantes"""
        response = client.post("/calculate", json={"a": 10})
        assert response.status_code == 422

    def test_invalid_number_format(self):
        """Prueba formato de número inválido"""
        response = client.post("/calculate", json={
            "a": "not_a_number",
            "b": 5,
            "operation": "add"
        })
        assert response.status_code == 422

    def test_negative_numbers(self):
        """Prueba con números negativos"""
        response = client.post("/calculate", json={
            "a": -10,
            "b": 5,
            "operation": "add"
        })
        assert response.status_code == 200
        assert response.json()["result"] == -5

if __name__ == "__main__":
    pytest.main([__file__, "-v"])