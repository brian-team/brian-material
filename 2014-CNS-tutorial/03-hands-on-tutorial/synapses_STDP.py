from time import time
from brian2 import *

N       = 1000
taum    = 10 * ms
taupre  = 20 * ms
taupost = taupre
Ee      = 0 * mV
vt      = -54 * mV
vr      = -60 * mV
El      = -74 * mV
taue    = 5 * ms
F       = 15 * Hz
gmax    = .01
dApre   = .01
dApost  = -dApre * taupre / taupost * 1.05
dApost *= gmax
dApre  *= gmax
tau_homeo = 1*second

eqs_neurons = '''
dv/dt=(ge*(Ee-vr)+El-v)/taum : volt   # the synaptic current is linearized
dge/dt=-ge/taue : 1
drate/dt = -rate/tau_homeo : 1
'''

input = PoissonGroup(N, rates=F)
neurons = NeuronGroup(1, eqs_neurons, threshold='v>vt', reset='v=vr; rate += 1')
S = Synapses(input, neurons,
             '''dw/dt = 0.01*w*(10 - rate_post): 1''',
             pre = '''ge += w''', connect=True)

S.w='rand()*gmax'
dmax = 5*ms
S.delay = 'rand()*dmax'
start_time = time()

w_recorder = StateMonitor(S, 'w', record=True, when=Clock(dt=1*second))
rate_recorder = StateMonitor(neurons, 'rate', record=True)

run(10 * second, report='text')
print "Simulation time:", time() - start_time

subplot(411)
plot(S.w[:] / gmax, '.')
subplot(412)
hist(S.w[:] / gmax, 20)
subplot(413)
imshow(numpy.diff(w_recorder.w, 1), aspect='auto', interpolation='nearest')
colorbar()
subplot(414)
plot(rate_recorder.rate[0])
show()
