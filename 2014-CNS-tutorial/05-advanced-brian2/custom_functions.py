from brian2 import *

# Uncomment this line for Python/numpy runtime mode
brian_prefs.codegen.target = 'numpy'

# Uncomment this line for C++/weave runtime mode
#brian_prefs.codegen.target = 'weave'

# Uncomment this line to show debug output
#BrianLogger.log_level_debug()

@check_units(t=second, result=1)
def piecewise_linear(t):
    return where(t<50*ms, t/(50*ms), 1+3*(t-50*ms)/(50*ms))

eqs = '''
v = piecewise_linear(t) : 1
'''

G = NeuronGroup(1, eqs)
M = StateMonitor(G, 'v', record=True)
run(100*ms)
plot(M.t/ms, M.v[0])
xlabel('Time (ms)')
ylabel('v')
show()
