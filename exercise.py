import requests

url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson'
params ={'serviceKey' : 'boZekjwilAq30T3C6fn8GboYI3OCDnZeP11s2XfYg0QkqbP9+G/nlc6xctjtSMiCryY/4hu290ouse5o2G7cJg==', 'pageNo' : '1', 'numOfRows' : '10', 'startCreateDt' : '20200310', 'endCreateDt' : '20200315' }

response = requests.get(url, params=params)
print(response.content)