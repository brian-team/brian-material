from brian2 import *

N   = 10
v0  = 1.05
tau = 10*ms

neurons = NeuronGroup(N * N, '''x : meter
                                y : meter
                          dv/dt  = (v0-v+Igap)/tau : 1
                          Igap                     : 1 # gap junction current
						''', threshold='v>1', reset='v=0')

# initialize the grid positions
grid_dist = 25*umeter
neurons.x = '(i / N) * grid_dist - N/2.0 * grid_dist'
neurons.y = '(i % N) * grid_dist - N/2.0 * grid_dist'

neurons.v = rand(N*N)
trace = StateMonitor(neurons, 'v', record=True)

S = Synapses(neurons, neurons, '''w                           : 1 
                                  Igap_post = w*(v_pre-v_post): 1 (summed)''')

S.connect('i != j', p='1.5 * exp(-((x_pre-x_post)**2 + (y_pre-y_post)**2)/(2*(60*umeter)**2))')
S.w = 1

run(500*ms)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig   = plt.figure()
im    = plt.imshow(trace.v[:, 0].reshape(N, N), cmap=plt.get_cmap('jet'), interpolation='nearest')
count = 0

def updatefig(*args):
	global count
	count += 1
	im.set_array(trace.v[:, count].reshape(N, N))
	return im,

ani = animation.FuncAnimation(fig, updatefig, interval=30, blit=True)
plt.show()

show()
