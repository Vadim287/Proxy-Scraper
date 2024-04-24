import requests
import time
from termcolor import colored
import urllib.request
import socket
import concurrent.futures

timeout = "3000"
url = "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt"
url2 = "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"

# Define additional URLs for socks4, socks5, and http proxies
socks4_urls = [
    'https://raw.githubusercontent.com/ObcbO/getproxy/master/file/socks4.txt',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt',
    'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks4/socks4.txt',
    'https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/socks4.txt',
    'https://raw.githubusercontent.com/TuanMinPay/live-proxy/master/socks4.txt',
    'https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks4.txt',
    # Add more socks4 URLs here
]

socks5_urls = [
    'https://raw.githubusercontent.com/ObcbO/getproxy/master/file/socks5.txt',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt',
    'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt',
    'https://raw.githubusercontent.com/TuanMinPay/live-proxy/master/socks5.txt',
    'https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/socks5.txt',
    'https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5.txt',
    # Add more socks5 URLs here
]

http_urls = [
    'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt',
    'https://raw.githubusercontent.com/ObcbO/getproxy/master/file/http.txt',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://github.com/ObcbO/getproxy/blob/master/file/https.txt',
    'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt',
    'https://raw.githubusercontent.com/TuanMinPay/live-proxy/master/http.txt',
    'https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/http.txt',
    'https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/http.txt',
    # Add more http URLs here
]

# Combine all proxy URLs
all_proxy_urls = socks4_urls + socks5_urls + http_urls

querystring = {
    "request": "displayproxies",
    "protocol": "http",
    "timeout": f"{timeout}",
}

headers = {
    "accept": "text/plain, */*; q=0.01",
    "accept-language": "en-US,en;q=0.8",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# Fetch data from all proxy URLs
proxies = []
for proxy_url in all_proxy_urls:
    response = requests.request("GET", proxy_url, headers=headers)
    proxies.extend(response.text.split("\n"))

print("Amount of proxies:", len(proxies))
time.sleep(3)

socket.setdefaulttimeout(3)

def is_bad_proxy(pip):
    try:
        proxy_handler = urllib.request.ProxyHandler({"http": pip})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [("User-agent", "Mozilla/5.0")]
        urllib.request.install_opener(opener)
        sock = urllib.request.urlopen("http://api.ipify.org/")
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as detail:
        return 1
    return 0

working = []
badcount = 0
workingcount = 0

def check_proxy(proxy):
    global badcount, workingcount
    if is_bad_proxy(proxy):
        badcount += 1
        print(colored(f"{badcount} bad proxies", "red"))
    else:
        workingcount += 1
        print(colored(f"{workingcount} working proxies", "green"))
        working.append(proxy + "\n")

start_time = time.time()

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(check_proxy, proxies)

end_time = time.time()
print("Time taken: ", end_time - start_time, "seconds")

with open("proxies.txt", "w") as f:
    f.writelines(working)
