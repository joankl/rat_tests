#!/bin/bash
#SBATCH --job-name=RAT_neutron_simulation      # Nombre del trabajo
#SBATCH --output=logs/analysis_%j.out  # Archivo de salida estándar (%j = Job ID)
#SBATCH --error=logs/analysis_%j.err   # Archivo de errores

# 1. Cargar el entorno de RAT/ROOT
# Reemplaza esta ruta con el archivo env.sh oficial de tu instalación de RAT 8
source /lstore/sno/joankl/rat_v8/env.sh 

# 2. Ir al directorio donde está tu script (opcional pero recomendado)
cd /lstore/sno/joankl/rat_tests/rat_v8/neutrons/macros

# 3. Ejecutar el script de análisis
echo "Initializing RAT Simulation"
rat neutron_validation.mac 
echo "Simulation Finished"
