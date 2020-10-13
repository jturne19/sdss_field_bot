"""


"""
import numpy as np
import sys

# read in field range table
run, fmin, fmax = np.loadtxt('field_range.dat', unpack=True, dtype='int')


f = open('master_field.list', 'w')

for run_index in range(len(run)):
	R = run[run_index]

	for col_number in range(1,7):
		C = col_number

		for field in range(fmin[run_index], fmax[run_index]+1):
			F = field
			f.write('R=%i&C=%i&F=%i\n'%(R, C, F))


f.close()