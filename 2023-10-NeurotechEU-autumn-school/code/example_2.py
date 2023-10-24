from brian2 import *

spike_source = SpikeGeneratorGroup(1, [0], [5]*ms, period=20*ms)
target_neurons = NeuronGroup(2, '''dv/dt = (10*nS*(-70*mV -v) + 
                                            g*(0*mV - v))/ (200*pF) : volt
                                   dg/dt = -g/(5*ms) : siemens''',
                                   method='euler')  # leaky integrator
target_neurons.v = -70*mV
U_SE = 0.6    # utilization of synaptic efficacy
w_max = 2*nS  # maximal synaptic conductance
synapses_eqs = '''dx/dt = z / tau_rec          : 1 # "recovered"
                  dy/dt = -y / tau_in          : 1 # "effective"
                  dz/dt = y/tau_in - z/tau_rec : 1 # "inactive"
                  tau_rec : second (constant)
                  tau_in : second (constant)'''
synapses_action = '''y += U_SE * x
                     x -= U_SE * x
                     g_post += w_max * x'''

syn = Synapses(spike_source, target_neurons, model=synapses_eqs,
               on_pre=synapses_action)
syn.connect()
syn.tau_rec = [1000, 20] *ms
syn.tau_in = [5, 25] *ms
syn.x = 0.4
syn.y = 0.4
syn.z = 0.2

state_mon = StateMonitor(target_neurons, 'g', record=True)
run(200*ms)

fig, axs = plt.subplots(2, 1, figsize=(4, 3.5), sharex=True, sharey=True,
                        gridspec_kw={'height_ratios': (1, 2)})
for idx, ax in enumerate(axs):
    ax.plot(state_mon.t/ms, state_mon.g[idx]/nS, color=f'C{idx}', lw=2)
    ax.spines[['top', 'right', 'left']].set_visible(False)
    ax.set(yticks=[])
    ax.set_title(f'$\\tau_{{\\mathrm{{rec}}}} = {syn.tau_rec[idx]/ms:.0f}\\mathrm{{ms}}, '
                 f'\\tau_{{\\mathrm{{in}}}}= {syn.tau_in[idx]/ms:.0f}\\mathrm{{ms}}$',
                 loc='right', color=f'C{idx}')
axs[0].spines['bottom'].set_visible(False)
axs[0].set_title('\n$g$', loc='left')
axs[1].set_xlabel('time (ms)')
fig.tight_layout()
fig.savefig('../images/example_2.png', transparent=True)
