from django.urls import path
from . import views 
urlpatterns = [
    path("", views.home, name="home"),
    path("league/<league_code>", views.league_page, name="league_page"),
    path("team/<path:short_name>/", views.team_info, name='team_info'),
    path('api/cron/update-matches/', views.trigger_fetch_matches, name='cron_update_matches'),

]