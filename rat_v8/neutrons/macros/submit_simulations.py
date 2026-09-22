'''
Python script designed to run multiple jobs of RAT simualtions.
It will read a MACRO_TEMPLATE on which simulations will be based.
The simualtions will be executed within the Apptained container of RAT (CONTAINER_SIF).
It will create N_JOBS simulations, and their respective output.root files.

Created on 22/09/2026
'''

import os
import time

N_JOBS = 10                 # Nº of jobs to send to the Farm
EVENTS_PER_JOB = 1000       # Nº of events per job (Total events = N_JOBS * EVENTS_PER_JOB)
ENERGY = "3MeV"             # Files label (energy of simulation)

# Main working directory
BASE_DIR = "/lstore/sno/joankl/rat_tests/rat_v8/neutrons/"

MACRO_TEMPLATE = BASE_DIR + 'macros/neutron_validation.mac'
CONTAINER_SIF = "/lstore/sno/joankl/RAT/containers/rat_8.1.0.sif"

# Output directories (automatic creation)
OUTPUT_ROOT_DIR = os.path.join(BASE_DIR, "results", "root_files")
JOBS_DIR = os.path.join(BASE_DIR, "jobs")
LOGS_DIR = os.path.join(JOBS_DIR, "logs")

os.makedirs(OUTPUT_ROOT_DIR, exist_ok=True)
os.makedirs(JOBS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

if __name__ == "__main__":
    
    # 1. Read the macro template
    with open(MACRO_TEMPLATE, 'r') as f:
        macro_lines = f.readlines()

    print(f"Preparing to send {N_JOBS} jobs to SLURM...")

    # 2. Iteration of jobs
    for i in range(N_JOBS):
        job_name = f"RAT8_neutron_{i}"
        out_root = os.path.join(OUTPUT_ROOT_DIR, f"neutron_{ENERGY}_{i}.root")
        out_mac = os.path.join(JOBS_DIR, f"macro_{job_name}.mac")
        sh_file = os.path.join(JOBS_DIR, f"submit_{job_name}.sh")

        # --- A. Creating uniquemacro for this Job ---
        with open(out_mac, 'w') as f:
            for line in macro_lines:
                # Replace the output file to avoid overwritte the macro template
                if "/rat/procset file" in line:
                    f.write(f'/rat/procset file "{out_root}"\n')
                # Replace the Nº of events
                elif "/rat/run/start" in line:
                    f.write(f'/rat/run/start {EVENTS_PER_JOB}\n')
                else:
                    f.write(line)

        # --- B. Command in Container ---
        command_inside = (
            "source /usr/local/bin/geant4.sh && "
            "source /root-bin/bin/thisroot.sh && "
            "source /rat/env.sh && "
            f"rat {out_mac}"
        )

        # --- C. Create the sh script for SLURM ---
        slurm_script = f"""#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --output={LOGS_DIR}/{job_name}.out
#SBATCH --error={LOGS_DIR}/{job_name}.err
#SBATCH --partition=lipq

# Execute Apptainer
apptainer exec \\
    -B /lstore/sno/joankl \\
    {CONTAINER_SIF} \\
    bash -c "{command_inside}"
"""
        with open(sh_file, 'w') as f:
            f.write(slurm_script)

        # --- D. Send Job to SLURM ---
        print(f"Sending {job_name} ...")
        os.system(f"sbatch {sh_file}")
        
        # Pausa de 0.5s para no saturar al gestor de colas del servidor
        time.sleep(0.5)

    print(f"\n¡{N_JOBS} jobs running succesfully!")
    print(f"Files ROOT to be saved in: {OUTPUT_ROOT_DIR}")
