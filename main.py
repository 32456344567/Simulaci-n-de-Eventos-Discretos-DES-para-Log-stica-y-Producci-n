from src.simulation import run_scenarios
from src.analysis import analyze_results

def main():
    print("Starting Discrete Event Simulation Project...")
    print("Simulating Logistics and Production Line with SimPy")
    print("--------------------------------------------------")
    
    # Run Simulations
    results_df = run_scenarios()
    
    # Analyze Results
    print("\nAnalyzing Results...")
    summary = analyze_results(results_df)
    
    print("\nSimulation Finished Successfully.")
    print(summary)

if __name__ == "__main__":
    main()
