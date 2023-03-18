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


async def get_info_old(days: datetime):
    async with aiohttp.ClientSession() as session:
        s = f"{days.day}.0{days.month}.{days.year}"
        async with session.get(f"https://api.privatbank.ua/p24api/exchange_rates?json&date={s}") as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])
            print('Cookies: ', response.cookies)
            print(response.ok)
            result = await response.json()
            print(result)
            return result


async def get_info_now():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5") as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])
            print('Cookies: ', response.cookies)
            print(response.ok)
            result = await response.json()
            print(result)
            return result


async def get_currency():
    try:
        while True:
            days = input(">>>")
            if int(days) <= 10:
                break
        data = [datetime.now().date() - timedelta(days=i)
                for i in range(int(days))]
        task = [asyncio.create_task(get_info_old(d)) for d in data]
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
            await self.send_to_clients(f"{ws.name}: {message}")

    async def command_exchange(self, )
       if not f"\n" in message:
            await get_info_now()
        else:
            await get_info_old(days)


async def exchange(message):


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
