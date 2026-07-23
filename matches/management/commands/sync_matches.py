import requests

from django.core.management.base import BaseCommand
from matches.models import League, Team, Season, Match

class Command(BaseCommand):
    help = "دریافت اطلاعات لیگ‌های مختلف از API و ذخیره در دیتابیس"

    def add_arguments(self, parser):
        parser.add_argument('league_code', type=str, help='کد اختصاصی لیگ (مثلا PL یا PD)')

    def handle(self, *args, **options):
        API_TOKEN = "276242dab6b94dad84d799f5a5b7daa1"

        league_code = options['league_code']

        headers = {
            'X-Auth-Token': API_TOKEN
        }

        url = f"https://api.football-data.org/v4/competitions/{league_code}/matches"

        self.stdout.write(self.style.WARNING("در حال اتصال به API..."))

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()

            comp_data = data['competition']
            area_info = comp_data.get('area', {})
            country_name = area_info.get('name', 'International') if isinstance(area_info, dict) else "International"

            league, _ = League.objects.get_or_create(
                api_id=comp_data['id'],
                defaults={
                    'name': comp_data['name'],
                    'code': comp_data['code'],
                    'country': country_name,
                    'logo_url': comp_data.get('emblem', '')

                }
            )
            self.stdout.write(f'لیگ بررسی شد: {league.name}')

            matches_data = data['matches']
            match_count = 0

            for m in matches_data:
                season_data = m['season']
                season, _ = Season.objects.get_or_create(
                    api_id = season_data['id'],
                    defaults={
                        'league': league,
                        'start_date': season_data['startDate'],
                        'end_date': season_data['endDate'],
                        'current_matchday': season_data.get('currentMatchday')
                    }
                )
                home_data = m['homeTeam']
                home_team, _ = Team.objects.get_or_create(
                    api_id = home_data['id'],
                    defaults={
                        'name': home_data['name'],
                        'short_name': home_data.get('shortName', home_data['name']),
                        'crest_url': home_data.get('crest', '')
                    }
                )
                away_data = m['awayTeam']
                away_team, _ = Team.objects.get_or_create(
                    api_id=away_data['id'],
                    defaults={
                        'name': away_data['name'],
                        'short_name': away_data.get('shortName', away_data['name']),
                        'crest_url': away_data.get('crest', '')
                    }
                )

                Match.objects.update_or_create(
                    api_id=m['id'],
                    defaults={
                        'league': league,
                        'season': season,
                        'matchday': m.get('matchday'),
                        'home_team': home_team,
                        'away_team': away_team,
                        'starting_at': m['utcDate'],
                        'status': m['status'],
                        'home_score': m['score']['fullTime']['home'],
                        'away_score': m['score']['fullTime']['away'],
                    }
                )

                match_count += 1

            self.stdout.write(self.style.SUCCESS(f'عملیات موفقیت‌آمیز بود! {match_count} بازی برای لیگ {league_code} ثبت/بروزرسانی شد.'))
            
        else:
            self.stdout.write(self.style.ERROR(f'خطا در دریافت اطلاعات. کد ارور: {response.status_code}'))
            self.stdout.write(response.text)