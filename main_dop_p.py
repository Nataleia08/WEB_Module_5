import asyncio
import logging
import websockets
import aiohttp
import names
import platform
from datetime import datetime, timedelta
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK

logging.basicConfig(level=logging.INFO)


async def get_info(days: datetime):
    async with aiohttp.ClientSession() as session:
        s = f"{days.day}.0{days.month}.{days.year}"
        try:
            async with session.get(f"https://api.privatbank.ua/p24api/exchange_rates?json&date={s}") as response:
                result = await response.json()
                res_list = []
                res_list.append(f"date: {s}")
                print_info(result, res_list)
                return res_list
        except aiohttp.ClientConnectionError as er:
            logging.error("Connection error {er}")
            

def print_info(text, res_list: list):
    for k in text.keys():
        if k == "exchangeRate":
            res_list.append("EUR")
            res_list.append("sale:  ")
            res_list.append(text[k][8]['saleRateNB'])
            res_list.append("purchase:  ", text[k][8]['purchaseRateNB'])
            res_list.append("USD")
            res_list.append("sale:  ", text[k][23]['saleRateNB'])
            res_list.append("purchase:  ", text[k][23]['purchaseRateNB'])
            res_list.append("-----------------------------------------------")
    return res_list



async def command_exchange_arhive(days: int):
    try:
        data = [datetime.now().date() - timedelta(days=i)
                for i in range(int(days))]
        task = [asyncio.create_task(get_info(d)) for d in data]
        await asyncio.wait(task)
    except ValueError as err:
        print(f"This is not number! {err}")


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            if exchange in message:
                await exchange(message)
            if message.find("exchange") != -1:
                if message.find( r"") != -1:
                    await command_exchange_arhive()
                r = await get_info(datetime.now().date())

            await self.send_to_clients(f"{ws.name}: {message}, {r}")



async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

    # r = asyncio.run(get_currency())
    # print(r)
