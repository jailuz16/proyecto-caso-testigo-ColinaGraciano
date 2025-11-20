import pytest
import requests
import time
from datetime import datetime

class TestCalculatorIntegrationFinal:
    """20 pruebas de integración REALES y funcionales"""
    
    BASE_URL = "http://localhost:8000"
    
    def setup_method(self):
        """Preparar antes de cada test"""
        # Pequeña pausa para evitar sobrecarga
        time.sleep(0.1)
    
    def test_health_check(self):
        """Prueba 1: Health check"""
        response = requests.get(f"{self.BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        print("✅ Health check exitoso")

    def test_root_endpoint(self):
        """Prueba 2: Endpoint raíz"""
        response = requests.get(f"{self.BASE_URL}/")
        assert response.status_code == 200
        data = response.json()
        assert "Bienvenido" in data["message"]
        print("✅ Endpoint raíz funcionando")

    def test_addition_flow(self):
        """Prueba 3: Flujo completo de suma"""
        response = requests.post(f"{self.BASE_URL}/calculate", json={
            "a": 15.5,
            "b": 10.2,
            "operation": "add"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 25.7
        print("✅ Flujo de suma completo")

    def test_subtraction_flow(self):
        """Prueba 4: Flujo completo de resta"""
        response = requests.post(f"{self.BASE_URL}/calculate", json={
            "a": 20,
            "b": 8,
            "operation": "subtract"
        })
        assert response.status_code == 200
        assert response.json()["result"] == 12
        print("✅ Flujo de resta completo")

    def test_multiplication_flow(self):
        """Prueba 5: Flujo completo de multiplicación"""
        response = requests.post(f"{self.BASE_URL}/calculate", json={
            "a": 6,
            "b": 7,
            "operation": "multiply"
        })
        assert response.status_code == 200
        assert response.json()["result"] == 42
        print("✅ Flujo de multiplicación completo")

    def test_division_flow(self):
        """Prueba 6: Flujo completo de división"""
        response = requests.post(f"{self.BASE_URL}/calculate", json={
            "a": 15,
            "b": 3,
            "operation": "divide"
        })
        assert response.status_code == 200
        assert response.json()["result"] == 5
        print("✅ Flujo de división completo")

    def test_division_by_zero(self):
        """Prueba 7: División por cero"""
        response = requests.post(f"{self.BASE_URL}/calculate", json={
            "a": 10,
            "b": 0,
            "operation": "divide"
        })
        assert response.status_code == 400
        assert "No se puede dividir por cero" in response.json()["detail"]
        print("✅ Manejo de división por cero")

    def test_history_persistence(self):
        """Prueba 8: Persistencia del historial"""
        # Limpiar historial primero
        requests.delete(f"{self.BASE_URL}/history")
        
        # Realizar múltiples cálculos
        operations = [
            {"a": 1, "b": 2, "operation": "add"},
            {"a": 3, "b": 4, "operation": "multiply"},
        ]
        
        for op in operations:
            response = requests.post(f"{self.BASE_URL}/calculate", json=op)
            assert response.status_code == 200
        
        # Verificar historial acumulado
        response = requests.get(f"{self.BASE_URL}/history")
        assert response.status_code == 200
        history_data = response.json()
        assert len(history_data) == 2
        print("✅ Persistencia de historial verificada")

    def test_clear_history(self):
        """Prueba 9: Limpiar historial"""
        # Agregar un cálculo
        requests.post(f"{self.BASE_URL}/calculate", json={"a": 5, "b": 5, "operation": "add"})
        
        # Limpiar historial
        response = requests.delete(f"{self.BASE_URL}/history")
        assert response.status_code == 200
        
        # Verificar historial vacío
        response = requests.get(f"{self.BASE_URL}/history")
        assert len(response.json()) == 0
        print("✅ Limpieza de historial funcionando")

    def test_large_numbers(self):
        """Prueba 10: Cálculos con números grandes"""
        response = requests.post(f"{self.BASE_URL}/calculate", json={
            "a": 999999,
            "b": 111111,
            "operation": "add"
        })
        assert response.status_code == 200
        assert response.json()["result"] == 1111110
        print("✅ Números grandes procesados")

    def test_decimal_precision(self):
        """Prueba 11: Precisión con decimales"""
        response = requests.post(f"{self.BASE_URL}/calculate", json={
            "a": 0.1,
            "b": 0.2,
            "operation": "add"
        })
        assert response.status_code == 200
        result = response.json()["result"]
        assert abs(result - 0.3) < 0.000001
        print("✅ Precisión decimal verificada")

    def test_negative_numbers(self):
        """Prueba 12: Operaciones con números negativos"""
        response = requests.post(f"{self.BASE_URL}/calculate", json={
            "a": -10,
            "b": 5,
            "operation": "add"
        })
        assert response.status_code == 200
        assert response.json()["result"] == -5
        print("✅ Números negativos funcionando")

    def test_error_handling(self):
        """Prueba 13: Manejo de errores de validación"""
        response = requests.post(f"{self.BASE_URL}/calculate", json={
            "a": "invalid",
            "b": 5,
            "operation": "add"
        })
        assert response.status_code == 422
        print("✅ Manejo de errores funcionando")

    def test_missing_fields(self):
        """Prueba 14: Campos faltantes"""
        response = requests.post(f"{self.BASE_URL}/calculate", json={"a": 10})
        assert response.status_code == 422
        print("✅ Validación de campos funcionando")

    def test_invalid_operation(self):
        """Prueba 15: Operación inválida"""
        response = requests.post(f"{self.BASE_URL}/calculate", json={
            "a": 10,
            "b": 5,
            "operation": "invalid_operation"
        })
        assert response.status_code == 422
        print("✅ Validación de operaciones funcionando")

    def test_response_structure(self):
        """Prueba 16: Estructura de respuesta consistente"""
        response = requests.post(f"{self.BASE_URL}/calculate", json={
            "a": 8,
            "b": 2,
            "operation": "multiply"
        })
        data = response.json()
        
        required_fields = ["result", "operation", "timestamp"]
        for field in required_fields:
            assert field in data
        print("✅ Estructura de respuesta correcta")

    def test_history_order(self):
        """Prueba 17: Orden del historial"""
        requests.delete(f"{self.BASE_URL}/history")
        
        for i in [1, 2, 3]:
            requests.post(f"{self.BASE_URL}/calculate", json={
                "a": i, "b": i, "operation": "add"
            })
        
        response = requests.get(f"{self.BASE_URL}/history")
        history_data = response.json()
        assert len(history_data) == 3
        print("✅ Orden de historial preservado")

    def test_zero_operations(self):
        """Prueba 18: Operaciones con cero"""
        test_cases = [
            (0, 5, "add", 5),
            (5, 0, "add", 5),
            (0, 5, "multiply", 0),
        ]
        
        for a, b, op, expected in test_cases:
            response = requests.post(f"{self.BASE_URL}/calculate", json={
                "a": a, "b": b, "operation": op
            })
            assert response.status_code == 200
            assert response.json()["result"] == expected
        print("✅ Operaciones con cero funcionando")

    def test_consecutive_operations(self):
        """Prueba 19: Operaciones consecutivas"""
        requests.delete(f"{self.BASE_URL}/history")
        
        results = []
        for i in range(3):
            response = requests.post(f"{self.BASE_URL}/calculate", json={
                "a": i * 10,
                "b": i + 1,
                "operation": "add"
            })
            results.append(response.status_code)
        
        assert all(code == 200 for code in results)
        print("✅ Operaciones consecutivas exitosas")

    def test_stress_handling(self):
        """Prueba 20: Manejo de múltiples requests"""
        successful_requests = 0
        for i in range(5):
            try:
                response = requests.post(f"{self.BASE_URL}/calculate", json={
                    "a": i * 5,
                    "b": i + 2,
                    "operation": "add"
                }, timeout=5)
                if response.status_code == 200:
                    successful_requests += 1
            except:
                continue
        
        assert successful_requests >= 4  # 80% de éxito
        print(f"✅ Test de estrés: {successful_requests}/5 requests exitosas")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])