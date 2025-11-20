

### 3. **Backend - main.py**

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import datetime

app = FastAPI(
    title="Calculadora Empresarial API",
    description="API para cálculos empresariales con historial",
    version="1.0.0"
)

class OperationType(str, Enum):
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"

class CalculationRequest(BaseModel):
    a: float
    b: float
    operation: OperationType

class CalculationResponse(BaseModel):
    result: float
    operation: str
    timestamp: str

class CalculationHistory:
    def __init__(self):
        self.history = []
    
    def add_calculation(self, calculation: CalculationResponse):
        self.history.append(calculation)
    
    def get_history(self) -> List[CalculationResponse]:
        return self.history
    
    def clear_history(self):
        self.history.clear()

history_db = CalculationHistory()

@app.post("/calculate", response_model=CalculationResponse)
async def calculate(request: CalculationRequest):
    try:
        if request.operation == OperationType.ADD:
            result = request.a + request.b
            operation_symbol = "+"
        elif request.operation == OperationType.SUBTRACT:
            result = request.a - request.b
            operation_symbol = "-"
        elif request.operation == OperationType.MULTIPLY:
            result = request.a * request.b
            operation_symbol = "×"
        elif request.operation == OperationType.DIVIDE:
            if request.b == 0:
                raise HTTPException(status_code=400, detail="No se puede dividir por cero")
            result = request.a / request.b
            operation_symbol = "÷"
        else:
            raise HTTPException(status_code=400, detail="Operación no válida")
        
        response = CalculationResponse(
            result=round(result, 6),
            operation=f"{request.a} {operation_symbol} {request.b}",
            timestamp=datetime.now().isoformat()
        )
        
        history_db.add_calculation(response)
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@app.get("/history", response_model=List[CalculationResponse])
async def get_history():
    return history_db.get_history()

@app.delete("/history")
async def clear_history():
    history_db.clear_history()
    return {"message": "Historial limpiado correctamente"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "service": "Calculadora API"
    }

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a la Calculadora Empresarial API",
        "version": "1.0.0",
        "endpoints": {
            "calculate": "POST /calculate",
            "history": "GET /history",
            "clear_history": "DELETE /history",
            "health": "GET /health"
        }
    }