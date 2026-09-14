#!/bin/bash
#BATCH --job-name=RAT_neutron_simulation      
#SBATCH --output=logs/simu.out  
#SBATCH --error=logs/simu.err   
#SBATCH --partition=lipq               # Partición estándar

echo "Running on host: $(hostname)"
echo "Starting Apptainer Container for RAT Simulation..."

# --- Configuración de Rutas ---
MACRO_DIR="/lstore/sno/joankl/rat_tests/rat_v8/neutrons/macros"
CONTAINER_SIF="/lstore/sno/joankl/RAT/containers/rat_8.1.0.sif"

# --- Comandos a ejecutar DENTRO del contenedor ---
# Cargamos el entorno nativo de RAT dentro de la imagen, nos movemos al directorio y ejecutamos RAT
COMMAND_INSIDE="source /usr/local/bin/geant4.sh && \
                source /root-bin/bin/thisroot.sh && \
                source /rat/env.sh && \
                cd ${MACRO_DIR} && \
                echo 'Initializing RAT Simulation' && \
                rat neutron_validation.mac && \
                echo 'Simulation Finished'"

# --- Ejecución de Apptainer ---
# Montamos /lstore para que el contenedor pueda leer tu macro y guardar el archivo .root resultante
apptainer exec \
    -B /share/neutrino/snoplus/ \
    -B /lstore \
    ${CONTAINER_SIF} \
    bash -c "${COMMAND_INSIDE}"
