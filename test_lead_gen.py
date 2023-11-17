import random
import requests
from lxml.html import fromstring


def initialize_proxies():
    proxies = []
    try:
        for page in range(1, 3):
            response = requests.get("https://proxy.webshare.io/api/proxy/list/?page=" + str(
                page), headers={"Authorization": "Token 697bfb06a037cccc135419ceb1d08669b1f15384"})
            pr = response.json()
            print("Total Proxies: " + str(len(pr['results'])))
            proxies += pr['results']
        return proxies
    except Exception as e:
        print(e)
        return proxies

        # self.tracking_obj.tracebackError(self.initialize_proxies.__name__, self.fetch_date())
        # return "ProxyError: " + str(e)


def get_proxy(proxies):
    if proxies:
        pr = random.randint(0, 9)
        proxy = proxies[pr]['proxy_address'].strip()
        port = proxies[pr]['ports']['http']
        user = proxies[pr]['username'].strip()
        password = proxies[pr]['password'].strip()
        proxy_in = {
            'http': 'http://{}:{}@{}:{}/'.format(user, password, proxy, port),
            'https': 'http://{}:{}@{}:{}/'.format(user, password, proxy, port)
        }
        return proxy_in


initial_proxies = initialize_proxies()
proxies = get_proxy(initial_proxies)

headers = {
    'Cookie': '__cf_bm=65Xt5gz8rrb8NrA1sgRVB62xLHCgS7HL8EZm6.._U7I-1686207490-0-Ad5fpCyXNmFQwDVwl+csVtUfetexOlazhPUR8CawGN6nM+z38/vT/SSjEZxstiVE5DLEuIdl2ukKPhpAr8NnvgryoFgpogmid8HD6TFTgLdQ; _cfuvid=Sca6vkMgxdYPFm52zl0FgvVAUtMrb1ujkEHsHOUacpw-1686133175513-0-604800000; asst=1686207490.0; bs=jMZ5lHXP9H_WyjLFFHebGQ:QrDbGvUDEfEU_PNzXYhjQCWfl5HLitp9SnsrNU_7VGt26CO5m8cuY32_x3Npi8qUWa8ZzCh_P4DdZ6gYVPIcXJxRXbibRfO8cufg_Acfm6g:esTw1T3L8Z61Tz1kEElKhxXE2AZsD0Sg82QUxBv0TL8; gdId=41deb13f-25a8-45f8-8a3a-1406bf1244e4; gdsid=1686207490176:1686207490176:FAE0F76920A4D536365F4CA42347B44F'
}
res = requests.get('https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=software+developer&sc.keyword=software+developer&locT=N&locId=3&jobType=', headers=headers, proxies=proxies)

main_html = fromstring(res.content)
print(res.content)
print("MAIN CONTENT", main_html)
