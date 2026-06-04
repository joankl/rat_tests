'''
Function to construct the plot of dE/dx for a given particles as
a function of its kinetic energy at each step.
It must receive previous saved numpy data of the dE/dx and will 
return the plots

created on: 04/06/2026
'''

import numpy as np
import matplotlib.pyplot as plt

def dE_dx_plot(fin, fout):

	'''
	Function to create the plots of dE/dx

	Parameters:
	- fin: directory of the input files. It will need the dE/dxn and
		   the KE at each step saved in format npz. They are conteined
		   within the same compressed file.
	- fout: directory where plot will be saved.
	'''

	# ====== Load the Data ======
	arr = np.load(fin)

	energy = arr['energies']
	dedx_values = arr['dedx_values']
	bin_centers = arr['bin_centers']
	bin_means = arr['bin_means']
	energy_bin_edges = arr['energy_bins']

	# ===== Plots Construction =====
	plt.figure(figsize=(9, 6))
	# Plots of dot points (Straggling)
	plt.scatter(energies, dedx_values, alpha=0.08, color='darkblue', s=1.5, label='Individual Steps')

	# histogram of the mean dE/dx within each energy bin
	plt.step(energy_bin_edges[:-1], bin_means, where='post', color='orangered', lw=2, label='Mean Profile ($dE/dx$)')
	plt.scatter(bin_centers, bin_means, color='orangered', s=12, zorder=3)

	plt.xscale('log')
	#plt.yscale('log')

	plt.xlabel('Initial KE of Step (MeV)', fontsize=12)
	plt.ylabel('$dE/dx$ (MeV/mm)', fontsize=12)

	plt.title('$dE/dx$ for 5 MeV MC electrons on BisMSB', fontsize=13, fontweight='bold')
	plt.legend(loc='best')
	plt.grid(True, which="both", ls="--", alpha=0.4)

	plt.tight_layout()
	plt.savefig(fout , dpi=300)
	print(f"[-] Plot generated in: {fout}")

if __name__ == "__main__":

	fin = '/lstore/sno/joankl/rat_tests/rat_v8/electron/results/np_data/electron_5MeV_data.npz'
	fout = '/lstore/sno/joankl/rat_tests/rat_v8/electron/results/figures/'
	fig_name = 'electron_5MeV_dedx_replot.png'

	dE_dx_plot(fin, fout + fig_name)
