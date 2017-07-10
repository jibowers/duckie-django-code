from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateQuackView

urlpatterns = {
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^quacks/$', CreateQuackView.as_view(), name="createquack"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
