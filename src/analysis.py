import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def analyze_results(df):
    """Genera los gráficos y estadísticas para ver quién gana."""
    
    # Estilo visual
    sns.set(style="whitegrid")
    
    # 1. Comparación de Throughput (Boxplot)
    # Aquí vemos la "caja" de resultados. Si la caja es muy grande, es que el proceso es un caos.
    plt.figure(figsize=(10, 6))
    sns.boxplot(x="scenario", y="throughput", hue="scenario", data=df, palette="Set2", legend=False)
    plt.title("Comparación de Throughput (Producción Total) por Escenario")
    plt.ylabel("Unidades Producidas (8 horas)")
    plt.xlabel("Escenario")
    plt.savefig("throughput_comparison.png")
    plt.close()
    
    # 2. Distribución de Disponibilidad (Violin Plot)
    # Muestra qué tan seguido las máquinas estuvieron funcionando vs. rotas.
    plt.figure(figsize=(10, 6))
    sns.violinplot(x="scenario", y="m1_availability", hue="scenario", data=df, palette="muted", legend=False)
    plt.title("Distribución de Disponibilidad de Máquina 1")
    plt.ylabel("Disponibilidad (%)")
    plt.savefig("availability_distribution.png")
    plt.close()
    
    # Tabla Resumen
    summary = df.groupby("scenario")[["throughput", "rejected", "m1_availability"]].describe()
    summary.to_csv("simulation_summary.csv")
    
    print("Análisis completo. Revisa los PNGs generados.")
    print("Resumen guardado en 'simulation_summary.csv'.")
    
    return summary
