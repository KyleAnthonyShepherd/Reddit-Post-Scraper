# Reddit-Post-Scraper
This code can get the URLs of the ~600 million posts made to Reddit. As of Jan 2019, these urls can be obtained in about 24 hours.<br/>
<br/>
I wrote this code when I was trying to find historial posts in a subreddit,<br/>
and there was a limitation of 1000 posts backwards in time.<br/>
<br/>
Heavily inspired by this blog post by Andy Balaam:<br/>
Making 100 million requests with Python aiohttp<br/>
https://www.artificialworlds.net/blog/2017/06/12/making-100-million-requests-with-python-aiohttp/<br/>
<br/>
Technically, this code does not require a Reddit account, and does not use<br/>
OAUTH or any API tokens. It just extracts information contained in the response<br/>
headers of Reddit.<br/>
I most definitely exceeded the request rate limit when gathering the data,<br/>
but I was never blocked by Reddit.<br/>
<br/>
If this script is run by itself, the data is collected.<br/>
This script could be imported into another script, and the function<br/>
ControlLoop()<br/>
can be used on its own<br/>
<br/>
It takes ~35 GB to store the urls of all ~600 million posts.<br/>
<br/>
###<br/>
Code Written by:<br/>
Kyle Shepherd<br/>
KyleAnthonyShepherd.gmail.com<br/>
Jan 25, 2019<br/>
###<br/>
