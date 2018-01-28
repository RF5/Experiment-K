import numpy as np
from synapse import Synapse

class Neuron(object):

    def __init__(self, prune_threshold=0.02, decay_rate=0.02):
        self.dendrite_synapses = []
        self.axon_synapses = []
        self.prune_threshold = prune_threshold
        self.axon_potential = 0
        self.myelin_thickness = 0
        self.decay_rate = decay_rate
        self.type = "normal"

    def connect(self, post_neuron, initial_weight):
        self.axon_synapses += [Synapse(self, post_neuron, initial_weight)]

    def prune_axon_synapses(self):
        for cnt, syn in enumerate(self.axon_synapses):
            if syn.weight < self.prune_threshold:
                #print("Pruned!")
                del self.axon_synapses[cnt]

    def set_prune_threshold(self, new):
        self.prune_threshold = new

    def get_potential(self):
        rolling_pot = 0.0
        for syn in self.dendrite_synapses:
            tmp = syn.relay_pulse()
            rolling_pot += tmp

        return rolling_pot

    def get_activation(self):
        p = self.get_potential()
        if p > 0.0:
            pos_log_activation = (np.log(p) + 1) * np.sqrt(self.myelin_thickness + 1)
        else:
            pos_log_activation = 0

        if pos_log_activation > 0:
            self.myelin_thickness = self.myelin_thickness + 0.5 * (np.log(p) + 1)

        self.axon_potential = pos_log_activation
        return self.axon_potential

    def decay_axon(self):
        for syn in self.axon_synapses:
            if self.myelin_thickness < 3:
                syn.weight -= self.decay_rate
            else:
                syn.weight -= self.decay_rate / 2
        self.myelin_thickness = self.myelin_thickness * 0.98

class VisualNeuron(Neuron):
    def __init__(self):
        super().__init__()
        self.in_pixel = None
        self.type = "visual"

    def set_px_value(self, value):
        assert len(self.dendrite_synapses) == 0
        self.in_pixel = value

    def get_potential(self):
        return self.in_pixel

class MotorNeuron(Neuron):
    def __init__(self):
        super().__init__()
        self.type = "motor"
        
    def connect(self, post_neuron, initial_weight):
        pass
    
    def get_activation(self):
        p = self.get_potential()
        if p > 0.0:
            pos_log_activation = (np.log(p) + 1)
        else:
            pos_log_activation = 0

        self.axon_potential = pos_log_activation
        return self.axon_potential
    
    def decay_axon(self):
        assert len(self.axon_synapses) <= 1
        pass