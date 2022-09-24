class Level:
    def __init__(self, price, size, time):
        self.price = price
        self.size = size
        self.time = time


class Book:
    def __init__(self, bids, asks, rta, rtb):
        self.bids = bids
        self.asks = asks
        self.rta = rta
        self.rtb = rtb

    def insert(self, load):
        if list(load.keys())[0] == 'a':
            for i in load['a']:
                order = Level(float(i[0]),float(i[1]),i[2])
                if order.size > 0:
                    self.rta = self.asks.insert(order, self.rta)
                else:
                    self.rta = self.asks.delete(order, self.rta)
        elif list(load.keys())[0] == 'b':
            for i in load['b']:
                order = Level(float(i[0]),float(i[1]),i[2])
                if order.size > 0:
                    self.rtb = self.bids.insert(order, self.rtb)
                else:
                    self.rtb = self.bids.delete(order, self.rtb)

    def init_book(self, load):
        for i in load['as']:
            order = Level(float(i[0]),float(i[1]),i[2])
            self.rta = self.asks.insert(order, self.rta)
        for i in load['bs']:
            order = Level(float(i[0]),float(i[1]),i[2])
            self.rtb = self.bids.insert(order, self.rtb)

    def request_book(self):
        bids = self.bids.inorderTraversal(self.rtb)
        asks = self.asks.inorderTraversal(self.rta)
        return bids, asks