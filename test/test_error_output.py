import asyncio

async def t1():
    while True:
        print(1+1)
        await asyncio.sleep(10)
        print(1 + 'ff')

if __name__ == '__main__':
    asyncio.run(t1())
