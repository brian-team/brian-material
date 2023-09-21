from brian2 import *
seed(20210608)
prefs.codegen.target = 'numpy'  # Avoids compilation

neuron = NeuronGroup(100, model="""# ... actual neuron model
                     neuron_type : integer (constant)
                     x : meter (constant)
                     y : meter (constant)""")
neuron.neuron_type = 'int(rand() * 2)'  # two types
neuron.x = '(i % 10) * 50*um'  # Neurons arranged in a grid
neuron.y = '(i // 10) * 50*um'

synapses = Synapses(neuron, neuron)  # do-nothing synapse just for illustration
synapses.connect('neuron_type_pre == neuron_type_post',  # only if same type
                 p='1.5*exp(-sqrt(((x_pre - x_post)**2 +'
                   '               (y_pre - y_post)**2))/(100*um))')
fig, axs = plt.subplots(2, 1, sharex=True, sharey=True,
                        figsize=(4, 7))
colormap = np.array(['C0', 'C1'])
for type_idx, ax in enumerate(axs):
    ax.scatter(neuron.x/um, neuron.y/um,
               c=colormap[neuron.neuron_type])
    # Chose one example neuron of the type near the centre
    of_type = np.nonzero(neuron.neuron_type == type_idx)[0]
    closest_idx = np.argmin((neuron.x[of_type] - 250*um)**2 +
                            (neuron.y[of_type] - 250*um)**2)
    closest_idx = of_type[closest_idx]
    for idx in of_type:
        for target in synapses.j[idx, :]:
            ax.annotate('',
                        xy=(synapses.x_post[idx, target]/um, synapses.y_post[idx, target]/um), xycoords='data',
                        xytext=(synapses.x_pre[idx, target]/um, synapses.y_pre[idx, target]/um), textcoords='data',
                        arrowprops=dict(arrowstyle="wedge",
                                        fc=colormap[type_idx],
                                        ec="none",
                                        alpha=0.8 if idx == closest_idx else 0.1,
                                        connectionstyle="arc3,rad=0.3"))
    ax.axis('off')
    ax.set_aspect('equal')
fig.tight_layout()
plt.savefig('../images/example_3.png', transparent=True)
