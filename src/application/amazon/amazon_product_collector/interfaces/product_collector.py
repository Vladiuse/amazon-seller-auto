from abc import ABC, abstractmethod


class IAmazonProductsCollector(ABC):

    @abstractmethod
    def collect(self, list):
        pass