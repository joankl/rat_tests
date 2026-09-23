#!/bin/bash
		#SBATCH --job-name=RAT8_neutron_analysis_0
		#SBATCH --output=logs_RAT8_neutron_analysis/job_0.out
		#SBATCH --error=logs_RAT8_neutron_analysis/job_0.err
		#SBATCH --partition=lipq

		echo "Running on host: $(hostname)"
		echo "Starting Container..."

		# Run apptainer
		# We initialize the directories to be readen: /share (date), /lstore (libs y output), y $PWD (scripts)
		apptainer exec \
		-B /lstore/sno/joankl \
		-B /lstore/sno/joankl/rat_tests/rat_v8/neutrons/jobs \
		/lstore/sno/joankl/RAT/containers/rat_8.1.0.sif \
		bash -c 'source /usr/local/bin/geant4.sh && source /root-bin/bin/thisroot.sh && source /rat/env.sh && export PYTHONPATH=$PYTHONPATH:/lstore/sno/joankl/my_pylibs/:/lstore/sno/joankl/rat_tests/rat_v8/neutrons/jobs && python3 -c "import sys; from neutron_analysis import analyze_neutrons; analyze_neutrons(sys.argv[1], sys.argv[2])" "/lstore/sno/joankl/rat_tests/rat_v8/neutrons/results/root_files/neutron_3MeV_8.root" "/lstore/sno/joankl/rat_tests/rat_v8/neutrons/results/np_files/neutron_3MeV_8.npz"'

echo "Job finished"
