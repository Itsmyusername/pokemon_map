from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    photo = models.ImageField(null=True)
    description = models.TextField(default='desc')
    title_en = models.CharField(default='title en', max_length=100)
    title_jp = models.CharField(default='title jp', max_length=100)
    previous_evolution = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='next_evolutions')

    def __str__(self):
        return f'{self.title}'


class PokemonEntitiy(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(null=True)
    disappeared_at = models.DateTimeField(null=True)
    level = models.IntegerField(default=0)
    health = models.IntegerField(default=0)
    strength = models.IntegerField(default=0)
    defence = models.IntegerField(default=0)
    stamina = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.pokemon}'
