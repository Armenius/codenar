from django.conf.urls import url

from .views import ValidDomainIPView, SubdomainView

urlpatterns = [
    url('^$', ValidDomainIPView.as_view(), name='valid_domain_ip'),
    url('^subdomain', SubdomainView.as_view(), name='get_list_of_subdomains'),
    url('^crawl', ValidDomainIPView.as_view(), name='valid_domain_ip'),
]
