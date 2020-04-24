from .fifo_device import FIFODevice
from .utility import transfer_rate_to_bps


class ComputationDevice(FIFODevice):
    def __init__(self, name, performance='0bps'):
        '''Init a CalculationDevice with calculation performance

        Args:
            performance: a string representing calculating performance.
                         e.g. '16Gibps'
        '''
        super().__init__(name)
        self.__performance = transfer_rate_to_bps(performance)  # Stored in bps

    def get_performance(self):
        '''Return the performance in bps
        '''
        return self.__performance


class CPU(ComputationDevice):
    def __init__(self, name, performance='0bps'):
        '''Init a CPU with calculation performance

        Args:
            performance: a string representing calculating performance.
                         e.g. '16Gibps'
        '''
        super().__init__(name, performance)


class GPU(ComputationDevice):
    def __init__(self, name, performance='0bps'):
        '''Init a GPU with calculation performance and transfer rates

        Args:
            performance: a string representing calculating performance.
                         e.g. '16Gibps'
        '''
        super().__init__(name, performance)
