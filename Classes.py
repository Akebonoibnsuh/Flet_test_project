from tinkoff.invest import Client


INVEST_TOKEN="___"

class TinkoffInvestClient:
    def __init__(self, token):
        self.token = token
        self.client = Client(token)
        self.get_accounts_id = self.get_accounts_id()

    def get_accounts_id(self):
        account_id = []
        with Client(self.token) as client:
            response = client.users.get_accounts()
            for r_account in response.accounts:
                account_id.append(r_account.id)
        return  account_id # ['2075449744', '2158156364', '2158156455']

    def get_positionts(self, account_id):
        # print(f" счет №: {account_id}")
        with Client(self.token) as client:
            response_getpositions = client.operations.get_positions(account_id=account_id)
        return response_getpositions


    def get_money_positions(self, response_getpositions):
        money_dict = {}  # Словарь для хранения значений денег
        for money_value in response_getpositions.money:
            units = money_value.units
            nano = money_value.nano
            total_value = units + nano / 1e9  # Переводим nano в единицы
            currency = money_value.currency
            money_dict[currency] = total_value
        return money_dict


    def get_security_positions(self, response_getpositions):
        securities_dict = {}  # Словарь для хранения значений акций
        for securities in response_getpositions.securities:
            figi = securities.figi
            balance = securities.balance
            securities_dict[figi] = balance
        return securities_dict



#
# client_r = TinkoffInvestClient(INVEST_TOKEN)
# # print(client_r.get_positionts('2075449744'))
# print(client_r.get_accounts_id)
#
# for acc in client_r.get_accounts_id:
#     r_position = client_r.get_positionts(acc)
#     print(client_r.get_money_positions(r_position))
#     print(client_r.get_security_positions(r_position))






