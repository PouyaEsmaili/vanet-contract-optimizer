from flask import Flask, request
from scipy.optimize import minimize, LinearConstraint, Bounds
import numpy as np

app = Flask(__name__)

# unit_benefit: r_BS
# computation_capability: \delta_BS
# duration: T
# type_probability: \lambda_k

def base_station_utility(delta, pie, total_vehicles, unit_benefit, computation_capability, duration, type_probability):
    benefit = unit_benefit * duration * delta / (delta + computation_capability)
    utility = total_vehicles * np.sum(type_probability * (benefit - pie))
    return utility


def base_station_utility_factory(total_vehicles, unit_benefit, computation_capability, duration, type_probability):
    def func(x):
        total_types = np.size(x) // 2
        delta = x[:total_types]
        pie = x[total_types:]
        return -base_station_utility(delta, pie, total_vehicles, unit_benefit, computation_capability, duration, type_probability)

    return func


@app.route('/', methods=['POST'])
def optimize():
    data = request.get_json()
    unit_benefit = data['unit_benefit']
    computation_capability = data['computation_capability']
    duration = data['duration']
    type_probability = np.array(data['type_probability'])
    total_types = np.size(type_probability)
    total_vehicles = data['total_vehicles']
    delta_min = data['delta_min']
    delta_max = data['delta_max']

    theta = [
        delta_min + k / total_types * (delta_max - delta_min)
        for k in range(total_types)
    ]
    constraints = [
        {'type': 'eq', 'fun': lambda x: theta[0] * x[total_types] - x[0]},
    ] + [
        {'type': 'eq', 'fun': lambda x: -x[k] + x[k - 1] + theta[k] * (x[total_types + k] - x[total_types + k - 1])}
        for k in range(1, total_types)
    ] + [
        {'type': 'ineq', 'fun': lambda x: x[k] - x[k-1] if k > 0 else x[k]}
        for k in range(total_types)
    ] + [
        {'type': 'ineq', 'fun': lambda x: theta[k] - x[k]}
        for k in range(total_types)
    ]

    f = base_station_utility_factory(total_vehicles, unit_benefit, computation_capability, duration, type_probability)
    result = minimize(f, np.random.random(2 * total_types), method='SLSQP', constraints=constraints)
    delta = result.x[:total_types]
    pie = result.x[total_types:]
    print(result)
    return {
        'delta': delta.tolist(),
        'pie': pie.tolist(),
        'utility': -result.fun,
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0')
