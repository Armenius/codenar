import ipaddress
import requests

from urllib.parse import urlparse
import dns.resolver
import socket

'''
            Returns JSON
            Step 1: view gets the post with request
            Step 2: checks if the requst body has user_input
            Step 3: calls validate_input
            Step 4: identifies ip address
            if ip_address than it calls validate_ip_address
            Decides if input is IP address is private or illegal
            Step 5: if not ip calls validate_domain
            checks validate domain
            checks if it starts with http or not
            calls requests to check the status_code
            sends domain, ip address and reverse DNS
            [TODO] unable to perform reverse lookup for gmail.com
'''


class DomainValidation:
    def __init__(self):
        self.common_headers = [
            'accept-patch', 'accept-ranges', 'age',
            'allow', 'alt-svc', 'cache-control',
            'connection', 'content-disposition', 'content-encoding',
            'content-language', 'content-length', 'content-location',
            'content-range', 'content-type', 'date',
            'delta-base', 'etag', 'expires',
            'im', 'last-modified', 'link',
            'location', 'pragma', 'proxy-authenticate',
            'public-key-pins', 'retry-after', 'set-cookie',
            'strict-transport-security', 'trailer', 'transfer-encoding',
            'tk', 'upgrade', 'vary',
            'via', 'warning', 'www-authenticate',
            'content-security-policy', 'refresh', 'x-powered-by',
            'x-request-id', 'x-ua-compatible', 'x-xss-protection',
            'x-frame-options', 'x-content-type-options',
            'referrer-policy', 'access-control-allow-origin', 'strict-transport-security',
            'x-download-options', 'Content-Security-Policy-Report-Only'
        ]

    def validate_input(self, input):
        try:
            parts = input.split('.')
            if (
                    len(parts) == 4 and all(
                0 <= int(part) < 256 for part in parts
            )
            ):
                json_contains_ip_address = self.validate_ip_address(input)

                if 'error' in json_contains_ip_address.keys():
                    return json_contains_ip_address

                elif 'ip_address' in json_contains_ip_address.keys():
                    return json_contains_ip_address

            else:
                return self.validate_domain(input)

        except (ValueError, AttributeError, TypeError):
            return self.validate_domain(input)

    def validate_ip_address(self, ip_address):
        try:
            ip_object = ipaddress.ip_address(ip_address)

        except ValueError:
            return {'error': 'Invalid IP address'}

        if ip_object.is_private:
            return {'error': 'Private IP address'}

        return {'domain': self.get_reverse_dns(ip_address),
                'ip_address': ip_address,
                'reverse_dns': self.get_reverse_dns(ip_address)}

        '''
		Clean domain function is called vertify if,
		scheme http or https
		if entry is codenar.com than it adds
		https://www.codenar.com
		'''

    def clean_domain(self, unsanatized_url):
        parser = urlparse(unsanatized_url)

        if parser.scheme:
            clean_url = unsanatized_url

        else:
            url = parser.path

            if len(url.split('.')) == 2:
                clean_url = 'https://www.' + url

            else:
                clean_url = 'https://' + url

        return clean_url

    def validate_domain(self, domain):
        clean_domain = self.clean_domain(domain)

        try:
            response = requests.get(clean_domain, stream=True)

        except requests.exceptions.ConnectionError:
            return {'error': 'Invalid domain'}

        if response.status_code == 200:
            ip_address = response.raw._connection.sock.getpeername()[0]

            return {"domain": clean_domain,
                    "ip_address": ip_address,
                    "reverse_dns": self.get_reverse_dns(ip_address)
                    }

        return {'error': str(response.status_code)}

    def get_reverse_dns(self, ip_address):
        # https://stackoverflow.com/questions/7832264/difficulty-using-pythons-socket-gethostbyaddr

        try:
            reverse_dns = socket.gethostbyaddr(ip_address)[0]
        except:
            ip_address = ip_address + '.in-addr.arpa.'
            try:
                reverse_dns = socket.gethostbyaddr(ip_address)[0]
            except:
                reverse_dns = ip_address
        return reverse_dns


'''
Todo 
1. Generate POST request body get_info_post()
2. Set cookies get_cookies 
'''


class Proxy:
    def __init__(self, url):
        self.url = url

    def clean(self, text):
        text = text.strip()
        text = text.replace("\n", " ")
        text = re.sub(" +", " ", text)
        return text

    def get_cookie(self, prepped):
        prepped.headers[
            'User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 Firefox/58.0'
        prepped.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.'
        prepped.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        prepped.headers['Connection'] = 'keep-alive'
        prepped.headers['Accept-Encoding'] = 'gzip, deflate, br'
        prepped.headers['Accept-Language'] = 'en-US,en;q=0.9'
        return prepped

    def get_info(self):
        session = requests.Session()
        request = Request('GET', self.url)
        prepped = session.prepare_request(request)
        page = session.send(self.get_cookie(prepped))
        return page

    def get_info_post():
        pass

    def send_data(self, http_verb='GET', proxy=False):
        http_proxy = "127.0.0.1:8080"
        https_proxy = "127.0.0.1:8080"
        ftp_proxy = "127.0.0.1:8080"
        proxyDict = {
            "http": http_proxy,
            "https": https_proxy,
            "ftp": ftp_proxy
        }
        session = requests.Session()
        request = Request('GET', self.url)
        prepped = session.prepare_request(request)
        if proxy:
            page = session.send(self.get_cookie(prepped), proxies=proxyDict, verify=False, timeout=2)
        else:
            page = session.send(self.get_cookie(prepped), timeout=2)
        return page
