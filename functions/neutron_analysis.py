'''
Script to read RAT neutron simulations and extract observables of interest. 
The observables are:
1. Traveling distance of the neutron.
2. Energy spectrum of produced gammas

Creation Date: 12/09/2026
'''

#!/usr/bin/env python3
import numpy as np
import ROOT
import rat

def analyze_neutrons(fin_dir, fout_np_dir):
    
    # Inicializar el lector de datos de RAT
    ds_reader = ROOT.RAT.DU.DSReader(fin_dir)
    total_entries = ds_reader.GetEntryCount()
    print(f"Processing {total_entries} neutron events...")

    penetration_distances = []
    capture_gamma_energies = []

    # Loop on events
    for i_entry in range(total_entries):
        r_ds = ds_reader.GetEntry(i_entry)
        r_mc = r_ds.GetMC()
        mc_track_ids = r_mc.GetMCTrackIDs()

        neutron_track_id = -1 # Default value. It may change to the track ID if a neutron is found.
        
        # --- Primary neutron track ---
        for track_id in mc_track_ids:
            r_mc_track = r_mc.GetMCTrack(track_id)
            
            # Neutron PDF code is 2112. Look for the first particle (ParentID == 0).
            if r_mc_track.GetParentID() == 0 and r_mc_track.GetPDGCode() == 2112:
                neutron_track_id = r_mc_track.GetTrackID()
                
                step_count = r_mc_track.GetMCTrackStepCount()
                if step_count > 0:
                    # step where neutron was generated
                    first_step = r_mc_track.GetMCTrackStep(0)
                    pos_initial = first_step.GetPosition()
                    
                    # step where neutron was captured
                    last_step = r_mc_track.GetMCTrackStep(step_count - 1)
                    pos_final = last_step.GetPosition()
                    
                    # Propagation distance
                    distance = (pos_final - pos_initial).Mag()

                    #dx = pos_final.x() - pos_initial.x()
                    #dy = pos_final.y() - pos_initial.y()
                    #dz = pos_final.z() - pos_initial.z()
                    #distance = np.sqrt(dx**2 + dy**2 + dz**2)
                    
                    penetration_distances.append(distance)
                
                # get out of the loop once the neutron is found
                break 

        # --- Secondary gammas analysis ---
        # Look for the sons of the neutron if identified correctly.
        if neutron_track_id != -1:
            for track_id in mc_track_ids:
                r_mc_track = r_mc.GetMCTrack(track_id)
                
                # Filter only the gamma particles (PDG == 22)
                if r_mc_track.GetParentID() == neutron_track_id and r_mc_track.GetPDGCode() == 22:
                    
                    if r_mc_track.GetMCTrackStepCount() > 0:
                        # Take the initial energy of the produced gammas (step 0)
                        gamma_energy = r_mc_track.GetMCTrackStep(0).GetKineticEnergy()
                        capture_gamma_energies.append(gamma_energy)

    # convert to numpy
    penetration_distances = np.array(penetration_distances)
    capture_gamma_energies = np.array(capture_gamma_energies)

    # save the data
    np.savez(fout_np_dir, 
             distances=penetration_distances, 
             gamma_energies=capture_gamma_energies)
    
    print(f"[-] Data saved in NumPy Format in: {fout_np_dir}")

if __name__ == "__main__":

    fin_dir = '/lstore/sno/joankl/rat_tests/rat_v8/neutrons/macros/neutron_validation_3MeV.root'
    fout_dir = '/lstore/sno/joankl/rat_tests/rat_v8/neutrons/results/'
    fout_name = 'neutron_data.npz'

    fout_np_dir = fout_dir + fout_name
    
    analyze_neutrons(fin_dir, fout_np_dir)