from brian2 import *

tau_input = 5 * ms
input = NeuronGroup(1, model='dx/dt=-x/tau_input + (2./tau_input)**.5*xi:1')

N     = 25
tau   = 20 * ms
sigma = .015

eqs_neurons = '''
dx/dt = (0.9+.5*I-x)/tau+sigma*(2./tau)**.5*xi:1
I : 1 (linked)
'''

neurons   = NeuronGroup(N, model=eqs_neurons, threshold="x > 1", reset="x=0", refractory="5 * ms")
neurons.I = linked_var(input, 'x')
neurons.v = rand(N)
spikes    = SpikeMonitor(neurons)
voltages  = StateMonitor(neurons, 'x', record=arange(5))

run(500 * ms)

figure()
subplot(211)
plot(spikes.t/second, spikes.i, '.k')
subplot(212)
plot(voltages.t, voltages.x.T)
show()
