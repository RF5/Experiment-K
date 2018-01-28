from math import sin, cos, exp, sqrt, pi
import random

def holder_table(di):
    x0 = di['x0']
    x1 = di['x1']
    return -abs(sin(x0)*cos(x1)*exp(abs(1-sqrt(x0*x0+x1*x1)/pi)))

class RandomOptimizer(object):

    def __init__(self, func, bounds, keep_top_k=5):
        '''
            func: the function to minimize, something that say trains your network for a few epochs.
                It should take in a dict of hyperparameters and return the final loss or average reward
                (depending on whether u want to max or min) after it finishes training.
            bounds: dict of [min, max] pairs for each hyperparam
            keep_top_k: how many runs to keep track of. i.e 5 means this class will keep track of the hyperparams for
                the 5 runs with the highest (or lowest) reward (or loss).
        '''
        self.function = func
        assert callable(func)
        self.param_bounds = bounds
        self.keep_top_k = keep_top_k
        assert type(bounds) == dict
        self.min_losses = []
        for a in range(self.keep_top_k):
            self.min_losses.append({'loss': float('inf'), 'hyperparameters': {}})

    def minimize(self, function_calls = 10):
        # min losses goes from best run (least loss) at index 0 to least best at max index

        for i in range(function_calls):
            current_inputs = {}
            for key, value in self.param_bounds.items():
                current_inputs[key] = random.uniform(value[0], value[1])

            current_loss = self.function(current_inputs)

            for obj in self.min_losses:
                if current_loss < obj['loss']:
                    obj['loss'] = current_loss
                    obj['hyperparameters'] = current_inputs
                        
                    break

        return self.min_losses[0]
    
    def maximize(self, function_calls):
        self.min_losses = [{'loss': float('inf'), 'hyperparameters': {}}] * self.keep_top_k
        # min losses goes from best run (least loss) at index 0 to least best at max index

        for i in range(function_calls):
            current_inputs = {}
            for key, value in self.param_bounds.items():
                current_inputs[key] = random.uniform(value[0], value[1])

            current_loss = self.function(current_inputs)

            for j in range(self.keep_top_k):
                if current_loss > self.min_losses[j]['loss']:
                    self.min_losses[j]['loss'] = current_loss
                    self.min_losses[j]['hyperparameters'] = current_inputs
                    break

        return self.min_losses[0]

    def get_top_k(self, k=None):
        if k is None:
            return self.min_losses
        elif type(k) is int:
            return self.min_losses[0:k]
        else:
            print("k must be an integer")
            return None
            
if __name__ == '__main__':
    bounds = {'x0': [-10, 10], 'x1': [-10, 10]}
    moo = RandomOptimizer(holder_table, bounds)
    z = moo.minimize(600)
    h = moo.get_top_k()
    for b in h:
        print(b)
