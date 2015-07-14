"""An example demonstrating the client-side usage
of the cretificate request API endpoint.

"""

import requests, sys

url = sys.argv[1] + '/dashboard/blimp/api/get_cert'
domain = sys.argv[2]
secret = sys.argv[3]
print('getting: ' + url)
r = requests.post(
    url, {'domain': domain, 'secret': secret}
)
print(r.text)
print(r)
