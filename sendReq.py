import requests

proxy = {"http": "127.0.0.1:3000"}
url = "http://api.emnr.no/course/TTM4100" #Låner bare endpointet til emnr.no (Beklager litt trafikk)
response = requests.get(url=url, proxies=proxy)
print("resp: ", response.text)