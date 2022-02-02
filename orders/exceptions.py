class OutOfStockError(Exception):
    def __init__(self):
        super().__init__('OUT_OF_STOCK')

class LackOfPointError(Exception):
    def __init__(self):
        super().__init__('LACK_OF_POINTS')