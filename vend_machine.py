class VENDMACHINE():

    def __init__(self, init_state):
        self.shelves = init_state['shelves']
        self.account = init_state['account']
        self.height = len(self.shelves)
        self.width = len(self.shelves[0])
        self.customer_account = init_state['customer_account']

    def put_in(self, name: str, price: float, qty: int, x: int, y: int) -> bool:
        if (y > self.height - 1) or (x > self.width - 1):
            return False

        if self.shelves[y][x] is None:
            item = {'name': name, 'price': price, 'qty': qty}
            self.shelves[y][x] = item
            return True
        else:
            return False

    def purchase(self, x: int, y: int) -> bool:

        if (y > self.height - 1) or (x > self.width - 1):  # if wrong x and y
            print(f'wrong {x=}, {y=}')
            return False

        if self.shelves[y][x] is None:  # if selected box is empty
            print(f'box {x=},{y=} empty')
            return False

        if self.customer_account['cash_now'] < self.shelves[y][x]['price']:  # if not enought money
            print('not enoght money')
            return False

        self.customer_account['cash_now'] -= self.shelves[y][x]['price']
        self.shelves[y][x]['qty'] -= 1

        if self.shelves[y][x]['qty'] == 0:
            self.shelves[y][x] = None

    def add_money(self, cash_sum: float) -> float:
        # print(f'putting ${cash_sum} money')
        self.customer_account['cash_now'] += cash_sum
        return self.customer_account['cash_now']

    def take_moneyback(self) -> float:
        self.customer_account['cash_now'] = 0
        return True

    def showcase(self):
        for shelf in self.shelves:
            shelf_view_1 = ''
            shelf_view_2 = ''
            shelf_view_3 = ''

            for box in shelf:
                if box is not None:
                    item = box.get('name')
                    price = '$' + str(box.get('price'))
                    qty = str(box.get('qty'))
                    info = price + ': x' + qty
                    separator = '|------------'
                else:
                    item = 'none'
                    info = ''
                shelf_view_1 += f'  |  {item: <10}'
                shelf_view_2 += f'  |  {info: <10}'
                shelf_view_3 += f'  {separator:<10}'

            print(shelf_view_1 + '|')
            print(shelf_view_2 + '|')
            print(shelf_view_3 + '|')
        print(f'\nEarned  money: ${self.account["total_sum"]}')            
        print(f'Customer cash: ${self.customer_account["cash_now"]}')

    
    def __sub__(self, other):
        goods_1 = [item['name'] for item in sum(self.shelves, []) if item is not None]
        goods_2 = [item['name'] for item in sum(other.shelves, []) if item is not None]
        goods_difference = {g:0 for g in set(goods_1 + goods_2)}

        goods_1 = [item for item in sum(self.shelves, []) if item is not None]
        goods_2 = [item for item in sum(other.shelves, []) if item is not None]

        for g in goods_1:
            goods_difference[g['name']] = g['qty']

        for g in goods_2:
            goods_difference[g['name']] = abs(goods_difference[g['name']] - g['qty'])
        
        return goods_difference
    
    def __add__(self, other):
        goods_1 = [item['name'] for item in sum(self.shelves, []) if item is not None]
        goods_2 = [item['name'] for item in sum(other.shelves, []) if item is not None]
        goods_union = {g:0 for g in set(goods_1 + goods_2)}

        goods_1 = [item for item in sum(self.shelves, []) if item is not None]
        goods_2 = [item for item in sum(other.shelves, []) if item is not None]

        for g in goods_1:
            goods_union[g['name']] = g['qty']

        for g in goods_2:
            goods_union[g['name']] = abs(goods_union[g['name']] + g['qty'])
        
        return goods_union
    
    def __truediv__(self, other):
        goods_1 = [item['name'] for item in sum(self.shelves, []) if item is not None]
        goods_2 = [item['name'] for item in sum(other.shelves, []) if item is not None]
        goods_intersection = {g:0 for g in set(goods_1).intersection(goods_2)}

        goods_1 = [item for item in sum(self.shelves, []) if item is not None]
        goods_2 = [item for item in sum(other.shelves, []) if item is not None]

        for g in goods_1:
            if g['name'] in list(goods_intersection.keys()):
                goods_intersection[g['name']] = g['qty']

        for g in goods_2:
            if g['name'] in list(goods_intersection.keys()):
                goods_intersection[g['name']] = min(g['qty'], goods_intersection[g['name']])
        return goods_intersection

    def __lt__(self, other):
        account_1 = [coin * qty for coin, qty in self.account['coins'].items()]
        account_2 = [coin * qty for coin, qty in other.account['coins'].items()]
        if sum(account_1) < sum(account_2):
            return True
        else:
            return False

    def __gt__(self, other):
        account_1 = [coin * qty for coin, qty in self.account['coins'].items()]
        account_2 = [coin * qty for coin, qty in other.account['coins'].items()]
        if sum(account_1) > sum(account_2):
            return True
        else:
            return False
        
if __name__ == '__main__':
    content_for_A = {

        'shelves': [[{'name': 'candy', 'price': 10, 'qty': 3},
                     {'name': 'bread', 'price': 8, 'qty': 5},
                     {'name': 'pepsi', 'price': 20, 'qty': 6},
                     {'name': 'milk', 'price': 7, 'qty': 4}],
                    [None, None, None, None],
                    [None, None, None, None]],
        'account': {'total_sum': 915.00, 'coins': {1: 10, 5: 15, 10: 23, 50: 12}},
        'customer_account': {'state': 'selecting',
                             'cash_now': 15,
                             'choice': {'x': None, 'y': None}}

    }

    content_for_B = {

        'shelves': [[{'name': 'fanta', 'price': 7, 'qty': 4},
                     {'name': 'candy', 'price': 8, 'qty': 5},
                     {'name': 'pepsi', 'price': 20, 'qty': 6},
                     {'name': 'cookes', 'price': 1, 'qty': 10}],
                    [None, None, None, None],
                    [None, None, None, None]],
        'account': {'total_sum': 815, 'coins': {1: 10, 5: 15, 10: 23, 50: 10}},
        'customer_account': {'state': 'selecting',
                             'cash_now': 15,
                             'choice': {'x': None, 'y': None}}

    }

    print('----\nHere is our Vending Machine\n\n')
    VM_A = VENDMACHINE(content_for_A)
    VM_B = VENDMACHINE(content_for_B)

    print('----\nShow contents:\n\n')
    print('For A:')
    VM_A.showcase()

    print('\n\nFor B:')
    VM_B.showcase()

    print('----\n\nCheck the content difference with "-":\n')
    print('VM_A - VM_B = ', VM_A - VM_B)

    print('VM_B - VM_A = ', VM_B - VM_A)

    print('----\n\nCheck the content union with "+":\n')
    print('VM_A + VM_B = ', VM_A + VM_B)

    print('----\n\nCheck the content intersection with "/":\n')
    print('VM_A / VM_B = ', VM_A / VM_B)

    print('VM_B / VM_A = ', VM_B / VM_A)

    print('----\n\nCompare the amount of money inside:\n')
    print('VM_A > VM_B = ', VM_A > VM_B)

    print('VM_B > VM_A = ', VM_B > VM_A)