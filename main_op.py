import platform

import aiohttp
import asyncio
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import logging
import json

async def get_info(days: datetime):
    async with aiohttp.ClientSession() as session:
        s = f"{days.day}.0{days.month}.{days.year}"
        try:
            async with session.get(f"https://api.privatbank.ua/p24api/exchange_rates?json&date={s}") as response:
                result = await response.json()
                print(f"date: {s}")
                print_info(result)
                return result
        except aiohttp.ClientConnectionError as er:
            logging.error("Connection error {er}")
            

def print_info(text):
    for k in text.keys():
        if k == "exchangeRate":
            print("EUR")
            print("sale:  ", text[k][8]['saleRateNB'])
            print("purchase:  ", text[k][8]['purchaseRateNB'])
            print("USD")
            print("sale:  ", text[k][23]['saleRateNB'])
            print("purchase:  ", text[k][23]['purchaseRateNB'])
            print("-----------------------------------------------")



async def main():
    try:
        while True:
            days = input(">>>")
            if int(days) <= 10:
                break
        data = [datetime.now().date() - timedelta(days=i)
                for i in range(int(days))]
        task = [asyncio.create_task(get_info(d)) for d in data]
        await asyncio.wait(task)
    except ValueError as err:
        print(f"This is not number! {err}")

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
