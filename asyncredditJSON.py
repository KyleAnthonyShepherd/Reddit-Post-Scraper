'''
This code extracts the URLS of every post made to Reddit.

I wrote this code when I was trying to find historial posts in a subreddit,
and there was a limitation of 1000 posts backwards in time.

Heavily inspired by this blog post by Andy Balaam:
Making 100 million requests with Python aiohttp
https://www.artificialworlds.net/blog/2017/06/12/making-100-million-requests-with-python-aiohttp/

Technically, this code does not require a Reddit account, and does not use
OAUTH or any API tokens. It just extracts information contained in the response
headers of Reddit.
I most definitely exceeded the request rate limit when gathering the data,
but I was never blocked by Reddit.

If this script is run by itself, the data is collected.
This script could be imported into another script, and the function
ControlLoop()
can be used on its own

It takes ~35 GB to store the urls of all ~600 million posts.

###
Code Written by:
Kyle Shepherd
KyleAnthonyShepherd.gmail.com
Jan 25, 2019
###
'''


#### Import Block ####
# the import block imports needed modules, and spits out a json file with
# version numbers so the code can be repeatable
file = open("ModuleVersions.json", 'w')
modules = {}

import sys
modules['Python'] = dict([('version', sys.version_info)])

import time
import math
from itertools import islice
import asyncio
import os

import json
modules['json'] = dict([('version', json.__version__)])

import aiohttp
modules['aiohttp'] = dict([('version', aiohttp.__version__)])
from aiohttp import ClientSession, TCPConnector

import numpy
modules['numpy'] = dict([('version', numpy.__version__)])

json.dump(modules, file, indent=4, sort_keys=True)
file.close()
#### END Import Block ####

# Mostly copied from Andy Balaam's blog post
# Its purpose is to limit the number of simultaneous requests, so the ports
# on the computer are not exceeded.
def limited_as_completed(coros, limit):
    # limits the number of requests to limit
    # also initiates the coros, fetch, function
    futures = [
        asyncio.ensure_future(c)
        for c in islice(coros, 0, limit)
    ]
    async def first_to_finish():
        # while loop, busy loop
        # does cause lots of CPU use, but only one core
        while True:
            # brief sleep to make sure things work
            await asyncio.sleep(0)
            # looks at the currently running tasks
            for f in futures:
                # if a request is finished, kick it from the list
                # and append the next coros task
                # and start that task
                if f.done():
                    futures.remove(f)
                    try:
                        newf = next(coros)
                        futures.append(
                            asyncio.ensure_future(newf))
                    except StopIteration as e:
                        pass
                    return f.result()
    # waits for futures to run out
    while len(futures) > 0:
        yield first_to_finish()

# async function that makes the URL request
# it also parses the response and saves it to a file
async def fetch(url, session, file, log, ID):
    try:
        async with session.get(url) as response:
            out=await response.json()
            try:
                # print(response.headers['location'])
                for k in range(0,int(out['data']['dist'])):
                    file.write(out['data']['children'][k]['data']['id']+','+out['data']['children'][k]['data']['permalink']+'\n')
            except:
                pass
    except:
        for k in range(0,100):
            log.write(str(ID[k])+','+'FAILED\n')

# async function that handles all of the tasks given to it
# it exits when all the tasks are completed
async def print_when_done(tasks,limit):
    for res in limited_as_completed(tasks,limit):
        await res

def ControlLoop(NewPostId):

    if not os.path.exists('JSON'):
        os.makedirs('JSON') # creates data folder if it does not exist

    end=int('NewPostId',36) # newest post
    limit = 64 # open port limitation
    FileSize=1000000 # number of urls to store per file.
    loops=math.ceil(end/FileSize) # determines number of files to create

    # this URL could be used to get post urls one at a time, avoiding the
    # API entirely
    url = "https://www.reddit.com/{}"

    # This URL is the one used to get all of the post urls, 100 at a time.
    # uses the API technically
    url = "https://www.reddit.com/api/info.json?id={}"

    # url formatting for the requests
    IDS=''
    values=[]
    for k in range(0,100):
        IDS=IDS+'t3_{},'
        values.append(k)
    values=range(0,100)
    url=url.format(IDS)[:-1]

    # asyncio loop
    loop = asyncio.get_event_loop()

    #opens the request session
    connector = TCPConnector(limit=limit)
    session=ClientSession(connector=connector)

    #opens log file for storing failed requests
    log=open('JSON/log','w',encoding='utf-8')

    # loop for collecting the URLS
    # each loop is 1,000,000 URLs collected
    for k in range(0,loops):
        IDs=[]
        # t=time.time()
        #opens file
        file=open('JSON/urls k='+str(k),'w',encoding='utf-8')

        #constructs the urls that will be requested
        #creates 1,000,000 / 100 urls = 10,000 urls
        for i in range(k*FileSize,k*FileSize+FileSize,100):
            IDnum=numpy.arange(i,i+100)
            ID=[numpy.base_repr(IDnum[j], base=36).lower() for j in range(0,100)]
            IDs.append(ID)
            # IDnum=IDnum-1
        # print(time.time()-t)

        #creates list of tasks to perform
        coros = (fetch(url.format(*IDs[i]), session, file, log, IDs[i]) for i in range(int(FileSize/100)))

        # initiates URL requests
        loop.run_until_complete(print_when_done(coros,limit))
        file.close()
        # print(time.time()-t)
    loop.close()


if __name__ == "__main__":
    #this code runs if this script is called by itself
    NewPostId='al30vg'
    ControlLoop(NewPostId)
