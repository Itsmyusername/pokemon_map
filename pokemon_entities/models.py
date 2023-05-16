from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название на русском')
    title_en = models.CharField(default='title en', max_length=100, verbose_name='Название на английском', blank=True)
    title_jp = models.CharField(default='title jp', max_length=100, verbose_name='Название на японском', blank=True)
    photo = models.ImageField(blank=True, verbose_name='Изображение')
    description = models.TextField(default='desc', verbose_name='Описание', blank=True) 
    previous_evolution = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='next_evolutions', verbose_name='Предыдущая эволюция')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='entities', verbose_name='Название на русском')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(blank=True, verbose_name='Появится с ...')
    disappeared_at = models.DateTimeField(blank=True, verbose_name='Исчезнет до ...')
    level = models.IntegerField(blank=True, verbose_name='Уровень')
    health = models.IntegerField(blank=True, verbose_name='Здоровье')
    strength = models.IntegerField(blank=True, verbose_name='Сила')
    defence = models.IntegerField(blank=True, verbose_name='Защита')
    stamina = models.IntegerField(blank=True, verbose_name='Выносливость')

    def __str__(self):
        return f'{self.pokemon}'
