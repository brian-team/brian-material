from brian2 import *
seed(20210608)

g_L = 10*nS; E_L = -70*mV; C_m = 200*pF
neuron = NeuronGroup(3, model="""
                     dv/dt = (g_L*(E_L - v) + I_inj)/C_m : volt
                     I_inj = amplitude * (0.5 + 0.5 * sin(2*pi*freq*t)) : amp
                     amplitude : amp
                     freq : Hz""",
                     threshold='v > -40*mV', reset='v = E_L')
neuron.run_regularly("""amplitude = rand() * 2*nA
                        freq = 50*Hz + 100*Hz*rand()""",
                     dt=100*ms)  # change injected current every 100ms
neuron.v = E_L
state_mon = StateMonitor(neuron, ['v', 'I_inj'], record=True)
spike_mon = SpikeMonitor(neuron)

run(300*ms)

fig, axs = plt.subplots(4, 1, sharex=True, figsize=(4, 7))
for idx, ax in enumerate(axs[:3]):
    ax.plot(state_mon.t/ms, state_mon.I_inj[idx]/nA, lw=2, color=f'C{idx}')
    ax.spines[['top', 'right', 'bottom']].set_visible(False)
    ax.set_ylim(0, 2)
axs[0].set_title('$I_{inj}$ (nA)', loc='left')
axs[2].spines['bottom'].set_visible(True)

spike_trains = spike_mon.spike_trains()
for idx in range(3):
    spikes = spike_trains[idx]
    axs[-1].plot(spikes/ms, 3-np.ones(len(spikes)) * idx, '|', lw=2, mew=2)
axs[-1].spines[['top', 'left', 'right']].set_visible(False)
axs[-1].set(xlabel='time (ms)', yticks=[])
fig.tight_layout()
plt.savefig('../images/example_4.png', transparent=True)

