'''
Python script designed to read the RAT test output files.
It will read ROOT files and perform analysis on the 
simulated particle properties, such as dE/dx behavior.

created on: 03/06/2026
'''

#!/usr/bin/env python3
import sys
import numpy as np
import matplotlib.pyplot as plt

import ROOT
import rat

def analyze_dedx_pure(fin_dir, fout_plot_dir, fout_np_dir):

	'''
	Function to analyze dE/dx of simulated particles.
	Return: (1) Energy of particles at each step in numpy format
			(2) dE/dx profile in numpy format
			(3) plots of dE/dx in 

	Parameters:
	- fin_dir: Directory of the ROOT file with the MC information
	- fout_plot_dir: Directory where to save the output plots
	- fout_np_dir: Directory where to save the output numpy arrays
	'''

	ds_reader = ROOT.RAT.DU.DSReader(fin_dir)

	energy_i = 0.05
	energy_f = 5.5
	n_bins = 20
	energy_bin_edges = np.linspace(energy_i, energy_f, n_bins + 1)

	# List to collect the information at each particle step
	all_energies = []
	all_dedx = []

	total_entries = ds_reader.GetEntryCount()
	print(f"Procesando {total_entries} eventos...")

	# Loop over events
	for i_entry in range(total_entries):
		r_ds = ds_reader.GetEntry(i_entry)
		r_mc = r_ds.GetMC()
		mc_track_ids = r_mc.GetMCTrackIDs()

		# Loop over generated tracks
		for track_id in mc_track_ids:
			r_mc_track = r_mc.GetMCTrack(track_id)

			# Take only the generted parent particle
			if r_mc_track.GetParentID() != 0:
				continue

			step_count = r_mc_track.GetMCTrackStepCount()
			if step_count < 2:
				continue

			# take the kinetic energy of the initial step
			previous_energy = r_mc_track.GetMCTrackStep(0).GetKineticEnergy()

			# Loop over the steps of the track
			for i_step in range(1, step_count):
				r_mc_track_step = r_mc_track.GetMCTrackStep(i_step)
				current_energy = r_mc_track_step.GetKineticEnergy()
				step_length = r_mc_track_step.GetLength()

				# Energy loss
				d_e = previous_energy - current_energy

				# Validation conditions
				if d_e > 0.0 and step_length > 0.0:
					calculated_dedx = d_e / step_length

					# Guardar datos para el análisis en Python
					all_energies.append(previous_energy)
					all_dedx.append(calculated_dedx)

				previous_energy = current_energy

	energies = np.array(all_energies)
	dedx_values = np.array(all_dedx)

	# ===== Histograms Calculation =====

	bin_centers = []
	bin_means = []

	for i in range(len(energy_bin_edges) - 1):
		low, high = energy_bin_edges[i], energy_bin_edges[i+1]

		# Only pick energies between the bin edges
		mask = (energies >= low) & (energies < high) 

		if np.any(mask):
			# compute the mean value of dE/dx within this bin
			bin_means.append(np.mean(dedx_values[mask]))
		else:
			bin_means.append(0.0)
		bin_centers.append((low + high) / 2.0)

	# Save the raw data
	np.savez(fout_np_dir, energies=energies, dedx_values=dedx_values,
		bin_centers=bin_centers, bin_means=bin_means, energy_bins=energy_bin_edges)
	
	print(f"[-] Data saved in NumPy Format in: {fout_np_dir}")

	# ===== Plots Construction =====
	plt.figure(figsize=(9, 6))
	# Plots of dot points (Straggling)
	plt.scatter(energies, dedx_values, alpha=0.08, color='darkblue', s=1.5, label='Individual Steps')

	# Graficar el histograma del dE/dx promedio escalonado
	plt.step(energy_bin_edges[:-1], bin_means, where='post', color='orangered', lw=2, label='Mean Profile ($dE/dx$)')
	plt.scatter(bin_centers, bin_means, color='orangered', s=12, zorder=3)

	plt.xscale('log')
	plt.yscale('log')

	plt.xlabel('Initial KE of Step (MeV)', fontsize=12)
	plt.ylabel('$dE/dx$ (MeV/mm)', fontsize=12)

	plt.title('$dE/dx$ for electrons (BisMSB)', fontsize=13, fontweight='bold')
	plt.legend(loc='best')
	plt.grid(True, which="both", ls="--", alpha=0.4)

	plt.tight_layout()
	plt.savefig(fout_plot_dir , dpi=300)
	print(f"[-] Plot generated in: {fout_plot_dir}")



if __name__ == "__main__":

	fin_dir = '/lstore/sno/joankl/rat_tests/rat_v8/electron/macros/electron_validation_5MeV.root'
	fout_plot_dir = '/lstore/sno/joankl/rat_tests/rat_v8/electron/results/figures/'
	fout_np_dir = '/lstore/sno/joankl/rat_tests/rat_v8/electron/results/np_data/'

	fig_name = 'electron_5MeV_dedx.png'
	np_array_name = 'electron_5MeV_data.npz'

	analyze_dedx_pure(
		fin_dir = fin_dir, 
		fout_plot_dir = fout_plot_dir + fig_name, 
		fout_np_dir = fout_np_dir + np_array_name
		)