from brian2 import *

# Uncomment this line for Python/numpy runtime mode
brian_prefs.codegen.target = 'numpy'

# Uncomment this line for C++/weave runtime mode
#brian_prefs.codegen.target = 'weave'

# Uncomment this line to show debug output
#BrianLogger.log_level_debug()

tau = 5*ms
sigma = 0.3
eqs = '''
dv/dt = -v/tau + sigma*xi/tau**0.5 : 1
'''

G = NeuronGroup(1, eqs)

M = StateMonitor(G, 'v', record=True)

run(100*ms)

plot(M.t/ms, M.v[0])
xlabel('Time (ms)')
ylabel('v')
show()
