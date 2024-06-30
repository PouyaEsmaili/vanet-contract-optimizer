import requests
import json
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import norm


def discrete_normal_distribution(mean, std_dev):
    # Define the range of X
    x = np.arange(1, 21)

    # Create a normal distribution
    normal_distribution = norm.pdf(x, mean, std_dev)

    # Normalize the distribution so that the sum is 1
    probabilities = normal_distribution / normal_distribution.sum()

    return list(probabilities)


def shared_computation_resource(delta, type_probability, total_vehicles):
    return np.sum(np.array(delta) * np.array(type_probability)) * total_vehicles


def rewards(pie, type_probability, total_vehicles):
    return np.sum(np.array(pie) * np.array(type_probability) * total_vehicles)


def test(
        unit_benefit=1,
        computation_capability=5,
        duration=100,
        type_probability=None,
        total_vehicles=20,
        delta_min=2,
        delta_max=15,
):
    data = {
        'unit_benefit': unit_benefit,
        'computation_capability': computation_capability,
        'duration': duration,
        'type_probability': type_probability,
        'total_vehicles': total_vehicles,
        'delta_min': delta_min,
        'delta_max': delta_max,
    }
    headers = {
        'Content-Type': 'application/json'
    }
    json_data = json.dumps(data)
    resp = requests.post('http://localhost:9090', data=json_data,
                         headers=headers).json()
    delta = resp['delta']
    pie = resp['pie']
    scr = shared_computation_resource(delta, type_probability, total_vehicles)
    r = rewards(pie, type_probability, total_vehicles)
    return delta, pie


def main():
    delta_min = 2
    delta_max = 15
    deltas = []
    pies = []
    # for mean in range(9, 11):
    # for std_dev in np.arange(2, 5, 0.5):
    mean = 15
    std_dev = 7
    delta, pie = test(
        type_probability=discrete_normal_distribution(mean, std_dev),
        delta_min=delta_min,
        delta_max=delta_max,
    )
    deltas.append(np.array(delta))
    pies.append(np.array(pie))

    plt.plot(range(1, 21), np.average(deltas, axis=0), label=str(std_dev))
    plt.legend()
    plt.show()
    print(','.join([str(x) for x in discrete_normal_distribution(mean, std_dev)]))


if __name__ == '__main__':
    main()
