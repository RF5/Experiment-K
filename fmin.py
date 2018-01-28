import numpy as np
import random
from math import sin, cos, exp, sqrt, pi
import dlib

def holder_table(x0,x1):
    return -abs(sin(x0)*cos(x1)*exp(abs(1-sqrt(x0*x0+x1*x1)/pi)))

def minimize(function, param_bounds, iterations):

    psi = 1e6
    points = []
    n_params = len(param_bounds)
    K = np.eye(n_params)
    sigmas = []

    initial_inputs = [ (a + b) / 2 + 0.1 for a, b in param_bounds]
    scimin_bounds = [(a, b) for a, b in param_bounds]
    sigmas += [1]
    current_inputs = initial_inputs
    # points are in format (inputs, f(inputs)) as a list item for each point

    
    for i in range(iterations * 2):
        points += [(current_inputs, -1 * function(*current_inputs))]

        if i % 2 == 0:
            # Do maxLIPO
            
            cons = (
                {'type': 'ineq', 'fun': lambda x: np.amin(x[0:K.shape[0]])},
                {'type': 'ineq', 'fun': lambda x: min(x[K.shape[0]:])},
                {'type': 'ineq', 'fun': lambda x: min([upper_bound(point[0], points, k=np.diag(x[0:K.shape[0]]), 
                    sigmas=x[K.shape[0]:]) - point[1] for ind, point in enumerate(points)])}
            )
            
            x0 = [0.01] * (K.shape[0] + len(sigmas))

            def k_estim_func(x):
                inner_k = np.diag(x[0:K.shape[0]])
                inner_sigmas = x[K.shape[0]:]
                kaka = np.square(np.linalg.norm(inner_k)) + psi * np.sum(np.square(inner_sigmas))
                return kaka

            res = scimin(k_estim_func, x0, constraints=cons)
            print("RES: ", res.x)
            tmp = res.x
            K = np.diag(np.asarray(tmp[0:K.shape[0]]))
            sigmas = tmp[K.shape[0]:]
            print(res.success)
            print(res.message)
            
            # Now find maximum upper bound for next point:
            if i > 1:
                def lipo_func(x):
                    # minimize - upper_bound
                    return -1 * upper_bound(x, points, K, np.asarray(sigmas))

                x02 = current_inputs

                res2 = scimin(lipo_func, x02, bounds=scimin_bounds)
                print("RES 2 = ", res2.x)
                print(res2.success)
                print(res2.message)
            else:
                current_inputs = [random.uniform(a, b) for a, b in param_bounds]
            
        else:
            # do trust region bound optimization
            # do it with SLSQP
            
            max_output = float('-inf')
            max_input = None

            for point in points:
                if point[1] > max_point:
                    max_point = point[1]
                    max_input = point[0]

    return 0, 0


def upper_bound(x, points, k, sigmas):
    zeta = [point[1] + np.sqrt(sigmas[i] + np.matmul(np.matmul(np.transpose(np.asarray(x) - 
        np.asarray(point[0])), k), (np.asarray(x) - np.asarray(point[0])))) for i, point in enumerate(points)]
    
    ub = min(zeta)
    return ub


if __name__ == '__main__':
    # pairs of [min, max]
    hyperparam_bounds = [[-10, 10], [-10, 10]]
    #x, y = minimize(holder_table, hyperparam_bounds, 5)
    tracker = dlib.correlation_tracker()
    
    x, y = dlib.find_min_global(holder_table, 
                           [-10,-10],  # Lower bound constraints on x0 and x1 respectively
                           [10,10],    # Upper bound constraints on x0 and x1 respectively
                           80)         # The number of times find_min_global() will call holder_table()

    print("x = ", x)
    print("y = ", y)
