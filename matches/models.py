from django.db import models

class League(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام لیگ")
    persian_name = models.CharField(max_length=60, null=True, blank=True)
    code = models.CharField(max_length=10, verbose_name="کد لیگ")
    country = models.CharField(max_length=100, verbose_name="کشور صاحب لیگ")
    logo_url = models.URLField(blank=True, verbose_name="آدرس لوگو")
    api_id = models.IntegerField(unique=True, verbose_name="شناسه API")

    def __str__(self):
        return f"The league {self.name} in {self.country}"

    class Meta:
        verbose_name = "لیگ"
        verbose_name_plural = "لیگ‌ها"

class Season(models.Model):
    league = models.ForeignKey(League, related_name="seasons", on_delete=models.CASCADE, verbose_name="لیگ مربوطه")
    start_date = models.DateField(verbose_name="تاریخ شروع لیگ")
    end_date = models.DateField(verbose_name="تاریخ پایان لیگ")
    current_matchday = models.IntegerField(null=True, blank=True, verbose_name="هفته فعلی")
    api_id = models.IntegerField(unique=True, verbose_name="شناسه API فصل")

    def __str__(self):
        return f"{self.league.name}: {self.start_date} -> {self.start_date.year}"

    class Meta:
        verbose_name = "فصل"
        verbose_name_plural = "فصل‌ها"

class Team(models.Model):
    persian_name = models.CharField(max_length=60, null=True, blank=True)
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=40)
    crest_url = models.URLField(blank=True)
    api_id = models.IntegerField(unique=True, verbose_name="شناسه API")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "تیم"
        verbose_name_plural = "تیم‌ها"        

class Match(models.Model):
    STATUS_CHOICES = [
        ('SCHEDULED', 'برنامه‌ریزی شده'),
        ('TIMED', 'زمان‌بندی شده'),
        ('IN_PLAY', 'در حال برگزاری'),
        ('PAUSED', 'بین دو نیمه'),
        ('EXTRA_TIME', 'وقت اضافه'),
        ('PENALTY_SHOOTOUT', 'ضربات پنالتی'),
        ('FINISHED', 'پایان یافته'),
        ('SUSPENDED', 'تعلیق شده'),
        ('POSTPONED', 'به تعویق افتاده'),
        ('CANCELLED', 'لغو شده'),
        ('AWARDED', 'رای کمیته انضباطی'),
    ]

    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="matches", verbose_name="لیگ‌")
    season = models.ForeignKey(Season, related_name="season_mathces", on_delete=models.CASCADE, verbose_name="فصل")
    matchday = models.IntegerField(null=True, blank=True, verbose_name="هفته بازی")
    home_team = models.ForeignKey(Team, related_name="home_matches", on_delete=models.CASCADE, verbose_name="تیم میزبان")
    away_team = models.ForeignKey(Team, related_name="away_matches", on_delete=models.CASCADE, verbose_name="تیم مهمان")
    starting_at = models.DateTimeField(verbose_name="زمان شروع بازی")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="وضعیت بازی")
    home_score = models.IntegerField(null=True, blank=True, verbose_name="گل میزبان")
    away_score = models.IntegerField(null=True, blank=True, verbose_name="گل مهمان")
    api_id = models.IntegerField(unique=True, verbose_name="شناسه API")

    def __str__(self):
        home_g = self.home_score if self.home_score is not None else "-"
        away_g = self.away_score if self.away_score is not None else "-"
        return f"{self.home_team.name} {home_g} - {away_g} {self.away_team.name}" 

    class Meta:
        verbose_name = "بازی"
        verbose_name_plural = "بازی‌ها"


class Standing(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="standings")
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    played = models.PositiveIntegerField(default=0)
    won = models.PositiveIntegerField(default=0)
    drawn = models.PositiveIntegerField(default=0)
    lost = models.PositiveIntegerField(default=0)
    points = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)
    goal_difference = models.IntegerField(default=0)

    class Meta:
        ordering = ['position']
        verbose_name = "رده‌بندی تیم"
        verbose_name_plural = "جدول‌های رده‌بندی"

    def __str__(self):
        return f"{self.league.name} - {self.position}. {self.team.name}"
                