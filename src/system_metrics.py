from abc import ABC, abstractmethod


class SystemMetrics(ABC):
    @abstractmethod
    def update(self):
        pass
