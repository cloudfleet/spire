import requests, sys
url = sys.argv[1]
print('trying jules')
r = requests.post(url,
                  {'username':'jules', 'password':'jules123'})
print(r.text)
print('trying jules, wrong password')
r = requests.post(url,
                  {'username':'jules', 'password':'jules1235'})
print(r.text)
print('trying mickey')
r = requests.post(url,
                  {'username':'mickey', 'password':'mickey123'})
print(r.text)
