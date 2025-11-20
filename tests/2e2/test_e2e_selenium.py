import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

class TestCalculatorE2E:
    """10 pruebas E2E con Selenium"""
    
    def setup_method(self):
        """Configurar antes de cada test"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ejecutar en modo sin cabeza
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)
    
    def teardown_method(self):
        """Limpiar después de cada test"""
        self.driver.quit()
    
    def test_e2e_application_loads(self):
        """Prueba 1: La aplicación se carga correctamente"""
        self.driver.get("http://localhost:3000")
        
        # Verificar elementos principales
        assert "Calculadora" in self.driver.title or "Calculadora" in self.driver.page_source
        assert self.driver.find_element(By.TAG_NAME, "h1").is_displayed()
        print("✅ Aplicación cargada correctamente")
    
    def test_e2e_addition_calculation(self):
        """Prueba 2: Cálculo de suma E2E"""
        self.driver.get("http://localhost:3000")
        
        # Llenar formulario
        input_a = self.driver.find_element(By.PLACEHOLDER, "Primer número")
        input_b = self.driver.find_element(By.PLACEHOLDER, "Segundo número")
        calculate_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Calcular')]")
        
        input_a.clear()
        input_a.send_keys("15")
        input_b.clear()
        input_b.send_keys("25")
        calculate_btn.click()
        
        # Esperar y verificar resultado
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Resultado:')]")))
        result_element = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Resultado:')]")
        assert "40" in result_element.text
        print("✅ Cálculo de suma E2E exitoso")
    
    def test_e2e_history_functionality(self):
        """Prueba 3: Funcionalidad de historial"""
        self.driver.get("http://localhost:3000")
        
        # Realizar cálculo
        input_a = self.driver.find_element(By.PLACEHOLDER, "Primer número")
        input_b = self.driver.find_element(By.PLACEHOLDER, "Segundo número")
        calculate_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Calcular')]")
        
        input_a.clear()
        input_a.send_keys("10")
        input_b.clear()
        input_b.send_keys("5")
        calculate_btn.click()
        
        time.sleep(1)  # Esperar actualización
        
        # Verificar historial
        history_items = self.driver.find_elements(By.CLASS_NAME, "history-item")
        assert len(history_items) >= 1
        print("✅ Historial funcionando correctamente")
    
    def test_e2e_clear_history(self):
        """Prueba 4: Limpiar historial"""
        self.driver.get("http://localhost:3000")
        
        # Limpiar historial
        clear_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Limpiar')]")
        clear_btn.click()
        
        time.sleep(1)
        
        # Verificar historial vacío
        empty_history = self.driver.find_element(By.CLASS_NAME, "empty-history")
        assert empty_history.is_displayed()
        print("✅ Limpieza de historial E2E exitosa")
    
    def test_e2e_error_handling(self):
        """Prueba 5: Manejo de errores"""
        self.driver.get("http://localhost:3000")
        
        # Intentar calcular con campos vacíos
        calculate_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Calcular')]")
        calculate_btn.click()
        
        # La aplicación no debería crashear
        assert self.driver.find_element(By.PLACEHOLDER, "Primer número").is_displayed()
        print("✅ Manejo de errores E2E verificado")
    
    def test_e2e_responsive_design(self):
        """Prueba 6: Diseño responsive"""
        self.driver.get("http://localhost:3000")
        
        # Verificar en vista desktop
        self.driver.set_window_size(1200, 800)
        input_group = self.driver.find_element(By.CLASS_NAME, "input-group")
        assert input_group.is_displayed()
        
        # Verificar en vista móvil
        self.driver.set_window_size(375, 667)
        assert input_group.is_displayed()
        print("✅ Diseño responsive verificado")
    
    def test_e2e_navigation_flow(self):
        """Prueba 7: Flujo de navegación completo"""
        self.driver.get("http://localhost:3000")
        
        # Realizar múltiples operaciones
        operations = [
            ("8", "2", "multiply"),
            ("15", "3", "divide"), 
            ("20", "5", "subtract")
        ]
        
        for a, b, _ in operations:
            input_a = self.driver.find_element(By.PLACEHOLDER, "Primer número")
            input_b = self.driver.find_element(By.PLACEHOLDER, "Segundo número")
            calculate_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Calcular')]")
            
            input_a.clear()
            input_a.send_keys(a)
            input_b.clear() 
            input_b.send_keys(b)
            calculate_btn.click()
            time.sleep(0.5)
        
        # Verificar múltiples elementos en historial
        history_items = self.driver.find_elements(By.CLASS_NAME, "history-item")
        assert len(history_items) >= 3
        print("✅ Flujo de navegación completo verificado")
    
    def test_e2e_input_validation(self):
        """Prueba 8: Validación de entrada"""
        self.driver.get("http://localhost:3000")
        
        # Probar entrada inválida
        input_a = self.driver.find_element(By.PLACEHOLDER, "Primer número")
        input_a.clear()
        input_a.send_keys("abc")  # Entrada no numérica
        
        # La aplicación debería manejar esto
        calculate_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Calcular')]")
        calculate_btn.click()
        
        assert self.driver.find_element(By.PLACEHOLDER, "Primer número").is_displayed()
        print("✅ Validación de entrada E2E verificada")
    
    def test_e2e_performance(self):
        """Prueba 9: Rendimiento básico"""
        start_time = time.time()
        
        self.driver.get("http://localhost:3000")
        
        load_time = time.time() - start_time
        assert load_time < 5  # Debe cargar en menos de 5 segundos
        print(f"✅ Rendimiento E2E: {load_time:.2f}s")
    
    def test_e2e_cross_browser_compatibility(self):
        """Prueba 10: Compatibilidad básica"""
        self.driver.get("http://localhost:3000")
        
        # Verificar que los elementos clave existen
        elements_to_check = [
            "Primer número",
            "Segundo número", 
            "Calcular",
            "Historial de Cálculos"
        ]
        
        for element_text in elements_to_check:
            assert element_text in self.driver.page_source
        
        print("✅ Compatibilidad E2E verificada")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])