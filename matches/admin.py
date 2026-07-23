from django.contrib import admin
from .models import League, Match, Season, Team

admin.site.register(League)
admin.site.register(Team)
admin.site.register(Season)
admin.site.register(Match)