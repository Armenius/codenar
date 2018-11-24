import requests

from test_plus import TestCase

from .views import ValidDomainIPView


class TestValidDomainIPView(TestCase):

    def setUp(self):
        request = requests.get('http://google.com', stream=True)
        self.google_ip_address = request.raw._connection.sock.getpeername()[0]
        print (self.google_ip_address)

    def test_post_valid(self):
        url = self.reverse('valid_domain_ip')
        payload = {'user_input': 'https://google.com'}
        result = self.post(url, data=payload, extra={'format': 'json'})
        self.assertEquals(result.json(), {
            payload['user_input']: self.google_ip_address
        })

    def test_validate_ip_address_valid(self):
        view = ValidDomainIPView()
        user_input = '112.18.16.12'
        result = view.validate_ip_address(user_input)
        self.assertIn('ip_address', result)
        self.assertEqual(result['ip_address'], user_input)

    def test_validate_ip_address_invalid(self):
        view = ValidDomainIPView()
        user_input = '999.99.99.99'
        result = view.validate_ip_address(user_input)
        self.assertIn('error', result)
        self.assertIn('Invalid', result['error'])

    def test_validate_ip_address_private(self):
        view = ValidDomainIPView()
        user_input = '192.168.1.1'
        result = view.validate_ip_address(user_input)
        self.assertIn('error', result)
        self.assertIn('Private', result['error'])

    def test_validate_domain_valid(self):
        view = ValidDomainIPView()
        user_input = 'http://google.com'
        result = view.validate_domain(user_input)
        self.assertIn(user_input, result)
        self.assertEqual(result[user_input], self.google_ip_address)

    def test_validate_domain_valid_missing_http(self):
        view = ValidDomainIPView()
        user_input = 'google.com'
        result = view.validate_domain(user_input)
        self.assertIn('http://' + user_input, result)
        self.assertEqual(
            result['http://' + user_input],
            self.google_ip_address
        )

    def test_validate_domain_invalid(self):
        view = ValidDomainIPView()
        user_input = 'test'
        result = view.validate_domain(user_input)
        self.assertIn('error', result)
        self.assertIn('Invalid', result['error'])

    def test_validate_domain_404(self):
        view = ValidDomainIPView()
        user_input = 'revsys.com/whatever'
        result = view.validate_domain(user_input)
        self.assertIn('error', result)
        self.assertIn('404', result['error'])

    def test_validate_input_ip(self):
        view = ValidDomainIPView()
        user_input = '112.18.16.12'
        result = view.validate_input(user_input)
        self.assertEqual(result, {'ip_address': user_input})

    def test_validate_input_domain(self):
        view = ValidDomainIPView()
        user_input = 'https://google.com'
        result = view.validate_input(user_input)
        self.assertEqual(result, {user_input: self.google_ip_address})
