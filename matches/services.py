import requests
import time
from django.utils.dateparse import parse_datetime, parse_date
from .models import League, Season, Team, Match, Standing

API_KEY = '276242dab6b94dad84d799f5a5b7daa1'
BASE_URL = 'https://api.football-data.org/v4'
HEADERS = {'X-Auth-Token': API_KEY}

# لیگ‌های مدنظر (کد اختصاصی API)
LEAGUES = ['PL', 'PD', 'BL1', 'SA', 'FL1']


def fetch_and_update_api_data():
    """تابع اصلی برای بروزرسانی مسابقات و جداول رده‌بندی"""
    try:
        # ۱. آپدیت جدول و اطلاعات لیگ‌ها، فصل‌ها و تیم‌ها
        update_standings_and_leagues()

        # ۲. آپدیت بازی‌های روز (یا هفته جاری)
        update_today_matches()

        print("✅ تمامی داده‌های دیتابیس با موفقیت بروزرسانی شدند.")

    except Exception as e:
        print(f"❌ خطای کلی در اجرای سرویس بروزرسانی: {e}")


def update_standings_and_leagues():
    for code in LEAGUES:
        url = f"{BASE_URL}/competitions/{code}/standings"
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            data = response.json()

            # ۱. ذخیره یا بروزرسانی لیگ (League)
            comp_data = data['competition']
            league, _ = League.objects.update_or_create(
                api_id=comp_data['id'],
                defaults={
                    'name': comp_data['name'],
                    'code': comp_data['code'],
                    'country': comp_data.get('area', {}).get('name', ''),
                    'logo_url': comp_data.get('emblem', ''),
                }
            )

            # ۲. ذخیره یا بروزرسانی فصل (Season)
            season_data = data['season']
            season, _ = Season.objects.update_or_create(
                api_id=season_data['id'],
                defaults={
                    'league': league,
                    'start_date': parse_date(season_data['startDate']),
                    'end_date': parse_date(season_data['endDate']),
                    'current_matchday': season_data.get('currentMatchday'),
                }
            )

            # ۳. ذخیره یا بروزرسانی جدول (Standing) و تیم‌ها (Team)
            # در API معمولا نوع 'TOTAL' مدنظر ماست
            standings_list = data.get('standings', [])
            total_standing = next((s for s in standings_list if s.get('type') == 'TOTAL'), None)

            if total_standing:
                for table_row in total_standing.get('table', []):
                    team_data = table_row['team']

                    # ساخت/بروزرسانی تیم
                    team, _ = Team.objects.update_or_create(
                        api_id=team_data['id'],
                        defaults={
                            'name': team_data['name'],
                            'short_name': team_data.get('shortName', team_data['name']),
                            'crest_url': team_data.get('crest', ''),
                        }
                    )

                    # ساخت/بروزرسانی موقعیت تیم در جدول
                    Standing.objects.update_or_create(
                        league=league,
                        team=team,
                        defaults={
                            'position': table_row['position'],
                            'played': table_row['playedGames'],
                            'won': table_row['won'],
                            'drawn': table_row['draw'],
                            'lost': table_row['lost'],
                            'points': table_row['points'],
                            'goals_for': table_row['goalsFor'],
                            'goals_against': table_row['goalsAgainst'],
                            'goal_difference': table_row['goalDifference'],
                        }
                    )
            print(f"جدول لیگ {league.name} بروزرسانی شد.")
        elif response.status_code == 429:
            print("⚠️ محدودیت API (Rate Limit)! چند لحظه صبر کنید...")
        else:
            print(f"خطا در دریافت جدول {code}: {response.status_code}")

        # وقفه ۲ ثانیه‌ای جهت رعایت Rate Limit
        time.sleep(2)


def update_today_matches():
    url = f"{BASE_URL}/matches"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()

        for match_item in data.get('matches', []):
            comp_id = match_item['competition']['id']

            # اگر لیگ بازی در دیتابیس ما ثبت شده باشد
            league = League.objects.filter(api_id=comp_id).first()
            if not league:
                continue

            season = Season.objects.filter(api_id=match_item['season']['id']).first()

            # دریافت/ایجاد تیم میزبان و مهمان
            home_team, _ = Team.objects.update_or_create(
                api_id=match_item['homeTeam']['id'],
                defaults={
                    'name': match_item['homeTeam']['name'],
                    'short_name': match_item['homeTeam'].get('shortName', ''),
                    'crest_url': match_item['homeTeam'].get('crest', ''),
                }
            )

            away_team, _ = Team.objects.update_or_create(
                api_id=match_item['awayTeam']['id'],
                defaults={
                    'name': match_item['awayTeam']['name'],
                    'short_name': match_item['awayTeam'].get('shortName', ''),
                    'crest_url': match_item['awayTeam'].get('crest', ''),
                }
            )

            # امتیازات
            score_fulltime = match_item.get('score', {}).get('fullTime', {})

            # ذخیره یا بروزرسانی بازی
            Match.objects.update_or_create(
                api_id=match_item['id'],
                defaults={
                    'league': league,
                    'season': season,
                    'matchday': match_item.get('matchday'),
                    'home_team': home_team,
                    'away_team': away_team,
                    'starting_at': parse_datetime(match_item['utcDate']),
                    'status': match_item['status'],
                    'home_score': score_fulltime.get('home'),
                    'away_score': score_fulltime.get('away'),
                }
            )
        print("بازی‌های امروز بروزرسانی شدند.")