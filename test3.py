import aiohttp
import asyncio

async def get_body(url):
  response = await aiohttp.request('GET', url)
  raw_html = await response.read()
  return raw_html

async def main():
  # run them sequentially (but the loop can do other stuff in the meanwhile)
  body1 = await get_body('http://httpbin.org/ip')
  body2 = await get_body('http://httpbin.org/user-agent')

  # run them in parallel
  task1 = get_body('http://httpbin.org/ip')
  task2 = get_body('http://httpbin.org/user-agent')

  for body in await asyncio.gather(task1, task2):
    print(body)

  # OR
  #done, pending = await asyncio.wait([task1, task2], return_when=asyncio.ALL_COMPLETED, timeout=None)
  #for task in done:
  #    print(task.result())

if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())
