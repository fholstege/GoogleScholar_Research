BOT_NAME = 'GoogleScholar'

SPIDER_MODULES = ['GoogleScholar_spider']

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# List of different user agents
USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'
]


DOWNLOADER_MIDDLEWARES = {
	'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
     'funda.middlewares.RandomUserAgentMiddleware': 400,
     'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy_proxies.RandomProxy': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    # Disable compression middleware, so the actual HTML pages are cached
}

PROXY_MODE = 2
http_proxy = "http://lum-customer-hl_f9982940-zone-googlescholar:ofdqieuiwps4@zproxy.lum-superproxy.io:22225"
CUSTOM_PROXY = "http://lum-customer-hl_f9982940-zone-googlescholar:ofdqieuiwps4@zproxy.lum-superproxy.io:22225"
