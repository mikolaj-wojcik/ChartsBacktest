def get_gross(transactions):
    total_profit = 0
    total_loss = 0

    for transaction in transactions:
         if transaction.profit > 0:
            total_profit += transaction.profit
         elif transaction.profit < 0:
             total_loss += transaction.profit

    return total_profit, total_loss

def get_gross_profit(transactions):
    total_profit = 0
    for transaction in transactions:
        if transaction.profit > 0:
            total_profit += transaction.profit
    return round(float(total_profit),2)

def get_gross_loss(transactions):
    total_loss = 0
    for transaction in transactions:
        if transaction.profit < 0:
            total_loss += transaction.profit
    return round(float(total_loss),2)

def get_profit_factor(transactions):

    gross_profit, gross_loss = get_gross(transactions)
    return float(round(gross_profit / (abs(gross_loss) if gross_loss != 0 else 1), 2))

def get_net_profit(transactions):
    gross_profit, gross_loss = get_gross(transactions)
    comission = get_total_comission(transactions)
    return float(round(gross_profit + gross_loss - comission, 2))
    pass


def get_total_trades(transactions):
    return len(transactions)
    pass

def get_total_comission(transactions):
       total_comission = 0
       for transaction in transactions:
           total_comission += transaction.commission

       return total_comission


def get_total_buying(transactions):
    return len(list(filter(lambda x: (x.size > 0), transactions)))

    pass