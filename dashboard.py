import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.simulation import run_monte_carlo

# Configuración de la página
st.set_page_config(page_title="Simulador de Producción DES", layout="wide")

st.title("🏭 Simulador de Eventos Discretos: Logística y Producción")
st.markdown("""
Esta herramienta permite modelar el comportamiento de una línea de producción bajo condiciones de variabilidad.
A diferencia de un Excel estático, aquí simulamos miles de días de operación para ver el impacto real de las averías y la calidad.
""")

# Sidebar para parámetros
st.sidebar.header("⚙️ Configuración de la Planta")

st.sidebar.subheader("Máquina 1 (Proceso Inicial)")
m1_mean = st.sidebar.slider("Tiempo Promedio de Proceso (min)", 1.0, 10.0, 4.0)
m1_std = st.sidebar.slider("Variabilidad (Desviación Std)", 0.1, 3.0, 1.0)
m1_mtbf = st.sidebar.number_input("Tiempo Entre Fallas (MTBF - min)", value=200)
m1_mttr = st.sidebar.number_input("Tiempo de Reparación (MTTR - min)", value=30)

st.sidebar.subheader("Control de Calidad")
rejection_rate = st.sidebar.slider("Tasa de Rechazo (%)", 0.0, 20.0, 5.0) / 100.0

st.sidebar.subheader("Máquina 2 (Proceso Final)")
m2_mean = st.sidebar.slider("Tiempo Promedio M2 (min)", 1.0, 10.0, 4.5)
m2_std = st.sidebar.slider("Variabilidad M2", 0.1, 3.0, 1.5)
m2_mtbf = st.sidebar.number_input("MTBF M2 (min)", value=300)
m2_mttr = st.sidebar.number_input("MTTR M2 (min)", value=20)

st.sidebar.subheader("Simulación")
sim_days = st.sidebar.slider("Días a Simular (Iteraciones)", 10, 1000, 200)

# Botón para ejecutar
if st.button("🚀 Correr Simulación"):
    with st.spinner('Simulando operaciones...'):
        # Configuración dinámica
        config = {
            'sim_time': 480, # 8 horas
            'arrival_interval': 5.0,
            'm1_mean': m1_mean,
            'm1_std': m1_std,
            'm1_capacity': 1,
            'm1_mtbf': m1_mtbf,
            'm1_mttr': m1_mttr,
            'rejection_rate': rejection_rate,
            'm2_mean': m2_mean,
            'm2_std': m2_std,
            'm2_capacity': 1,
            'm2_mtbf': m2_mtbf,
            'm2_mttr': m2_mttr
        }
        
        # Corremos la simulación (usamos la función existente)
        # Para comparar, creamos un escenario "Optimizado" automático (ej. reduciendo variabilidad)
        df_base = run_monte_carlo(config, num_runs=sim_days, scenario_name="Configuración Actual")
        
        # Escenario Comparativo: Reducción de variabilidad (Six Sigma)
        config_opt = config.copy()
        config_opt['m1_std'] = m1_std * 0.5
        config_opt['m2_std'] = m2_std * 0.5
        df_opt = run_monte_carlo(config_opt, num_runs=sim_days, scenario_name="Escenario Six Sigma (Baja Var.)")
        
        df_final = pd.concat([df_base, df_opt])
        
        # --- Resultados ---
        st.success("¡Simulación Completada!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Producción Diaria (Throughput)")
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.boxplot(x="scenario", y="throughput", hue="scenario", data=df_final, palette="Set2", ax=ax, legend=False)
            ax.set_title("Comparación de Producción")
            ax.set_ylabel("Unidades por Turno (8h)")
            st.pyplot(fig)
            
        with col2:
            st.subheader("📉 Disponibilidad de Máquina 1")
            fig2, ax2 = plt.subplots(figsize=(8, 5))
            sns.violinplot(x="scenario", y="m1_availability", hue="scenario", data=df_final, palette="muted", ax=ax2, legend=False)
            ax2.set_title("Impacto de las Averías")
            ax2.set_ylabel("Disponibilidad (%)")
            st.pyplot(fig2)
            
        # Estadísticas Clave
        st.subheader("Resumen Ejecutivo")
        summary = df_final.groupby("scenario")[["throughput", "rejected", "m1_availability"]].mean()
        st.dataframe(summary.style.format("{:.2f}"))
        
        st.markdown("### 💡 Interpretación")
        base_prod = summary.loc["Configuración Actual", "throughput"]
        opt_prod = summary.loc["Escenario Six Sigma (Baja Var.)", "throughput"]
        diff = opt_prod - base_prod
        
        if diff > 1:
            st.info(f"Al reducir la variabilidad, podrías ganar **{diff:.1f} unidades extra** por turno en promedio, sin comprar máquinas nuevas.")
        else:
            st.warning("La reducción de variabilidad no impactó mucho el promedio. Revisa si el cuello de botella son las averías (MTBF) y no la velocidad.")

