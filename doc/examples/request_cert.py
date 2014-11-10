"""An example demonstrating the client-side usage
of the cretificate request API endpoint.

"""

import requests, sys

import requests, sys

url = sys.argv[1] + '/dashboard/blimp/api/request_cert'
domain = sys.argv[2]
secret = sys.argv[3]
print('requesting: ' + url)
files = {'signature': open('signature.txt', 'rb')}
r = requests.post(url, {'domain': domain, 'secret': secret}, files=files)
#r = requests.post(url)
print(r.text)
