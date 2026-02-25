from abc import ABC, abstractmethod


class IAmazonRequestSender(ABC):

    @abstractmethod
    def get(self, url: str) -> bytes:
        raise NotImplementedError
