from brian import *

clear()
defaultclock.t = 0*ms

# Time constants
taum = 20 * msecond
taue = 5 * msecond
taui = 10 * msecond
# Reversal potentials
Ee = (0. + 60.) * mvolt
Ei = (-80. + 60.) * mvolt

eqs = Equations('''
dv/dt = (-v+ge*(Ee-v)+gi*(Ei-v))*(1./taum) : volt
dge/dt = -ge*(1./taue) : 1
dgi/dt = -gi*(1./taui) : 1 
''')

P = NeuronGroup(2000, model=eqs, threshold=10 * mvolt, \
              reset=0 * mvolt, refractory=5 * msecond,
              order=1, compile=True)
Pe = P.subgroup(1600)
Pi = P.subgroup(400)
we = 6. / 10. # excitatory synaptic weight (voltage)
wi = 67. / 10. # inhibitory synaptic weight
Ce = Connection(Pe, P, 'ge', weight=we, sparseness=0.02)
Ci = Connection(Pi, P, 'gi', weight=wi, sparseness=0.02)
# Initialization
P.v = (randn(len(P)) * 5 - 5) * mvolt
P.ge = randn(len(P)) * 1.5 + 4
P.gi = randn(len(P)) * 12 + 20

# Record the number of spikes
Me = PopulationSpikeCounter(Pe)
Mi = PopulationSpikeCounter(Pi)

# Record all excitatory spikes
spikes_e = SpikeMonitor(Pe)
# Record the membrane potential of a single neuron
mon_e = StateMonitor(Pe, 'v', record=0)
run(1 * second)

print Me.nspikes, "excitatory spikes"
print Mi.nspikes, "inhibitory spikes"

subplot(1, 2, 1)
raster_plot(spikes_e)
subplot(1, 2, 2)
plot(mon_e.times/ms, mon_e[0]/mV)
show()

