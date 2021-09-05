from utils.Feature import Feature
from itertools import combinations
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import time


def get_all_possible_combinations(feature_set):
    return sum([list(map(list, combinations(feature_set, i))) for i in range(len(feature_set) + 1)], [])


def get_all_possible_combinations_for_10th():
    feature_set = [Maximum(),Minimum(), STD(), CrossMean(), Peaks()]
    return feature_set

def create_regression_tasks2(y_samples, feature_set):
    possible_combinations = get_all_possible_combinations(feature_set)
    print(possible_combinations)
    return 


def create_regression_tasks(y_samples, feature_set):
    possible_combinations = get_all_possible_combinations(feature_set)
    y_train, y_train_combinations = [], []
    y_samples_flatten = y_samples.reshape(y_samples.shape[0],y_samples.shape[1])
    # For runtime saving - calculate each feature result only once and the concat if necessary
    feat_dic = {}
    for feature in feature_set:
        start = time.time()
        feat_dic[feature] = []
        y_true = []
        print("Computing feature {}".format(feature))
        for y_sample in y_samples_flatten:
            curr_feat = feature.compute_feature(y_sample.tolist())
            y_true.append(curr_feat)
        feat_dic[feature] = y_true

    for idx, comb in enumerate(possible_combinations):
        if len(comb) < 1:
            continue
        
        if idx % 10 == 0:
            print("{}/{}".format(idx,len(possible_combinations)))
        current_comb = []
        this_zip = []
        for feature in comb:
            this_zip.append(feat_dic[feature])
        for tup in list(zip(*this_zip)):
            y_true = []
            for val in tup:
                if type(val) == list:
                    y_true += curr_feat
                else:   
                    y_true.append(val)
            current_comb.append(y_true)
        y_train_combinations.append(current_comb)
    y_train_combinations = np.array(y_train_combinations)
    return y_train_combinations


def create_classification_tasks(x, seqs):
    dic = {i: val for i,val in enumerate(seqs)}
    desc_dic = {val: i for i,val in enumerate(set(seqs))}
    num_classes = len(seqs)
    num_samples = int(x.shape[0]/num_classes)
    print(num_classes)
    print(num_samples)
    y = []
    for i in range(x.shape[0]):
        label = [0 for j in range(len(desc_dic))]
        curr_label = desc_dic[dic[int(i/num_samples)]]
        label[curr_label] = 1
        y.append(label)
    return np.array(y)


def create_regression_tastks_no_multi(y_samples, feature_set):
    y_s = [[] for i in range(y_samples.shape[0])]
    for idx, y_sample in enumerate(y_samples):
        for feature in feature_set:
            curr_feat = feature.compute_feature(y_sample.squeeze().tolist())
            if type(curr_feat) != list:
                curr_feat = [curr_feat]
            y_s[idx] += curr_feat

    return np.array([np.array(y) for y in y_s])


class Maximum(Feature):

    # overriding abstract method
    def compute_feature(self, sequence):
        return max(sequence)


class Minimum(Feature):

    # overriding abstract method
    def compute_feature(self, sequence):
        return min(sequence)


class STD(Feature):

    # overriding abstract method
    def compute_feature(self, sequence):
        return np.std(sequence)
    
class Peaks(Feature):

    # overriding abstract method
    def compute_feature(self, sequence):
        # prominence
        peaks, _ = find_peaks(sequence, prominence=0.1)
        return len(peaks)


class CrossMean(Feature):

    # overriding abstract method
    def compute_feature(self, sequence):
        mean = np.mean(sequence)
        crosses = 0
        for i in range(len(sequence) - 1):
            if sequence[i] < mean < sequence[i + 1]:
                crosses += 1
            if sequence[i + 1] < mean < sequence[i]:
                crosses += 1
        return crosses
    
    
class Split10th(Feature):
    
     # overriding abstract method
    def compute_feature(self, sequence):
        regressions = []
        m = len(sequence) // 10
        splits = [sequence[i:i+m] for i in range(0, len(sequence), m)]
        tasks = get_all_possible_combinations_for_10th()
        for split in splits[:-1]:
            current_regressions = []
            for task in tasks:
                current_regressions.append(task.compute_feature(split))
            regressions += current_regressions
        return regressions
    
    
    
class summing_up(Feature):
    
    # overriding abstract method
    def compute_feature(self, sequence):
        return np.sum(sequence)