import platform

import aiohttp
import asyncio
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

async def get_info(days: datetime):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.privatbank.ua/p24api/exchange_rates?date={days}") as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])
            print('Cookies: ', response.cookies)
            print(response.ok)
            result = await response.json()
            print(result)
            return result

async def main():
    try:
        days = input()
        data = [datetime.now().date() - timedelta(days = i) for i in range(int(days))]
        task = [asyncio.create_task(get_info(d)) for d in data]
        await asyncio.wait(task)
    except ValueError as err:
        print(f"This is not number! {err}")

if __name__ == "__main__":
    r = asyncio.run(main())
    print(r)