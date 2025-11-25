import numpy as np
import pandas as pd
from .model import run_simulation

def run_monte_carlo(base_config, num_runs=1000, scenario_name="Base"):
    results = []
    
    for i in range(num_runs):
        # We can optionally vary the seed here if needed, but SimPy/Random handles it if we don't reset
        # Ideally we might want reproducible runs, so we could set seed per run
        # random.seed(i) 
        
        res = run_simulation(base_config)
        res['scenario'] = scenario_name
        res['run_id'] = i
        results.append(res)
        
    return pd.DataFrame(results)

def run_scenarios():
    # Configuración base (Lo que creemos que pasa en la planta)
    base_config = {
        'sim_time': 480, # 8 horas de turno (en minutos)
        'arrival_interval': 5.0, # Llega materia prima cada 5 mins promedio
        'm1_mean': 4.0,
        'm1_std': 1.0,
        'm1_capacity': 1,
        'm1_mtbf': 200, # Falla cada 200 mins
        'm1_mttr': 30,  # Tardan 30 mins en arreglarla
        'rejection_rate': 0.05, # 5% de rechazo (Calidad)
        'm2_mean': 4.5, # Esta es un poco más lenta (posible cuello de botella)
        'm2_std': 1.5,
        'm2_capacity': 1,
        'm2_mtbf': 300,
        'm2_mttr': 20
    }
    
    # Escenario Base
    print("Corriendo Escenario Base (La realidad actual)...")
    df_base = run_monte_carlo(base_config, scenario_name="Base")
    
    # Escenario A: Aumentar velocidad Máquina 2 (Inversión en CAPEX)
    # Reducimos el tiempo de proceso de M2
    config_a = base_config.copy()
    config_a['m2_mean'] = 3.5 
    print("Corriendo Escenario A (Máquina 2 más rápida)...")
    df_a = run_monte_carlo(config_a, scenario_name="Scenario A")
    
    # Escenario B: Reducción de Variabilidad (Six Sigma / Lean)
    # Reducimos la desviación estándar (hacer el proceso más estable)
    config_b = base_config.copy()
    config_b['m1_std'] = 0.2
    config_b['m2_std'] = 0.2
    print("Corriendo Escenario B (Six Sigma - Baja Variabilidad)...")
    df_b = run_monte_carlo(config_b, scenario_name="Scenario B")
    
    # Juntamos todo para analizar
    final_df = pd.concat([df_base, df_a, df_b], ignore_index=True)
    return final_df
