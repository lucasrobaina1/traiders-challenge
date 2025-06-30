# Prueba Técnica para Backend Developer - Traiders

## Enunciado de la Prueba

### Empresa: Traiders (Fintech - Trading & Análisis de Mercados)
### Puesto: Backend Developer
### Tiempo máximo: 60 minutos
### Modalidad: Código ejecutable localmente (sin despliegue)

## Contexto
Traiders es una startup fintech especializada en trading automático y análisis de carteras. Necesitamos evaluar tus habilidades prácticas para desarrollar APIs que procesen datos financieros y simulen estrategias de trading.

## Stack Técnico Requerido
- FastAPI para APIs REST
- pandas/numpy para procesamiento de datos financieros
- Consultas de base de datos
- Conocimientos básicos de indicadores técnicos y métricas financieras

## Objetivos de la Evaluación
Esta prueba evalúa tu capacidad real para:
- Desarrollar APIs REST con FastAPI - Estructura profesional y manejo de datos
- Procesar datos financieros - Análisis de series temporales OHLC y validación
- Calcular indicadores técnicos - RSI, MACD, medias móviles
- Implementar estrategias de trading - Simulación de operaciones y backtesting
- Aplicar métricas financieras - Sharpe ratio, drawdown, rendimientos
- Estructurar código profesional - Organización de proyecto Python

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