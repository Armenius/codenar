from django.conf.urls import url, include
from django.contrib import admin

# Swagger import 
from rest_framework_swagger.views import get_swagger_view

'''
Swagger injection

[TODO] change its template
https://django-rest-swagger.readthedocs.io/en/latest/customization/

setting.py - INSTALLED apps 'rest_framework_swagger',

function - get_swagger_view
https://django-rest-swagger.readthedocs.io/en/latest/
'''

schema_view = get_swagger_view(title='Codenar API')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^swagger/$', schema_view),
    url(r'^api/', include('api.urls')),
]
