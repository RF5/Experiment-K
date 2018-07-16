import numpy as np
import random
import neuron

class Astrocytes(object):

    def __init__(self, neuron_group, w_grow_threshold = 50):
        self.neuron_group = neuron_group
        self.weight_grow_threshold = w_grow_threshold
        self.r_connection_grow = None
        self.r_neuron_grow = None

    def random_grow_connections(self):

        for neuron in self.neuron_group:
            if random.random() > self.r_connection_grow or neuron.type == "motor":
                continue
            post_neuron = neuron
            while post_neuron == neuron or post_neuron.type == "visual":
                post_neuron = random.choice(self.neuron_group)

            rand = random.randint(0, 1)
            if rand == 1:
                neuron.connect(post_neuron, 0.05)
            else:
                neuron.connect(post_neuron, -0.05)
            

    def grow_neurons(self):
        #kappa = []
        for n in self.neuron_group:
            #re = [abs(s.weight) for s in neuron.axon_synapses]
            #kappa = kappa + [sum(re)]

            for syn in n.axon_synapses:
                if syn.weight > self.weight_grow_threshold:
                    syn.weight = syn.weight / 2.0
                    new_neuron = neuron.Neuron()
                    new_neuron.connect(syn.postsynaptic_neuron, random.random() - 0.1)
                    n.connect(new_neuron, random.random() - 0.1)
                    self.neuron_group = self.neuron_group + [new_neuron]
                elif syn.weight < -self.weight_grow_threshold:
                    syn.weight = syn.weight / 2.0
                    new_neuron = neuron.Neuron()
                    new_neuron.connect(syn.postsynaptic_neuron, -random.random() + 0.1)
                    n.connect(new_neuron, -random.random() + 0.1)
                    self.neuron_group = self.neuron_group + [new_neuron]
                elif random.random() < self.r_neuron_grow:
                    syn.weight = syn.weight / 2.0
                    new_neuron = neuron.Neuron()
                    new_neuron.connect(syn.postsynaptic_neuron, random.random() - 0.5)
                    n.connect(new_neuron, random.random() - 0.5)
                    self.neuron_group = self.neuron_group + [new_neuron]

    def set_neuron_group(self, new_group):
        self.neuron_group = new_group

    def get_total_neurons(self):
        return len(self.neuron_group)

    def get_total_synapses(self):
        ree = [len(k.axon_synapses) for k in self.neuron_group]
        return sum(ree)

    def update_neurotransmitters(self, new):
        for n in self.neuron_group:
            for s in n.axon_synapses:
                s.set_neurotransmitter(new)

    def set_r_neuron_grow(self, inn):
        self.r_neuron_grow = inn

    def set_r_conn_grow(self, inn):
        self.r_connection_grow = inn

    


