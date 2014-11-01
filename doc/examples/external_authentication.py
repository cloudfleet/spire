import requests, sys
url = sys.argv[1] + '/auth/'
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

if len(sys.argv) > 2:
    print('Blimp authorization')
    blimp = sys.argv[2]
    url = sys.argv[1] + '/auth_blimp/'
    print('trying {}'.format(blimp))
    r = requests.post(url,
                      {'username':'jules', 'password':'jules123',
                       'blimp': blimp})
    print(r.text)
    print('trying {}.false'.format(blimp))
    r = requests.post(url,
                      {'username':'jules', 'password':'jules123',
                       'blimp': blimp + '.false'})
    print(r.text)
