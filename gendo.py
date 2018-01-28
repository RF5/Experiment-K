import neuron
import synapse
import glia
import sys
import random
from tensorflow.examples.tutorials.mnist import input_data
import time

def main():
    print("Beginning")

    mnist = input_data.read_data_sets("MNIST_data/", one_hot=False)
    
    # x is now (1, 784)
    # y is now (1, 10) one hot vector
    visual_ns = [neuron.VisualNeuron() for _ in range(784)]
    motor_ns = [neuron.MotorNeuron() for _ in range(10)]
    acyte = glia.Astrocytes([])

    cnt = 0
    switch_image_every = 10 # in seconds

    positive_nt = {'op': 'multiply', 'value': 1.3}
    negative_nt = {'op': 'multiply', 'value': 0.7}

    first_neuron = neuron.Neuron()
    for n in visual_ns:
        n.connect(first_neuron, random.random() - 0.5)
    for n in motor_ns:
        first_neuron.connect(n, random.random() - 0.5)

    acyte.set_neuron_group([first_neuron,] + visual_ns + motor_ns)

    #TODO make metrics to see longest living neuron (make sure the good ones aren't just dying out)
    ngrow = acyte.r_neuron_grow = 0.04
    nini = ngrow
    cgrow = acyte.r_connection_grow = 0.9
    cinit = cgrow

    # Running accuracy over past 100 timesteps
    running_accuracy = [0] * 80

    print("Starting sequence")
    while 1:

        if cnt % switch_image_every == 0:
            x, y = mnist.train.next_batch(1)
            x = x.reshape([-1])
            y = y[0]

            for i in range(784):
                visual_ns[i].set_px_value(x[i])

        tmp = 0
        for n in visual_ns:
            tmp += len(n.axon_synapses)

        # activate each neuron
        for n in acyte.neuron_group:
            n.get_activation()
            n.decay_axon()
            n.prune_axon_synapses()

        tmp2 = acyte.get_total_neurons()
        if tmp2 > 1:
            acyte.random_grow_connections()
        #print("Kappa")
        acyte.grow_neurons()
        if cnt > 0:
            ngrow = nini * (1 / cnt)
        acyte.set_r_conn_grow(cgrow)
        acyte.set_r_neuron_grow(ngrow)
        #print("delta")

        responses = [k.get_activation() for k in motor_ns]
        tmp = max(responses)
        output = responses.index(tmp)

        if output == y:
            # do shit, add positive neurotransmitter
            acyte.update_neurotransmitters(positive_nt)
            running_accuracy[cnt % 100] = 1
        else:
            # do shit, add neuroinhibitor
            acyte.update_neurotransmitters(negative_nt)
            running_accuracy[cnt % 100] = 0

        kakka = acyte.get_total_synapses() + tmp
        if kakka > 10000:
            cgrow = cinit * 0.5
            negative_nt = {'op': 'multiply', 'value': 0.1}
        if kakka > 20000:
            negative_nt = {'op': 'multiply', 'value': 0.01}

        print("Total neurons: %4d, synapses: %4d " % (tmp2, kakka))
        print("input image: %d | %d output. Accuracy = %3f | cnt = %d" % (y, output, sum(running_accuracy)/100.0, cnt))
        print("Responses: ", responses)

        cnt = cnt + 1



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)