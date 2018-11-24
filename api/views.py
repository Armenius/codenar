from api.utils import DomainValidation

from rest_framework.response import Response
from rest_framework.views import APIView

import dns.resolver
import masscan


class ValidDomainIPView(APIView):
    '''
        [TODO] Replace rest_framework as this is a commerical tool
    '''
    queryset = None

    def post(self, request, format=None):
        domain_validator = DomainValidation()

        try:
            # Step 1: view gets the post with request
            # Step 2: checks if the requst body has user_input

            input_entered = request.data['user_input']

            # Step 3: calls validate_input
            result = domain_validator.validate_input(
                input_entered
            )

        except KeyError:
            print(KeyError)
            return Response(
                {
                    'error': 'Please pass input in user_input.'
                }
            )

        '''

            APIView
            https://www.django-rest-framework.org/api-guide/caching/#using-cache-with-apiview-and-viewsets
            
            rest_framework uses Response and APIView calls
            we import this from settings.py INSTALLED_APPS
            
            Look at https://www.django-rest-framework.org/ for details
            https://www.django-rest-framework.org/api-guide/responses/#response
        '''

        return Response(result)


class SubdomainView(APIView):
    '''
        [TODO] Replace rest_framework as this is a commerical tool
    '''
    queryset = None

    def post(self, request, format=None):
        domain_validator = DomainValidation()

        try:
            # Step 1: view gets the post with request
            # Step 2: checks if the requst body has user_input

            input_entered = request.data['user_input']

            # Step 3: calls validate_input
            result = domain_validator.validate_input(
                input_entered
            )

        except KeyError:
            print(KeyError)
            return Response(
                {
                    'error': 'Please pass input in user_input.'
                }
            )

        '''

            APIView
            https://www.django-rest-framework.org/api-guide/caching/#using-cache-with-apiview-and-viewsets
            
            rest_framework uses Response and APIView calls
            we import this from settings.py INSTALLED_APPS
            
            Look at https://www.django-rest-framework.org/ for details
            https://www.django-rest-framework.org/api-guide/responses/#response
        '''

        return Response(result)
