# Python script designed to submit jobs to analyze neutron simulations

import glob
import re
import sys
import os
import time

# Main directory of neutron simualtions ROOT files and file name patter
main_fdir = '/lstore/sno/joankl/rat_tests/rat_v8/neutrons/results/root_files/neutron_3MeV_*.root' 
flist = glob.glob(main_fdir)

# Main directory where to save the analysis results
main_save_dir = '/lstore/sno/joankl/rat_tests/rat_v8/neutrons/results/np_files'
os.makedirs(main_save_dir, exist_ok=True)

# RAT container directory and libraries
CONTAINER_SIF = "/lstore/sno/joankl/RAT/containers/rat_8.1.0.sif"
MY_LIBS = "/lstore/sno/joankl/my_pylibs/" # Complementar python libraries
SCRIPT_DIR = os.getcwd() # Return the current directory path, where the script and rat_read_ntuples.py are.

data_type = 'RAT8_neutron_analysis'
os.makedirs(f'logs_{data_type}', exist_ok=True)

if __name__ == '__main__':

	for i_dx, fin_dir_i in enumerate(flist):

		# Define the output file name and output directory
		base_name = os.path.basename(fin_dir_i)
		fname_i = os.path.splitext(base_name)[0]
		fout_dir = os.path.join(main_save_dir, fname_i + '.npz')

		# script.sh name
		script_name = f"run_job_{data_type}_{i_dx}.sh"

		# Call the Analysis function and pass arguments through sys
		py_one_liner = ("import sys; "
			"from neutron_analysis import analyze_neutrons; "
			"analyze_neutrons(sys.argv[1], sys.argv[2])")

		command_inside_container = (
		"source /usr/local/bin/geant4.sh && "
		"source /root-bin/bin/thisroot.sh && "
		"source /rat/env.sh && "
		f"export PYTHONPATH=$PYTHONPATH:{MY_LIBS}:{SCRIPT_DIR} && "
		f"python3 -c \"{py_one_liner}\" \"{fin_dir_i}\" \"{fout_dir}\""
		)

        # Content of script SBATCH
		script_content = f"""#!/bin/bash
		#SBATCH --job-name={data_type}_{i_dx}
		#SBATCH --output=logs_{data_type}/job_{i_dx}.out
		#SBATCH --error=logs_{data_type}/job_{i_dx}.err
		#SBATCH --partition=lipq

		echo "Running on host: $(hostname)"
		echo "Starting Container..."

		# Run apptainer
		# We initialize the directories to be readen: /share (date), /lstore (libs y output), y $PWD (scripts)
		apptainer exec \\
		-B /lstore/sno/joankl \\
		-B {SCRIPT_DIR} \\
		{CONTAINER_SIF} \\
		bash -c '{command_inside_container}'

echo "Job finished"
"""

		with open(script_name, "w") as f:
			f.write(script_content)

		# Enviar a la cola
		print(f"Enviando job {i_dx}...")
		os.system(f"sbatch {script_name}")

		# Borrar el script generado para no llenar la carpeta de basura (opcional)
		# os.remove(script_name) 

		time.sleep(0.5) # Pequeña pausa para no saturar al scheduler




