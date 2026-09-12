#!/bin/bash
#SBATCH --job-name=rat_neutron_analysis      # Nombre del trabajo
#SBATCH --output=logs/analysis_%j.out  # Archivo de salida estándar (%j = Job ID)
#SBATCH --error=logs/analysis_%j.err   # Archivo de errores
#SBATCH --time=02:00:00                # Tiempo máximo de ejecución (HH:MM:SS)

# 1. Cargar el entorno de RAT/ROOT
source /lstore/sno/joankl/RAT/rat_8.1.0_appt.sh 

# 2. Ir al directorio donde está tu script (opcional pero recomendado)
cd /lstore/sno/joankl/rat_tests/functions/

# 3. Ejecutar el script de análisis
echo "Iniciando análisis de neutrones..."
python neutron_analysis.py
echo "Análisis finalizado con éxito."
