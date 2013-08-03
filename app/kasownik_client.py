
import requests
import hmac
import json
from secrets import API_KEY


class APIClientException(Exception):
    pass


class APIClient(object):
    def __init__(self, key=API_KEY, address="https://kasownik.hackerspace.pl"):
        self.key = key
        self.address = address.rstrip("/")

    def __getattr__(self, name):
        def f(**data):
            serialized = json.dumps(data)
            mac = hmac.new(self.key)
            mac.update(serialized)
            mac64 = mac.digest().encode("base64")
            
            data = serialized.encode("base64") + "," + mac64
            r = requests.post("%s/api/%s" % (self.address, name), data)
            if r.status_code == 400:
                raise APIClientException("malformed request.")
            if r.status_code == 403:
                raise APIClientException("wrong api key")
            if r.status_code == 404:
                raise APIClientException("no such method.")
            if r.status_code != 200:
                raise APIClientException("unexpected status code %i" % r.status_code)
	    	
            try:
                return json.loads(r.text)
            except ValueError:
                raise APIClientException("malformed response.")
        return f


if __name__ == '__main__':
    # private method: get member list
    client = APIClient()
    print client.members()

    # private method: get member info
    # this will probably 500 for an unknown member
    # please please please cache this somehow, as it does weird shit to the database
    # use memcached or i dunno
    print client.member_info(member="q3k")
    # public method: hs mana
    print client.mana()
