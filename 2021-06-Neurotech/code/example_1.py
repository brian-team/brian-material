from brian2 import *

g_L = 10*nS; E_L = -70*mV; C_m = 200*pF
vt_0 = -50*mV; vt_adapt = 10*mV; tau_vt = 50*ms; sigma_vt = 5*mV
neurons = NeuronGroup(4, model="""
                     dv/dt = (g_L*(E_L - v) + I_inj)/C_m: volt
                     dvt/dt = (vt_0 - vt)/tau_vt + sigma_vt*tau_vt**-0.5*xi : volt
                     I_inj : amp (constant)""",
                      threshold='v > vt', reset='''v = E_L
                                                  vt += vt_adapt''')
neurons.v = E_L
neurons.vt = vt_0
neurons.I_inj = '0.25*nA + 0.25*i*nA'
state_mon = StateMonitor(neurons, ['v', 'vt'], record=True)
spike_mon = SpikeMonitor(neurons, variables=['v'])

run(250*ms)

spike_values = spike_mon.all_values()
fig, axs = plt.subplots(4, 1, sharex=True, sharey=True,
                        figsize=(4, 7))

for idx, ax in enumerate(axs):
    ax.plot(state_mon.t/ms, state_mon.v[idx]/mV, lw=2)
    ax.plot(state_mon.t/ms, state_mon.vt[idx] / mV, lw=2)
    spike_times = spike_values['t'][idx]
    voltage_at_spike = spike_values['v'][idx]
    ax.vlines(spike_times/ms,
              voltage_at_spike/mV, np.zeros(len(spike_times)),
              color='C0', lw=2)
    ax.set_title(f'$I_{{inj}} = {neurons.I_inj[idx]/nA:.2f}$nA', loc='right')
    ax.spines[['top', 'left', 'right', 'bottom']].set_visible(False)
    ax.set(yticks=[])
axs[-1].spines['bottom'].set_visible(True)
axs[-1].set(xlabel='time (ms)')
fig.tight_layout()
fig.savefig('../images/example_1.png', transparent=True)
