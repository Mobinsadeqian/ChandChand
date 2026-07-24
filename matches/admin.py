from django.contrib import admin
from .models import League, Match, Season, Team, Standing

admin.site.register(League)
admin.site.register(Team)
admin.site.register(Season)
admin.site.register(Match)
admin.site.register(Standing)