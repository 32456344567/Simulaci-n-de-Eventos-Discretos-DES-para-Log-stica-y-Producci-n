# Proyecto Insignia: Simulación de Eventos Discretos (DES) para Logística y Producción

Este proyecto demuestra la aplicación de **Ingeniería de Procesos** y **Ciencia de Datos** para resolver problemas complejos de variabilidad en sistemas de manufactura. Utilizando **Python** y la librería **SimPy**, se modela una línea de producción dinámica para predecir el comportamiento del sistema bajo condiciones de incertidumbre (averías, variabilidad de procesos, rechazos de calidad).

## 🎯 Objetivo del Proyecto

Superar las limitaciones de los cálculos estáticos en Excel (promedios) mediante la simulación estocástica.

### 💡 ¿Por qué es útil este proyecto? (Valor de Negocio)
A menudo, en planta calculamos la capacidad usando promedios: *"Si la máquina hace una pieza cada 5 minutos, en una hora hago 12"*. **Esto es mentira**.
En la realidad existen:
*   **Averías (MTBF/MTTR)**: La máquina se rompe de forma aleatoria.
*   **Variabilidad Humana**: Un operario no es un robot, a veces tarda 4 min, a veces 7.
*   **Calidad**: Piezas rechazadas que consumieron tiempo pero no se venden.

Este simulador permite responder preguntas de **millones de dólares** sin gastar presupuesto real:
1.  ¿Vale la pena comprar una máquina más rápida o mejor invierto en mantenimiento para que la actual no falle tanto?
2.  ¿Qué pasa si reduzco la variabilidad del proceso (Six Sigma)?
3.  ¿Cuál es mi capacidad real comprometible para ventas?

## 🛠️ Tecnologías y Conceptos Clave

- **Lenguaje**: Python 3.x
- **Interfaz Interactiva**: `Streamlit` (Dashboard Web)
- **Librería de Simulación**: `SimPy` (Estándar para DES)
- **Análisis de Datos**: `Pandas`, `NumPy`
- **Visualización**: `Seaborn`, `Matplotlib`
- **Conceptos Lean Six Sigma**:
    - **MTBF / MTTR**: Modelado de confiabilidad de máquinas.
    - **Variabilidad**: Distribuciones normales para tiempos de proceso.
    - **Calidad**: Tasas de rechazo estocásticas.

## 📚 Fundamentos Teóricos (La Ciencia detrás del Código)

Este modelo no se basa en suposiciones aleatorias, sino en principios de **Ingeniería de Confiabilidad** e **Investigación de Operaciones**:

### 1. Modelado de Fallas (Curva de la Bañera)
Para simular las averías de las máquinas, utilizamos una **Distribución Exponencial** ($\lambda = 1/MTBF$).
*   **Por qué**: En la fase de vida útil de una máquina, las fallas ocurren de manera aleatoria e independiente del tiempo (tasa de falla constante). Es el estándar industrial para modelar eventos no planificados.
*   **Código**: `random.expovariate(1.0 / mtbf)`

### 2. Tiempos de Proceso (Teorema del Límite Central)
Para los tiempos de operación (corte, empaque), usamos una **Distribución Normal (Gaussiana)**.
*   **Por qué**: La variabilidad humana y de materiales es la suma de muchos pequeños factores independientes. Según el Teorema del Límite Central, esta suma tiende a una distribución normal.
*   **Código**: `random.gauss(mean, std)`

### 3. Lógica de Interrupción (Preemption)
Utilizamos recursos con **Preemption** (Interrupción).
*   **Por qué**: Un error común en simulaciones básicas es esperar a que la máquina termine la pieza para "fallar". En la realidad, si una banda se rompe, se detiene *durante* el proceso. Nuestro modelo captura esto, obligando a reprocesar o perder el tiempo invertido en esa pieza específica.

## 🏗️ Arquitectura del Modelo

El modelo (`src/model.py`) simula una línea de producción con las siguientes características:

1.  **Entidades**: Productos que fluyen a través del sistema.
2.  **Recursos con Preemption**: Máquinas que pueden ser interrumpidas por averías (prioridad de eventos).
3.  **Lógica de Averías**: Procesos paralelos que generan tiempos de inactividad basados en distribuciones exponenciales (MTBF/MTTR).
4.  **Control de Calidad**: Nodo de decisión probabilístico que descarta productos defectuosos.

## 📊 Escenarios Simulados

El sistema ejecuta un bucle de **Monte Carlo (1,000 iteraciones)** para cada uno de los siguientes escenarios:

1.  **Escenario Base**: Configuración actual de la planta.
2.  **Escenario A (Mejora de Capacidad)**: Aumento de velocidad en la Máquina 2 (Cuello de botella potencial).
3.  **Escenario B (Six Sigma)**: Reducción de la variabilidad en los tiempos de proceso (Estandarización).

## 📈 Resultados y Análisis

El script genera automáticamente visualizaciones para la toma de decisiones:

- **`throughput_comparison.png`**: Diagrama de caja comparando la producción total entre escenarios. Permite ver no solo el promedio, sino la dispersión (riesgo) de cada opción.
- **`availability_distribution.png`**: Gráfico de violín que muestra la densidad de probabilidad de la disponibilidad de las máquinas.
- **`simulation_summary.csv`**: Tabla resumen con estadísticas descriptivas.

### Interpretación Típica
- El **Escenario B** (Reducción de variabilidad) suele mostrar una producción más predecible (menor rango intercuartílico), lo cual es crucial para cumplir promesas de entrega (JIT).
- El **Escenario A** aumenta el promedio de producción pero puede mantener la misma volatilidad si no se atacan las causas raíz de las paradas.

## 🚀 Cómo Ejecutar el Proyecto

1.  **Clonar el repositorio**:
    ```bash
    git clone https://github.com/tu-usuario/Simulacion-DES-Logistica.git
    cd Simulacion-DES-Logistica
    ```

2.  **Instalar dependencias**:
    ```bash
    python -m pip install -r requirements.txt
    ```

3.  **Ejecutar la simulación (Modo Interactivo - Recomendado)**:
    ```bash
    py -m streamlit run dashboard.py
    ```
    Esto abrirá una página web donde puedes jugar con los parámetros (velocidad de máquinas, fallas, etc.) y ver los resultados en tiempo real.

    **Opción Clásica (Solo consola)**:
    ```bash
    py main.py
    ```

4.  **Ver resultados**:
    Revisar los gráficos interactivos en el navegador o los archivos `.png` generados si usas la consola.

---
*Este proyecto fue desarrollado como parte de un portafolio de Ingeniería de Procesos Avanzada.*
