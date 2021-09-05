from utils.DataGenerator import SequenceType
import random
from random import randrange, choices, randint

def generate_random_kwargs(seq_lengths, num_cycles, std, starting_point, y_max_value):
    return {
    'num_samples': 1,
    'seq_length': randint(seq_lengths[0], seq_lengths[1]),
    'num_cycles': randint(num_cycles[0], num_cycles[1]),
    'std': randint(std[0]*100, std[1]*100) / 100 ,
    'starting_point': starting_point,
    'y_max_value': y_max_value}


def generate_cycles_dic():
    cycles_dic = {}
    cycles = choices([1, 2], [1/3, 2/3])[0]
    cycle_distribution = [randrange(1, 3) for k in range(cycles)]
    cycle_distribution = [x / sum(cycle_distribution) for x in cycle_distribution]
    for i in range(cycles):
        items_in_cycle = randrange(1, 8)
        dis = [randrange(1, 10) for k in range (items_in_cycle)]
        dis = [x/sum(dis) for x in dis]
        curr_item_list = []
        for j in range(items_in_cycle):
            slope = choices(["D", "U", "S"], [1/3, 1/3, 1/3])[0]
            angle = randrange(1, 90)
            curr_dis = dis[j]
            item = [slope, curr_dis, angle]
            curr_item_list.append(item)
        cycles_dic["cycle{}".format(i)] = curr_item_list
    return cycles_dic, cycle_distribution, randrange(0, 2)


def generate_cycles_dic_crazy():
    cycles_dic = {}
    cycles = 1
    cycle_distribution = [randrange(1, 3) for k in range(cycles)]
    cycle_distribution = [x / sum(cycle_distribution) for x in cycle_distribution]
    for i in range(cycles):
        items_in_cycle = randrange(10, 15)
        dis = [randrange(1, 10) for k in range (items_in_cycle)]
        dis = [x/sum(dis) for x in dis]
        curr_item_list = []
        for j in range(items_in_cycle):
            slope = choices(["D", "U", "S", "SI"], [1/4, 1/4, 1/4, 1/4])[0]
            angle = randrange(1, 90)
            curr_dis = dis[j]
            item = [slope, curr_dis, angle]
            curr_item_list.append(item)
        cycles_dic["cycle{}".format(i)] = curr_item_list
    return cycles_dic, cycle_distribution, randrange(0, 2)


def get_all_classes():
    return ["StraightLine", "HighPeak", "Up"
            , "Down", "UpAndDown", "UpAndDownAndNormal"
            , "SmallUpHighDownAndNormal", "SmallDownHighUpAndNormal", "SinWave"
            , "RandomWaveVersion", "RandomWaveVersion", "RandomWaveVersion", "ECG200", "Traffic",
           "CrazyRandom", "CrazyRandom"]


class StraightLine(SequenceType):

    def __init__(self, num_samples, seq_length, num_cycles, std, starting_point, y_max_value):
        super(StraightLine, self).__init__(num_samples, seq_length, num_cycles, std, starting_point, y_max_value)

    def cycle_behavior(self):
        return {
            "in_cycle_randomisation": False,
            "cycles": {
                "cycle0": [["S", 1, 0]]
            },
            "cycles_distribution": [1]
        }


class HighPeak(SequenceType):

    def __init__(self, num_samples, seq_length, num_cycles, std, starting_point, y_max_value):
        super(HighPeak, self).__init__(num_samples, seq_length, num_cycles, std, starting_point, y_max_value)

    def cycle_behavior(self):
        return {
            "in_cycle_randomisation": False,
            "cycles": {
                "cycle0": [["S", 0.4, 80], ["U", 0.1, 70], ["D", 0.1, 70], ["S", 0.4, 80]],
                "cycle1": [["S", 1, 0]]
            },
            "cycles_distribution": [0.7, 0.3]
        }


class Up(SequenceType):

    def __init__(self, num_samples, seq_length, num_cycles, std, starting_point, y_max_value):
        super(Up, self).__init__(num_samples, seq_length, num_cycles, std, starting_point, y_max_value)

    def cycle_behavior(self):
        angle = randrange(1, 90)
        return {
            "in_cycle_randomisation": False,
            "cycles": {
                "cycle0": [["U", 1, angle]]
            },
            "cycles_distribution": [1]
        }


