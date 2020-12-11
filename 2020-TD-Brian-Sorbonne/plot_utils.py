'''
A number of plotting functions to have nice plots in the notebooks for part 2 and 3.
'''

from brian2 import *

def plot_current_voltage(state_mon, inp_spikes, out_spikes):
    fig, (ax_spikes, ax_current, ax_voltage) = plt.subplots(3, 1, sharex=True)
    ax_spikes.plot(inp_spikes.t/ms, inp_spikes.i, ',')
    ax_spikes.axis('off')
    ax_current.plot(state_mon.t/ms, state_mon.I_syn[0]/nA, label=f'mean: {np.mean(state_mon.I_syn[0]/nA):.2f} nA')
    ax_current.set(ylabel='$I_{syn}$ (nA)')
    ax_current.legend()
    ax_current.spines['top'].set_visible(False)
    ax_current.spines['right'].set_visible(False)
    ax_voltage.plot(state_mon.t/ms, state_mon.v[0]/mV)
    ax_voltage.vlines(out_spikes.t/ms, np.ones(len(out_spikes.t))*-50, np.ones(len(out_spikes.t))*-20, ls=':')
    ax_voltage.set(xlabel='time (ms)', ylabel='$v$ (mV)')
    ax_voltage.spines['top'].set_visible(False)
    ax_voltage.spines['right'].set_visible(False)
    return ax_voltage

def plot_periphery_model(sound_input, periphery_spikes, limits=None):
    fig, (ax_inp, ax_spikes) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [2.5, 1]})
    ax_inp.plot(sound_input.t/ms, sound_input.delayed_sound.T)
    ax_inp.spines['right'].set_visible(False)
    ax_inp.spines['left'].set_visible(False)
    ax_inp.spines['top'].set_visible(False)
    ax_inp.set_yticks([])

    spike_times = periphery_spikes.spike_trains()
    ax_spikes.plot(spike_times[0]/ms, np.ones(len(spike_times[0])), 'o')
    ax_spikes.plot(spike_times[1]/ms, np.zeros(len(spike_times[1])), 'o')
    ax_spikes.spines['left'].set_visible(False)	
    ax_spikes.spines['right'].set_visible(False)
    ax_spikes.spines['top'].set_visible(False)
    ax_spikes.set_yticks([])
    if limits is not None:
        ax_spikes.set_xlim(*[l/ms for l in limits])
    ax_spikes.set_xlabel('time (ms)')
    plt.tight_layout()
    
def plot_sound_localisation(sound_input, spikes):
    fig, (ax_sound, ax_spikes) = plt.subplots(2, 1, sharex=True)

    ax_sound.plot(sound_input.t/ms, sound_input.delay.T/ms)
    ax_sound.set(ylabel='delay (ms)')
    ax_sound.spines['top'].set_visible(False)
    ax_sound.spines['right'].set_visible(False)
    i, t = spikes.it
    ax_spikes.plot(t/ms, i, '.')
    ax_spikes.set_xlabel('Time (ms)')
    ax_spikes.set_ylabel('Neuron index')
    ax_spikes.spines['top'].set_visible(False)
    ax_spikes.spines['right'].set_visible(False)
    plt.tight_layout()

