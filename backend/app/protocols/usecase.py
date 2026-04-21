from abc import ABC, abstractmethod


class UseCase[INPUT, OUTPUT](ABC):
    @abstractmethod
    def execute(self, input: INPUT) -> OUTPUT:
        pass
