#!/bin/bash
#SBATCH --job-name=RAT8_neutron_0
#SBATCH --output=/lstore/sno/joankl/rat_tests/rat_v8/neutrons/jobs/logs/RAT8_neutron_0.out
#SBATCH --error=/lstore/sno/joankl/rat_tests/rat_v8/neutrons/jobs/logs/RAT8_neutron_0.err
#SBATCH --partition=lipq

# Execute Apptainer
apptainer exec \
    -B /lstore/sno/joankl \
    /lstore/sno/joankl/RAT/containers/rat_8.1.0.sif \
    bash -c "source /usr/local/bin/geant4.sh && source /root-bin/bin/thisroot.sh && source /rat/env.sh && rat /lstore/sno/joankl/rat_tests/rat_v8/neutrons/jobs/macro_RAT8_neutron_0.mac"
