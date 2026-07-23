from django.core.management.base import BaseCommand
from matches.models import Team

class Command(BaseCommand):
    help = "ترجمه و فارسی‌سازی نام تیم‌ها در دیتابیس"

    def handle(self, *args, **options):
        TRANSLATIONS = {
            # --- فرانسه (Ligue 1 / Ligue 2) ---
            "AS Monaco FC": "موناکو",
            "Le Havre AC": "لو اور",
            "Olympique Lyonnais": "لیون",
            "Toulouse FC": "تولوز",
            "Lille OSC": "لیل",
            "Angers SCO": "آنژه",
            "FC Lorient": "لوریان",
            "OGC Nice": "نیس",
            "RC Strasbourg Alsace": "استراسبورگ",
            "Olympique de Marseille": "مارسی",
            "Paris FC": "پاریس اف‌سی",
            "ES Troyes AC": "تروآ",
            "Stade Rennais FC 1901": "رن",
            "Paris Saint-Germain FC": "پاری سن ژرمن",
            "AJ Auxerre": "اوسر",
            "Racing Club de Lens": "لانس",
            "Stade Brestois 29": "برست",
            "Le Mans FC": "لومان",

            # --- آلمان (Bundesliga / 2. Bundesliga) ---
            "FC Schalke 04": "شالکه",
            "FC Augsburg": "آگزبورگ",
            "SV Werder Bremen": "وردربرمن",
            "SC Freiburg": "فرایبورگ",
            "Hamburger SV": "هامبورگ",
            "Borussia Dortmund": "دورتموند",
            "TSG 1899 Hoffenheim": "هوفنهایم",
            "1. FC Köln": "کلن",
            "Bayer 04 Leverkusen": "بایر لورکوزن",
            "SV 07 Elversberg": "الورسبرگ",
            "Eintracht Frankfurt": "اینتراخت فرانکفورت",
            "1. FC Union Berlin": "یونیون برلین",
            "SC Paderborn 07": "پادربورن",
            "1. FSV Mainz 05": "ماینتس",
            "Borussia Mönchengladbach": "بوروسیا مونشن‌گلادباخ",
            "RB Leipzig": "لاینپزیگ",
            "VfB Stuttgart": "اشتوتگارت",
            "FC Bayern München": "بایرن مونیخ",

            # --- ایتالیا (Serie A / Serie B) ---
            "ACF Fiorentina": "فیورنتینا",
            "AS Roma": "رم",
            "SS Lazio": "لاتسیو",
            "Bologna FC 1909": "بولونیا",
            "AC Milan": "میلان",
            "Torino FC": "تورینو",
            "US Sassuolo Calcio": "ساسولو",
            "Atalanta BC": "آتالانتا",
            "US Lecce": "لچه",
            "Venezia FC": "ونزیا",
            "Juventus FC": "یوونتوس",
            "Frosinone Calcio": "فروزینونه",
            "Cagliari Calcio": "کالیاری",
            "Parma Calcio 1913": "پارما",
            "SSC Napoli": "ناپولی",
            "Genoa CFC": "جنوا",
            "AC Monza": "مونتزا",
            "FC Internazionale Milano": "اینتر",
            "Como 1907": "کومو",
            "Udinese Calcio": "ادینزه",

            # --- اسپانیا (LaLiga / Segunda División) ---
            "FC Barcelona": "بارسلونا",
            "Real Madrid CF": "رئال مادرید",
            "Valencia CF": "والنسیا",
            "Athletic Club": "اتلتیک بیلبائو",
            "Real Sociedad de Fútbol": "رئال سوسیداد",
            "Real Betis Balompié": "رئال بتیس",
            "Málaga CF": "مالاگا",
            "Club Atlético de Madrid": "اتلتیکو مادرید",
            "Elche CF": "الچه",
            "RC Deportivo La Coruña": "دپورتیوو لاکرونیا",
            "CA Osasuna": "اوساسونا",
            "RC Celta de Vigo": "سلتاویگو",
            "Levante UD": "لوانته",
            "RCD Espanyol de Barcelona": "اسپانیول",
            "Villarreal CF": "ویارئال",
            "Real Racing Club de Santander": "راسینگ سانتاندر",
            "Rayo Vallecano de Madrid": "رایو وایکانو",
            "Sevilla FC": "سویا",
            "Getafe CF": "ختافه",
            "Deportivo Alavés": "آلاوز",

            # --- انگلیس (Premier League / Championship) ---
            "Chelsea FC": "چلسی",
            "Fulham FC": "فولام",
            "Liverpool FC": "لیورپول",
            "Newcastle United FC": "نیوکاسل",
            "Aston Villa FC": "استون ویلا",
            "Brighton & Hove Albion FC": "برایتون",
            "AFC Bournemouth": "بورنموث",
            "Manchester City FC": "منچستر سیتی",
            "Tottenham Hotspur FC": "توتنهام",
            "Brentford FC": "برنتفورد",
            "Crystal Palace FC": "کریستال پالاس",
            "Everton FC": "اورتون",
            "Leeds United FC": "لیدز یونایتد",
            "Nottingham Forest FC": "ناتینگام فارست",
            "Sunderland AFC": "ساندرلند",
            "Ipswich Town FC": "ایپسویچ تاون",
            "Manchester United FC": "منچستر یونایتد",
            "Hull City AFC": "هال سیتی",
            "Coventry City FC": "کاونتری سیتی",
            "Arsenal FC": "آرسنال",
        }

        updated_count = 0

        for eng_name, fa_name in TRANSLATIONS.items():
            teams = Team.objects.filter(name=eng_name)
            for team in teams:
                team.persian_name = fa_name
                team.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"تیم '{eng_name}' به '{fa_name}' تغییر یافت."))

        self.stdout.write(self.style.SUCCESS(f"\nپایان عملیات! مجموعاً {updated_count} تیم ترجمه شدند."))        