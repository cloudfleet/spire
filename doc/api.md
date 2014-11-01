The examples need the following packages:

    pip install requests

An example of using the external authentication API is shown in
`doc/examples/external_authentication.py` and can be tried out
if spire is running:

    python external_authentication.py localhost:8000

or against the live app:

    python external_authentication.py https://cloudfleet.herokuapp.com

To try Blimp authorization as well, pass the blimp url
(the part after the subdomain is BLIMPYARD_URL) e.g.:

    python external_authentication.py localhost:8000 jules.localhost
