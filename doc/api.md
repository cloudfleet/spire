The examples need the following packages:

    pip install requests

## External authentification

An example of using the external authentication API is shown in
`doc/examples/external_authentication.py` and can be tried out
if spire is running:

    python external_authentication.py http://localhost:8000

or against the live app:

    python external_authentication.py https://spire.cloudfleet.io

To try Blimp authorization as well, pass the blimp url
(the part after the subdomain is BLIMPYARD_URL) e.g.:

    python external_authentication.py http://localhost:8000 jules.localhost

## Certificate requesting

Run the example as:

    python request_cert.py http://localhost:8000 test.localhost secret

where `test.localhost` is the domain and `secret` is the... secret.

To test the API against the live app:

    python request_cert.py https://spire.cloudfleet.io \
    kermit.blimpyard.cloudfleet.io:80 password

## Certificate requesting (just json)

Run the example as:

    python request_cert.py http://localhost:8000 test.localhost \
    "djkslafjdsalfjdsalk" secret

where `test.localhost` is the domain, `"djkslafjdsalfjdsalk"` is the
cert. request and `secret` is the... secret.

To test the API against the live app:

    python request_cert.py https://spire.cloudfleet.io \
        kermit.blimpyard.cloudfleet.io:80 "djkslafjdsalfjdsalk" password

## Getting the finished certificates

Run the example as:

    python get_cert.py http://localhost:8000 test.localhost secret
