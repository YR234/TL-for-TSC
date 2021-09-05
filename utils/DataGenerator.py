import random
import math
import numpy as np
from abc import ABC, abstractmethod


def get_step_size(item, last_x):
    if item[0] == "Si":
        return math.sin(last_x / item[2])
    mul = 0 if item[0] == "S" else 1 if item[0] == "U" else -1
    return math.tan(math.pi * item[2] / 180) * mul


def get_std_addition(step_size, std, line_type):
    # for check if it will be plus or minus
    rnd = random.random()
    mul = 1 if rnd > 0.5 else -1
    std = round(random.uniform(0, std), 2)
    if line_type == "S":
        step_size = 1
    return step_size * std * mul


def get_cycle(cycles, cycles_distribution):
    return "cycle{}".format(random.choices([i for i in range(len(cycles))], cycles_distribution)[0])


def get_item_by_i(i, cycle_length, curr_cycle):
    ranges = [0]
    for item in curr_cycle:
        ranges.append(ranges[-1] + int(cycle_length * item[1]))
    for j in range(len(ranges)-1):
        if ranges[j] <= i < ranges[j + 1]:
            return curr_cycle[j]
    return curr_cycle[-1]


def get_item(in_cycle_randomisation, curr_cycle, i, cycle_length):
    cycle_distribution = [item[1] for item in curr_cycle]
    if not in_cycle_randomisation:
        return get_item_by_i(i, cycle_length, curr_cycle)
    return random.choices(curr_cycle, cycle_distribution)[0]


def generate(seq_length, num_cycles, std, starting_point, cycles, cycles_distribution, y_max_value,
             in_cycle_randomisation):
    """

    :int seq_length: sequence length
    :int cycles: number of cycles in the sequence
    :dict instructions: the dictionary should have the following structure:
    {
    "std": float. what std to use for the line. in case of straight line use 0

    "starting_point": list. the list should contain 2 numbers [from,to] - we randomize float number, with up
    to 2 digits. Y.XX

    "cycle1" : list of list. each node contains: [line_type (str), percentage (float), angle (float).
    here are the options for the values for cycle ["u"/"d"/"s" - up, down. straight, [0,1], [0-90]]
    for example: I want a line the goes in an angle of 45 up half of the way, and
    then 45 down half of the way. the cycle should look like this:
     /\
    /  \
    the values should be:
    "cycle0": [["U", 0.5, 45], ["D", 0.5, 45]]

    "cycle_distribution": list. in case I want cycle1 to occur 30% of the time and cycle 2 should be 70% of
     the time you should have the following list: [0.3, 0.7].
     for example in sequence length 100, with 10 cycles, and you wrote two different cycles, you will get
     3 cycles and 7 cycles in a random order.

    }
    """

    cycle_length = int(seq_length / num_cycles)
    starting_point = round(random.uniform(starting_point[0], starting_point[1]), 2)
    x, y = [0], [starting_point]
    for cycle_num in range(num_cycles):
        cycle = (get_cycle(cycles, cycles_distribution))
        for j in range(cycle_length):
            item = get_item(in_cycle_randomisation, cycles[cycle], j, cycle_length)
            step_size = get_step_size(item, x[-1])
            std_addition = get_std_addition(step_size, std, item[0])
            y.append(y[-1] + step_size + std_addition)
            x.append(x[-1] + 1)
    y_max_value = round(random.uniform(y_max_value[0], y_max_value[1]), 2)
    divide = max(math.fabs(max(y)), math.fabs(min(y)))
    if divide == 0:
        print(y)
        print(y_max_value)
        divide = y_max_value/2
    normalize = math.fabs(y_max_value / divide)
    normalized_y = [normalize * item for item in y]
    if len(normalized_y) < seq_length:
        for i in range(seq_length - len(normalized_y)):
            normalized_y.append(y[-1])
    return normalized_y[:seq_length]


def create_synthetic_data(kwargs):
    num_samples = kwargs["num_samples"]
    del kwargs["num_samples"]
    y_s = []
    for i in range(num_samples):
        y = generate(**kwargs)
        y_s.append(y)
    y_samples = np.array(y_s).reshape(len(y_s), len(y_s[0]), 1)
    return y_samples

    
class SequenceType(ABC):
    def __init__(self, num_samples, seq_length, num_cycles, std, starting_point, y_max_value):
        self.num_samples = num_samples
        self.seq_length = seq_length
        self.num_cycles = num_cycles
        self.std = std
        self.starting_point = starting_point
        # Change this to more than 1 option - maybe change to range
        self.y_max_value = y_max_value

    @abstractmethod
    def cycle_behavior(self):
        pass

    def generate_data(self):
        cycle_data = self.cycle_behavior()
        kwargs = {
            "num_samples": self.num_samples,
            "seq_length": self.seq_length,
            "num_cycles": self.num_cycles,
            "std": self.std,
            "starting_point": self.starting_point,
            # Change this to more than 1 option - maybe change to range
            "y_max_value": self.y_max_value,
            "in_cycle_randomisation": cycle_data["in_cycle_randomisation"],
            "cycles": cycle_data["cycles"],
            "cycles_distribution": cycle_data["cycles_distribution"]
        }
        return create_synthetic_data(kwargs)
