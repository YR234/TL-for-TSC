from abc import ABC, abstractmethod


class Feature(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def compute_feature(self, sequence):
        pass
    
    
