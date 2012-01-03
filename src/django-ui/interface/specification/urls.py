from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from specification.views import SimulationListView, dashboard_view

urlpatterns = patterns('specification.views',
    url(r'^simulations/$', login_required(SimulationListView.as_view(
        template_name="specification/simulations.html")),
        name="simulations"),
    url(r'^dashboard/(?P<pk>\d+)$', login_required(dashboard_view),
        name="dashboard"),
)
