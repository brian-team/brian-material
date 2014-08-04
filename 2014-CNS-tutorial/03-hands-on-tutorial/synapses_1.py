from brian2 import *

tau    = 10*ms
taue   = 5*ms
model  = '''dv/dt  = ((10 - v)*ge - v)/tau  : 1
			dge/dt = -ge/taue : 1
		  '''

spikes = {}
spikes['indices'] = numpy.zeros(3)
spikes['times'] = numpy.array([10, 60, 65])*ms

presyn  = SpikeGeneratorGroup(1, spikes['indices'], spikes['times'])
postsyn = NeuronGroup(10, model, threshold = "v > 1", reset = "v = -0.1")

c       = Synapses(presyn, postsyn, 'w:1', pre='ge += w')
c.connect('i == j')
c.delay = 5*ms 
c.w     = 'rand()'

Mp      = StateMonitor(postsyn, 'v', record = True)

run(100*ms)
plot(Mp.t/ms, Mp.v[0]/mV)
show()





