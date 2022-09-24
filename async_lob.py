import asyncio
import json
import time
import pandas as pd
from websocket import create_connection
from tree import AVL
from book import Book


async def kraken(q):
    ws = create_connection('wss://ws.kraken.com/')
    ws.send(json.dumps({
        "event": "subscribe",
        "pair": ["DOT/USD"],
        "subscription": {"name":"book"}
    }))

    while True:
        result = ws.recv()
        result = json.loads(result)
        await q.put(result)

async def consumerProcess(q, q_update):
    while True:
        load = await q.get()
        if type(load) == list:
            if list(load[1].keys())[0] == 'as':
                book.init_book(load[1])
            elif list(load[1].keys())[0] in ['a', 'b']:
                book.insert(load[1])
                await q_update.put(book.request_book())
            else:
                pass

async def request_updates(q):
    while True:
        dict = {}
        bids, asks = await q.get()
        bid_s = []
        bid_l = []
        ask_l = []
        ask_s = []
        for i in bids:
            bid_l.append(i.price)
            bid_s.append(i.size)
        for i in asks:
            ask_l.append(i.price)
            ask_s.append(i.size)
        bid_l.reverse()
        bid_s.reverse()
        dict['size bid'] = bid_s[:5]
        dict['bids'] = bid_l[0:5]
        dict['asks'] = ask_l[0:5]
        dict['size ask'] = ask_s[0:5]
        df = pd.DataFrame(dict)
        print(df)
        time.sleep(1)

async def main():

    q1 = asyncio.Queue(maxsize=40)
    q2 = asyncio.LifoQueue(maxsize=40)

    await asyncio.gather(kraken(q1), consumerProcess(q1, q2), request_updates(q2))

if __name__ == "__main__":

    bids = AVL()
    asks = AVL()
    rta = None
    rtb = None
    book = Book(bids, asks, rta, rtb)

    asyncio.run(main())
