import asyncio
import aiohttp


async def fetch_page(url):
  response = await aiohttp.request('GET', url)
  assert response.status == 200
  return await response.read()

content = asyncio.get_event_loop().run_until_complete(
    fetch_page('http://python.org'))
print(content)
