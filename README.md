# Prueba Técnica para Backend Developer - Traiders

## Parte 1: API con FastAPI (25 puntos)
Desarrolla una API REST que incluya:

### Endpoint 1: /upload-data (POST)
- Recibe un archivo CSV con datos OHLC (Open, High, Low, Close)
- Valida que contenga las columnas: timestamp, open, high, low, close, volume
- Almacena los datos en memoria para procesamiento posterior
- Retorna confirmación de carga exitosa

### Endpoint 2: /indicators (GET)
- Calcula y retorna indicadores técnicos sobre los datos cargados:
- Media móvil simple de 5 y 20 períodos
- RSI (14 períodos)
- MACD (12, 26, 9)
- Formato de respuesta: JSON con arrays de valores

### Endpoint 3: /strategy-backtest (GET)
- Simula una estrategia básica: compra cuando MA5 > MA20, vende cuando MA5 < MA20
- Retorna métricas de rendimiento:
- Rendimiento total (%)
- Número de operaciones
- Drawdown máximo (%)
- Sharpe ratio básico

## Parte 2: Procesamiento con pandas/numpy (20 puntos)
Implementa las siguientes funciones:

```python
def validate_ohlc_data(df: pd.DataFrame) -> bool:
    """Valida estructura y calidad de datos OHLC"""
    pass

def calculate_sma(prices: pd.Series, window: int) -> pd.Series:
    """Calcula media móvil simple"""
    pass

def calculate_rsi(prices: pd.Series, window: int = 14) -> pd.Series:
    """Calcula RSI (Relative Strength Index)"""
    pass

def calculate_macd(prices: pd.Series) -> dict:
    """Calcula MACD line, signal line e histogram"""
    pass
```

## Parte 3: Simulación de Estrategia (20 puntos)
Implementa una clase que simule operaciones de trading:

```python
class TradingStrategy:
    def __init__(self, initial_capital: float = 10000):
        pass

    def execute_strategy(self, data: pd.DataFrame) -> dict:
        """Ejecuta estrategia y retorna métricas"""
        pass

    def calculate_metrics(self) -> dict:
        """Calcula drawdown, sharpe ratio, etc."""
        pass
```

## Parte 4: Extensión Opcional - Bonus (20 puntos)
- Logging estructurado de operaciones
- Manejo de errores y validaciones robustas
- Documentación automática de API con Swagger
- Tests unitarios básicos

## Entregables
- Código fuente completo con la estructura sugerida

---

## Cómo Ejecutar y Probar

Sigue estos pasos para poner en marcha la aplicación y explorar la API.

### 1. Instalación de Dependencias

Asegúrate de tener Python 3 instalado. Luego, instala las librerías necesarias desde el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 2. Ejecutar el Servidor

Una vez instaladas las dependencias, puedes iniciar la aplicación con el siguiente comando:

```bash
python3 run.py
```

El servidor se ejecutará en `http://127.0.0.1:8000` y se recargará automáticamente si detecta cambios en el código.

### 3. Explorar la Documentación de la API

Una de las grandes ventajas de FastAPI es la documentación automática e interactiva. Puedes acceder a ella a través de dos interfaces:

- **Swagger UI (Recomendado)**: Una interfaz completa donde puedes ver todos los endpoints, sus descripciones, los modelos de datos y probarlos en tiempo real.
  - **URL**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

- **ReDoc**: Una vista de documentación alternativa, más limpia y enfocada en la lectura.
  - **URL**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)