class totalcomission:
    __name__ = 'Total comission'
    def __init__(self):
        pass

    def calculate(self, args_dict):
        history = args_dict['transactions']
        total_comission = 0
        for transaction in history:
            total_comission += transaction.commission

        return total_comission


