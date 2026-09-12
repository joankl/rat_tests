#!/bin/bash
#SBATCH --job-name=rat_n_analysis      # Nombre del trabajo
#SBATCH --output=logs/analysis_%j.out  # Archivo de salida estándar (%j = Job ID)
#SBATCH --error=logs/analysis_%j.err   # Archivo de errores
#SBATCH --time=02:00:00                # Tiempo máximo de ejecución (HH:MM:SS)
#SBATCH --mem=4G                       # Memoria RAM solicitada
#SBATCH --cpus-per-task=1              # Número de núcleos (el script es secuencial)

# 1. Cargar el entorno de RAT/ROOT
# Reemplaza esta ruta con el archivo env.sh oficial de tu instalación de RAT 8
source /lstore/sno/joankl/rat_v8/env.sh 

# 2. Ir al directorio donde está tu script (opcional pero recomendado)
cd /lstore/sno/joankl/rat_tests/functions/

# 3. Ejecutar el script de análisis
echo "Iniciando análisis de neutrones..."
python3 neutron_analysis.py
echo "Análisis finalizado con éxito."
