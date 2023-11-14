import requests
import json


def test(
        unit_benefit=1,
        computation_capability=2,
        duration=10,
        type_probability=None,
        total_vehicles=10,
        delta_min=1,
        delta_max=16,
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
                         headers=headers)
    print(resp.text)


if __name__ == '__main__':
    test(type_probability=[1 / 5] * 5)
