#!/bin/bash
#SBATCH --job-name=rat_neutron_analysis
#SBATCH --output=logs/analysis.out
#SBATCH --error=logs/analysis.err
#SBATCH --partition=lipq

echo "Running on host: $(hostname)"
echo "Starting Container..."

# --- Configuración de Rutas ---
SCRIPT_DIR="/lstore/sno/joankl/rat_tests/functions"
CONTAINER_SIF="/lstore/sno/joankl/RAT/containers/rat_8.1.0.sif"

# --- Comando interno del contenedor ---
# Inicializamos la cadena de entornos de SNO+ y ejecutamos el análisis
COMMAND_INSIDE="source /usr/local/bin/geant4.sh && \
                source /root-bin/bin/thisroot.sh && \
                source /rat/env.sh && \
                cd ${SCRIPT_DIR} && \
                python3 neutron_analysis.py"

# --- Ejecución de Apptainer ---
# Usamos exactamente la misma sintaxis de montajes (-B) que funciona en tu submit_job.py
apptainer exec \
    -B /share/neutrino/snoplus/ \
    -B /lstore \
    -B ${SCRIPT_DIR} \
    ${CONTAINER_SIF} \
    bash -c "${COMMAND_INSIDE}"

echo "Job finished"
