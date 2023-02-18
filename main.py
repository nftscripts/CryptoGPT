import asyncio
import pyuseragents
import random
import string
from faker import Faker
from aiohttp import ClientSession
from loguru import logger

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
        return ''.join(random.choice(string.ascii_letters) for _ in range(9)) + '@gmail.com'

    async def generate_fake_name_async(self) -> list:
        fake = Faker()
        fake_name = fake.name()
        return fake_name.split()

    async def register(self) -> None:
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
        self.headers.update({'user-agent': pyuseragents.random()})
        async with ClientSession(headers=self.headers) as session:
            response = await session.post('https://app.viral-loops.com/api/v2/events', json=json_data)
            if response.status == 200:
                logger.info(f'Successfully registered by code {code}')


async def main(nums_of_refs: int, reg: Process) -> None:
    tasks = []
    for _ in range(nums_of_refs):
        tasks.append(asyncio.create_task(reg.register()))
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    reg = Process()
    nums_of_refs = int(input('Enter number of referrals: '))
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(nums_of_refs, reg))
    except RuntimeError as e:
        if "Event loop is running" not in str(e):
            raise e
