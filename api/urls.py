from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateQuackView, RetrieveQuackView

urlpatterns = {
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^postquack/$', CreateQuackView.as_view(), name="createquack"),
    url(r'^retrievequacks/$', RetrieveQuackView.as_view(), name="getquacks"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
