from django.shortcuts import render, get_object_or_404
from .models import League, Team, Season, Match, Standing
from django.utils import timezone
import jdatetime
from zoneinfo import ZoneInfo
from django.db.models import Q
def home(request):
    teams = Team.objects.all()
    leagues = League.objects.all()
    now_tehran = timezone.now().astimezone(ZoneInfo('Asia/Tehran'))
    today_jalali = jdatetime.datetime.fromgregorian(datetime=now_tehran)
    today = timezone.now().date()
    today_matches = Match.objects.filter(starting_at__date=today).order_by('starting_at')[:5]
    context = {
        'leagues' : leagues,
        'today_matches': today_matches,
        'teams': teams,
        'today_jalali': today_jalali,
    }
    return render(request, 'matches/home.html', context)

def league_page(request, league_code):
    league_info = get_object_or_404(League, code=league_code)
    matches = Match.objects.filter(league=league_info).order_by('starting_at')
    standing_tables = Standing.objects.filter(league=league_info).select_related("team")

    context = {
        "league_info": league_info,
        'matches': matches,
        'standing_tables': standing_tables
    }
    return render(request, 'matches/league.html', context)


def team_info(request, short_name):
    team = get_object_or_404(Team, short_name=short_name)
    home_matches = Match.objects.filter(home_team=team).order_by('starting_at')
    away_matches = Match.objects.filter(away_team=team).order_by('starting_at')
    matches = Match.objects.filter(Q(home_team=team) | Q(away_team=team)).select_related('home_team', 'away_team', 'league').order_by('starting_at')

    context = {
        'team': team,
        'home_matches': home_matches,
        'away_matches': away_matches,
        'matches': matches,
    }
    return render(request, 'matches/team_info.html', context)

