from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateQuackView, RetrieveQuackView, ListDucklingsView 
from .views import RegisterUserView, UpdateSettingsView, SyncToNewerQuackView
from .views import ModeratorListView, ModeratorUpdateView

urlpatterns = {
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^postquack/$', CreateQuackView.as_view(), name="createquack"),
    url(r'^retrievequacks/(\d{1,2})/$', RetrieveQuackView.as_view(), name="getquacks"),
#    url(r'^ducklings/$', ListDucklingsView.as_view(), name="getducklings"),
    url(r'^registeruser/$', RegisterUserView.as_view(), name="registeruser"),
#    url(r'^createduckling/$', CreateDucklingView.as_view(), name="createduckling"),
    url(r'^getupdateduckling/$', UpdateSettingsView.as_view(), name="update"),
    url(r'^synctonewer/$', SyncToNewerQuackView.as_view(), name ="sync"),
    url(r'^moderatorlist/(\d{1,2})/$', ModeratorListView.as_view(), name="moderatorlist"),
    url(r'^moderatorupdate/(?P<pk>\d+)/$', ModeratorUpdateView.as_view(), name="moderatorupdate"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
