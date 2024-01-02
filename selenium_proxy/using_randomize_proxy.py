from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
req_proxy = RequestProxy() #you may get different number of proxy when  you run this at each time
proxies = req_proxy.get_proxy_list() #this will create proxy list


ind = [] #int is list of Indian proxy
for proxy in proxies:
    print(proxy.country)
    if proxy.country == 'India':
        ind.append(proxy)