from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateQuackView, RetrieveQuackView, ListDucklingsView 
from .views import RegisterUserView, UpdateSettingsView

urlpatterns = {
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^postquack/$', CreateQuackView.as_view(), name="createquack"),
    url(r'^retrievequacks/$', RetrieveQuackView.as_view(), name="getquacks"),
    url(r'^ducklings/$', ListDucklingsView.as_view(), name="getducklings"),
    url(r'^registeruser/$', RegisterUserView.as_view(), name="registeruser"),
#    url(r'^createduckling/$', CreateDucklingView.as_view(), name="createduckling"),
    url(r'^update/$', UpdateSettingsView.as_view(), name="update"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
