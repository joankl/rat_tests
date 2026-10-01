#!/bin/bash
#SBATCH --job-name=RAT9_electron
#SBATCH --output=electron.out
#SBATCH --error=electron.err
#SBATCH --partition=lipq

# Rutas de ejecución
CONTAINER_SIF="/lstore/sno/joankl/RAT/containers/rat9_test.sif"
RAT9_DIR="/lstore/sno/joankl/RAT/containers/rat9_test_dir"
MACRO_DIR="/lstore/sno/joankl/rat_tests/rat_v9/electron/macros"

# Comando interno: usamos $(geant4-config --prefix) para encontrar la ruta real dinámicamente
COMMAND_INSIDE='source $(geant4-config --prefix)/bin/geant4.sh && cd '"${RAT9_DIR}"' && source env.sh && cd '"${MACRO_DIR}"' && rat electron_validation.mac'

# Ejecución montando los volúmenes necesarios
apptainer exec \
    -B /share/ \
    -B /lstore/ \
    ${CONTAINER_SIF} \
    bash -c "${COMMAND_INSIDE}"
