import numpy as np

class Synapse(object):

    def  __init__(self, presynaptic, postsynaptic, initial_weight):
        self.presynaptic_neuron = presynaptic
        self.postsynaptic_neuron = postsynaptic
        self.postsynaptic_neuron.dendrite_synapses += [self]
        self.weight = initial_weight

        if initial_weight < 0:
            self.synapse_type = 'inhibitory'
        elif initial_weight > 0:
            self.synapse_type = 'exitory'

        self.neurotransmitter = None

    def relay_pulse(self):
        pulse_strength = self.presynaptic_neuron.axon_potential * self.weight
        if self.neurotransmitter is not None:
            if self.neurotransmitter['op'] == 'add':
                pulse_strength += self.neurotransmitter['value']
            elif self.neurotransmitter['op'] == 'multiply':
                pulse_strength *= self.neurotransmitter['value']
            elif self.neurotransmitter['op'] == 'radd':
                if pulse_strength > 0:
                    pulse_strength += self.neurotransmitter['value']
                else:
                    pulse_strength -= self.neurotransmitter['value']

        self.weight = self.weight + 0.01 * pulse_strength
        return pulse_strength

    def set_neurotransmitter(self, intransmit):
        self.neurotransmitter = intransmit
        assert type(self.neurotransmitter) == dict


