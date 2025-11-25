import simpy
import random
import numpy as np

class ProductionSystem:
    def __init__(self, env, config):
        self.env = env
        self.config = config
        
        # Resources with Preemption to allow breakdowns to interrupt work
        self.machine_1 = simpy.PreemptiveResource(env, capacity=config.get('m1_capacity', 1))
        self.machine_2 = simpy.PreemptiveResource(env, capacity=config.get('m2_capacity', 1))
        
        # Buffer (Container) between machines if needed, or just infinite queue
        # For this demo, we assume direct flow but we track queue times implicitly via resource wait
        
        # Metrics
        self.total_production = 0
        self.total_rejected = 0
        self.m1_downtime = 0
        self.m2_downtime = 0
        
        # Start breakdown processes
        if config.get('m1_mtbf') > 0:
            self.env.process(self.breakdown_process(self.machine_1, 'm1'))
        if config.get('m2_mtbf') > 0:
            self.env.process(self.breakdown_process(self.machine_2, 'm2'))

    def process_entity(self, entity_id):
        """Lifecycle of a product through the line."""
        arrival_time = self.env.now
        
        # --- Stage 1: Machine 1 ---
        # Processing logic with preemption handling
        proc_time_m1 = max(0.1, random.gauss(self.config['m1_mean'], self.config['m1_std']))
        remaining_time = proc_time_m1
        
        while remaining_time > 0:
            with self.machine_1.request(priority=1) as req:
                yield req
                start_time = self.env.now
                try:
                    yield self.env.timeout(remaining_time)
                    remaining_time = 0 # Finished
                except simpy.Interrupt:
                    # We were interrupted (breakdown). 
                    # Calculate how much work was done before interruption
                    worked = self.env.now - start_time
                    remaining_time -= worked
                    # The breakdown process holds the resource now.
                    # We loop back and wait for the resource again.

        # --- Quality Check ---
        if random.random() < self.config['rejection_rate']:
            self.total_rejected += 1
            return # Scrapped

        # --- Stage 2: Machine 2 ---
        proc_time_m2 = max(0.1, random.gauss(self.config['m2_mean'], self.config['m2_std']))
        remaining_time = proc_time_m2
        
        while remaining_time > 0:
            with self.machine_2.request(priority=1) as req:
                yield req
                start_time = self.env.now
                try:
                    yield self.env.timeout(remaining_time)
                    remaining_time = 0
                except simpy.Interrupt:
                    worked = self.env.now - start_time
                    remaining_time -= worked
            
        self.total_production += 1

    def breakdown_process(self, resource, machine_prefix):
        """Simula las fallas aleatorias de la máquina (La pesadilla del jefe de planta)."""
        while True:
            mtbf = self.config[f'{machine_prefix}_mtbf']
            mttr = self.config[f'{machine_prefix}_mttr']
            
            # Esperamos hasta que la máquina decida fallar (distribución exponencial)
            time_to_fail = random.expovariate(1.0 / mtbf)
            yield self.env.timeout(time_to_fail)
            
            # ¡Falla! Detenemos todo.
            # Pedimos el recurso con prioridad máxima (0) y preempt=True para echar a cualquier producto que se esté procesando
            with resource.request(priority=0, preempt=True) as req:
                yield req
                # Tiempo que tarda mantenimiento en arreglarla
                repair_time = random.expovariate(1.0 / mttr)
                
                if machine_prefix == 'm1':
                    self.m1_downtime += repair_time
                else:
                    self.m2_downtime += repair_time
                    
                yield self.env.timeout(repair_time)

def run_simulation(config):
    """Runs a single simulation replication."""
    env = simpy.Environment()
    system = ProductionSystem(env, config)
    
    def generator():
        i = 0
        while True:
            yield env.timeout(random.expovariate(1.0 / config['arrival_interval']))
            env.process(system.process_entity(i))
            i += 1
            
    env.process(generator())
    env.run(until=config['sim_time'])
    
    # Calculate OEE-like metrics (Simplified)
    # Availability = (Total Time - Downtime) / Total Time
    m1_availability = (config['sim_time'] - system.m1_downtime) / config['sim_time']
    throughput = system.total_production
    
    return {
        'throughput': throughput,
        'rejected': system.total_rejected,
        'm1_availability': m1_availability,
        'm1_downtime': system.m1_downtime
    }
