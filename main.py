import pyuseragents
import random
import string
from faker import Faker
from aiohttp import ClientSession
from loguru import logger
from asyncio import (
    gather,
    get_event_loop,
    create_task,
    sleep,
    set_event_loop,
    ProactorEventLoop
)

code = ''
public_token = ''


class Process:
    def __init__(self) -> None:
        self.headers = {
            'authority': 'app.viral-loops.com',
            'accept': '*/*',
            'accept-language': 'ru,en;q=0.9,ru-RU;q=0.8,en-US;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://www.cryptogpt.org',
            'referer': 'https://www.cryptogpt.org/',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': '',
            'x-ucid': '7ZPrKYPrpDItGsySTU6iwJ0dZMI',
        }

    async def generate_fake_mail_async(self) -> str:
        letters = string.ascii_lowercase
        digits = string.digits
        special_chars = "!#$%&'*+-/=?^_`{|}~"
        domain_names = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
        name_length = random.randint(5, 10)
        domain_name = random.choice(domain_names)
        name = ''.join(random.choice(letters + digits + special_chars) for _ in range(name_length))
        email = f"{name}@{domain_name}"
        return email

    async def generate_fake_name_async(self) -> list:
        fake = Faker()
        fake_name = fake.name()
        return fake_name.split()

    async def register(self, json_data) -> None:
        self.headers.update({'user-agent': pyuseragents.random()})
        async with ClientSession(headers=self.headers) as session:
            response = await session.post('https://app.viral-loops.com/api/v2/events', json=json_data)
            response_text = await response.text()
            if '"isNew":true' in response_text:
                logger.info(f'Successfully registered by code {code}')
            elif '<!DOCTYPE html>' in response_text:
                await sleep(30)
            else:
                logger.info(f'Successfully registered by code {code}')
            await sleep(0.5)

    async def get_tasks(self, nums_of_refs) -> list:
        tasks = []
        for _ in range(nums_of_refs):
            json_data = {
                'params': {
                    'event': 'registration',
                    'captchaJWT': None,
                    'user': {
                        'firstname': (await self.generate_fake_name_async())[0],
                        'lastname': (await self.generate_fake_name_async())[1],
                        'email': await self.generate_fake_mail_async(),
                        'initialAcquiredFrom': f'https://www.cryptogpt.org/refer?referralCode={code}&refSource=copy',
                    },
                    'referrer': {
                        'referralCode': code,
                    },
                    'refSource': 'copy',
                    'acquiredFrom': 'form_widget',
                },
                'publicToken': public_token,
            }
            tasks.append(create_task(self.register(json_data)))
            await sleep(0.5)
        return tasks

    async def get_symbols(self, nums_of_refs) -> None:
        tasks = await self.get_tasks(nums_of_refs)
        results = await gather(*tasks)


def start_event_loop(nums_of_refs, reg):
    loop = ProactorEventLoop()
    set_event_loop(loop)
    return get_event_loop().run_until_complete(reg.get_symbols(nums_of_refs))


reg = Process()
nums_of_refs = int(input('Enter number of referrals: '))
start_event_loop(nums_of_refs, reg)
