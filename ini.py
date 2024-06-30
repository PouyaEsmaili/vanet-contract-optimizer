import numpy as np

def calculate_total_resource(delta_min, delta_max, type_probability, total_vehicles):
    total_types = len(type_probability)
    subintervals = np.linspace(delta_min, delta_max, total_types + 1)

    # Generate totalResource values for each vehicle
    weighted_resources = []
    for _ in range(total_vehicles):
        total_resources = []
        for i in range(total_types):
            # Select a random value within the subinterval
            value = np.random.uniform(subintervals[i], subintervals[i + 1])
            total_resources.append(value)
        weighted_resources.append(np.random.choice(total_resources, p=type_probability))
    return weighted_resources

# Example usage
delta_min = 2
delta_max = 15
type_probability = [0.010081010821254819, 0.013278733115701241, 0.017137444089193647,
                    0.021670668408513345, 0.02684945101122729, 0.03259382734688505,
                    0.03876788947018423, 0.04517995601557748, 0.051588903387264844,
                    0.05771698494640697, 0.06326854153073262, 0.06795303486500145,
                    0.07150999362924623, 0.07373292594962233, 0.0744891544921788,
                    0.07373292594962233, 0.07150999362924623, 0.06795303486500145,
                    0.06326854153073262, 0.05771698494640697]
total_vehicle = 20

# Calculate the total resources
weighted_resources = calculate_total_resource(delta_min, delta_max, type_probability, total_vehicle)

# Format the output for the ini file
ini_format = "\n".join(f"**.vehicles[{i}].totalResource = {weighted_resources[i]}" for i in range(len(weighted_resources)))
print(ini_format)