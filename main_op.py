import platform
import sys

import aiohttp
import asyncio
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import logging
import json

CURRENCY = {
    "EUR": 8, 
    "USD": 23, 
    "CHF": 4, 
    "GBP": 9,  
    "XAU": 25, 
    "CAD": 3, 
    'AUD': 0, 
    'AZN': 1, 
    'BYN': 2, 
    'CNY': 5, 
    'CZK': 6, 
    'DKK': 7,
    'GEL': 10, 
    'HUF': 11, 
    'ILS': 12, 
    'JPY': 13, 
    'KZT': 14, 
    'MDL': 15, 
    'NOK': 16, 
    'PLN': 17, 
    'SEK': 18, 
    'SGD': 19, 
    'TMT': 20, 
    'TRY': 21, 
    'UAH': 22, 
    'UZS': 24, 

}

async def get_info(days: datetime, cur='UAH'):
    async with aiohttp.ClientSession() as session:
        s = f"{days.day}.0{days.month}.{days.year}"
        try:
            async with session.get(f"https://api.privatbank.ua/p24api/exchange_rates?json&date={s}") as response:
                result = await response.json()
                print(f"date: {s}")
                print_info(result, cur)
                return result
        except aiohttp.ClientConnectionError as er:
            logging.error("Connection error {er}")
            

def print_info(text, cur='UAH'):
    for k in text.keys():
        if k == "exchangeRate":
            try:
                print(cur)
                print("sale:  ", text[k][CURRENCY[cur]]['saleRateNB'])
                print("purchase:  ", text[k][CURRENCY[cur]]['purchaseRateNB'])
            except KeyError as n:
                print("This currency not found!")
            print("-----------------------------------------------")
            print("EUR")
            print("sale:  ", text[k][8]['saleRateNB'])
            print("purchase:  ", text[k][8]['purchaseRateNB'])
            print("-----------------------------------------------")
            print("USD")
            print("sale:  ", text[k][23]['saleRateNB'])
            print("purchase:  ", text[k][23]['purchaseRateNB'])
            print("-----------------------------------------------")



async def main():
    try:
        if (int(sys.argv[1]) <= 10)and(len(sys.argv)>2):
            data = [datetime.now().date() - timedelta(days=i) for i in range(int(sys.argv[1]))]
            task = [asyncio.create_task(get_info(d, sys.argv[2])) for d in data]
            await asyncio.wait(task)
        elif (int(sys.argv[1]) <= 10)and(len(sys.argv)>1):
            data = [datetime.now().date() - timedelta(days=i) for i in range(int(sys.argv[1]))]
            task = [asyncio.create_task(get_info(d)) for d in data]
            await asyncio.wait(task)
        else:
            await get_info(datetime.now().date())
    except ValueError as err:
        print(f"This is not number! {err}")

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
