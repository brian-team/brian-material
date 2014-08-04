from brian2 import *
import time

taum = 20 * ms
taue = 5 * ms
taui = 10 * ms
Vt   = -50 * mV
Vr   = -60 * mV
El   = -49 * mV

eqs = '''
dv/dt  = (ge+gi-(v-El))/taum : volt (unless refractory)
dge/dt = -ge/taue : volt (unless refractory)
dgi/dt = -gi/taui : volt (unless refractory)
'''

P    = NeuronGroup(4000, eqs, threshold='v>Vt', reset='v=Vr', refractory='5 * ms')
P.v  = Vr
P.ge = 0 * mV
P.gi = 0 * mV

we = (60 * 0.27 / 10) * mV # excitatory synaptic weight (voltage)
wi = (-20 * 4.5 / 10) * mV # inhibitory synaptic weight
Ce = Synapses(P, P, 'w:1', pre='ge += w')
Ci = Synapses(P, P, 'w:1', pre='gi += w')
Ce.connect('i<3200', p=0.02)
Ce.w = we
Ci.connect('i>=3200', p=0.02)
Ci.w = wi
P.v = Vr + rand(len(P)) * (Vt - Vr)

start_time = time.time()
s_mon = SpikeMonitor(P)
run(1 * second)
duration = time.time() - start_time

print duration
plt.plot(s_mon.t/ms, s_mon.i, '.')
plt.show()