class Down(SequenceType):

    def __init__(self, num_samples, seq_length, num_cycles, std, starting_point, y_max_value):
        super(Down, self).__init__(num_samples, seq_length, num_cycles, std, starting_point, y_max_value)

    def cycle_behavior(self):
        angle = randrange(1, 90)
        return {
            "in_cycle_randomisation": False,
            "cycles": {
                "cycle0": [["D", 1, angle]]
            },
            "cycles_distribution": [1]
        }


class UpAndDown(SequenceType):

    def __init__(self, num_samples, seq_length, num_cycles, std, starting_point, y_max_value):
        super(UpAndDown, self).__init__(num_samples, seq_length, num_cycles, std, starting_point, y_max_value)

    def cycle_behavior(self):
        angle = randrange(1, 90)
        return {
            "in_cycle_randomisation": False,
            "cycles": {
                "cycle0": [["U", 0.5, angle], ["D", 0.5, angle]]
            },
            "cycles_distribution": [1]
        }


class UpAndDownAndNormal(SequenceType):

    def __init__(self, num_samples, seq_length, num_cycles, std, starting_point, y_max_value):
        super(UpAndDownAndNormal, self).__init__(num_samples, seq_length, num_cycles, std, starting_point, y_max_value)

    def cycle_behavior(self):
        angle = randrange(1, 90)
        return {
            "in_cycle_randomisation": False,
            "cycles": {
                "cycle0": [["D", 0.15, angle], ["U", 0.3, angle], ["D", 0.15, angle], ["S", 0.4, angle]]
            },
            "cycles_distribution": [1]
        }


class SmallUpHighDownAndNormal(SequenceType):

    def __init__(self, num_samples, seq_length, num_cycles, std, starting_point, y_max_value):
        super(SmallUpHighDownAndNormal, self).__init__(num_samples, seq_length, num_cycles, std, starting_point,
                                                       y_max_value)

    def cycle_behavior(self):
        angle = randrange(50, 90)
        return {
            "in_cycle_randomisation": False,
            "cycles": {
                "cycle0": [["U", 0.1, angle], ["D", 0.3, angle], ["U", 0.2, angle], ["S", 0.4, angle]]
            },
            "cycles_distribution": [1]
        }


class SmallDownHighUpAndNormal(SequenceType):

    def __init__(self, num_samples, seq_length, num_cycles, std, starting_point, y_max_value):
        super(SmallDownHighUpAndNormal, self).__init__(num_samples, seq_length, num_cycles, std, starting_point,
                                                       y_max_value)

    def cycle_behavior(self):
        angle = randrange(50, 90)
        return {
            "in_cycle_randomisation": False,
            "cycles": {
                "cycle0": [["D", 0.1, angle], ["U", 0.3, angle], ["D", 0.2, angle], ["S", 0.4, angle]]
            },
            "cycles_distribution": [1]
        }


class SinWave(SequenceType):

    def __init__(self, num_samples, seq_length, num_cycles, std, starting_point, y_max_value):
        super(SinWave, self).__init__(num_samples, seq_length, num_cycles, std, starting_point, y_max_value)

    def cycle_behavior(self):
        rand = randrange(10, 100)/100
        divider = rand * self.seq_length / 10
        return {
            "in_cycle_randomisation": False,
            "cycles": {
                "cycle0": [["Si", 1, divider]]
            },
            "cycles_distribution": [1]
        }


class RandomWaveVersion(SequenceType):

    def __init__(self, num_samples, seq_length, num_cycles, std, starting_point, y_max_value):
        super(RandomWaveVersion, self).__init__(num_samples, seq_length, num_cycles, std, starting_point, y_max_value)

    def cycle_behavior(self):
        cycles, cycle_distribution, randomisation = generate_cycles_dic()
        return {
            "in_cycle_randomisation": randomisation,
            "cycles": cycles,
            "cycles_distribution": cycle_distribution
        }
    
    
class CrazyRandom(SequenceType):

    def __init__(self, num_samples, seq_length, num_cycles, std, starting_point, y_max_value):
        super(CrazyRandom, self).__init__(num_samples, seq_length, num_cycles, std, starting_point, y_max_value)

    def cycle_behavior(self):
        cycles, cycle_distribution, randomisation = generate_cycles_dic_crazy()
        return {
            "in_cycle_randomisation": randomisation,
            "cycles": cycles,
            "cycles_distribution": cycle_distribution
        }
    
    
