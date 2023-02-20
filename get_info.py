import asyncio
from concurrent.futures import ProcessPoolExecutor
import aiohttp
import lxml.html
import nest_asyncio
nest_asyncio.apply()


URL_STACK = ['https://www.kufar.by/listings?size=42&sort=lst.d&cur=BYR&cat=17010&query=iphone%207&ot=1&rgn=1&ar=1&prc=r%3A25000%2C35000',
      'https://www.kufar.by/listings?size=42&sort=lst.d&cur=BYR&cat=17010&query=iphone%207%20plus&ot=1&rgn=1&ar=1&prc=r%3A40000%2C55000',
      'https://www.kufar.by/listings?size=42&sort=lst.d&cur=BYR&cat=17010&query=iphone%208&ot=1&rgn=1&ar=1&prc=r%3A40000%2C60000',
      'https://www.kufar.by/listings?size=42&sort=lst.d&cur=BYR&cat=17010&query=iphone%208%20plus&ot=1&rgn=1&ar=1&prc=r%3A50000%2C70000',
      'https://www.kufar.by/listings?size=42&sort=lst.d&cur=BYR&cat=17010&query=iphone%20x&ot=1&rgn=1&ar=1&prc=r%3A60000%2C80000']
      # urls to parse iphones info

def get_hrefs(html,href):
  hrefs = []
  tree = lxml.html.fromstring(html)
  items = tree.xpath('//a[contains(@class,"styles_wrapper__IMYdY")]')
  for item in items:
    hrefs.append(item.get('href'))
  return hrefs

async def fetch_page(url, session):
  '''Meant for IO-bound workload'''
  async with session.get(url, timeout = 15) as res:
    return await res.text()


async def process(url, session, pool,func):
  html = await fetch_page(url, session)
  return await asyncio.wrap_future(pool.submit(func,html,url))


async def dispatch(urls,func):
  pool = ProcessPoolExecutor()
  async with aiohttp.ClientSession() as session:
    coros = (process(url, session, pool,func) for url in urls)
    return await asyncio.gather(*coros)

def parse():
  hrefs =  asyncio.get_event_loop().run_until_complete(dispatch(URL_STACK,get_hrefs))
  hrefs = sum(hrefs, [])
  return  hrefs
