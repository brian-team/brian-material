from brian2 import *

tau    = 10*ms
taue   = 5*ms


model  = '''dv/dt  = ((10. - v)*ge - v)/tau  : 1
            dge/dt = -ge/taue                : 1'''


presyn  = PoissonGroup(10, rates = '100*Hz*(sin(t/second) + 1)')
postsyn = NeuronGroup(10, model, threshold = "v > 1", reset = "v = -0.1")

c       = Synapses(presyn, postsyn, 'w:1', pre='ge += 0.1')
c.connect('i==j')
print len(c)

d       = Synapses(presyn, postsyn, 'w:1', pre='ge += 0.1')
d.connect('i>j')
print len(d)

e       = Synapses(presyn, postsyn, 'w:1', pre='ge += 0.1')
e.connect(True, p=0.2)
print len(e)


Mp      = StateMonitor(postsyn, 'v', record = True)

run(100*ms)

plot(Mp.t/ms, Mp.v[0]/mV)
show()