class ECG200(SequenceType):

    def __init__(self, num_samples, seq_length, num_cycles, std, starting_point, y_max_value):
        super(ECG200, self).__init__(num_samples, seq_length, num_cycles, std, starting_point,
                                                       y_max_value)

    def cycle_behavior(self):
        cycles = self.CreateECG200()
        return {
            "in_cycle_randomisation": False,
            "cycles": {
                "cycle0": cycles
            },
            "cycles_distribution": [1]
        }
    
    def CreateECG200(self):
        cycles = []
        prec = 0
        prec += round(random.uniform(0.04, 0.08), 2)
        hard_angle = randrange(70, 85)
        cycles.append(["U", prec, hard_angle])
        hard_angle = randrange(70, 85)
        cycles.append(["D", 0.18 - prec, hard_angle])
        prec = 0.18
        med_angle = randrange(25,35)
        curr_prec = round(random.uniform(0.15, 0.2), 2)
        prec += curr_prec
        cycles.append(["D",curr_prec, med_angle])
        med_angle = randrange(30,45)
        curr_prec = round(random.uniform(0.25, 0.35), 2)
        prec += curr_prec
        cycles.append(["U",curr_prec, med_angle])
        curr_prec = 1 - prec
        prec = 1
        slope = "U" if randrange(1,3) ==1 else "D"
        low_ange = randrange(0,15)
        cycles.append([slope,curr_prec, low_ange])
        return cycles
    
    
        
class Traffic(SequenceType):

    def __init__(self, num_samples, seq_length, num_cycles, std, starting_point, y_max_value):
        super(Traffic, self).__init__(num_samples, seq_length, num_cycles, std, starting_point,
                                                       y_max_value)

    def cycle_behavior(self):
        cycles = self.CreateTraffic()
        return {
            "in_cycle_randomisation": False,
            "cycles": {
                "cycle0": cycles
            },
            "cycles_distribution": [1]
        }
    
    def create_rounded(self,cycles,starting_angle, end_angle, steps, step_size, slope):
        angle_step = end_angle / steps
        for i in range(steps):
            cycles.append([slope, step_size, starting_angle + angle_step*i])
        return cycles
   
    def CreateTraffic(self):
        cycles = []
        prec = 0
        prec += round(random.uniform(0.3, 0.4), 2)
        low_angle = randrange(0,15)
        cycles.append(["D", prec, low_angle])
        high_angle = randrange(75,85)
        cycles = self.create_rounded(cycles,0, high_angle, 10, 0.02, "U")
        med_angle = randrange(10,45)
        cycles.append(["D", 0.1, med_angle])
        med_angle = randrange(10,45)
        cycles.append(["U", 0.1, med_angle])
        last_down = 1 - prec
        med_angle = randrange(35,55)
        cycles.append(["D",last_down, med_angle])
        return cycles


    
class Paper(SequenceType):

    def __init__(self, num_samples, seq_length, num_cycles, std, starting_point, y_max_value):
        super(Paper, self).__init__(num_samples, seq_length, num_cycles, std, starting_point,
                                                       y_max_value)

    def cycle_behavior(self):
        angle = 45
        rand = randrange(10, 100)/100
        divider = rand * self.seq_length / 10
        return {
            "in_cycle_randomisation": False,
            "cycles": {
                "cycle0": [["D", 0.25, angle], ["U", 0.25, angle], ["Si", 0.25, divider], ["S", 0.25, angle]]
            },
            "cycles_distribution": [1]
        }
    
    
class UpStraight(SequenceType):

    def __init__(self, num_samples, seq_length, num_cycles, std, starting_point, y_max_value):
        super(UpStraight, self).__init__(num_samples, seq_length, num_cycles, std, starting_point,
                                                       y_max_value)

    def cycle_behavior(self):
        return {
            "in_cycle_randomisation": False,
            "cycles": {
                "cycle0": [["U", 0.5, 45], ["S", 0.5, 0]]
            },
            "cycles_distribution": [1]
        }