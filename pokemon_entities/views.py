import folium
import json

from datetime import datetime
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from pokemon_entities.models import Pokemon, PokemonEntitiy


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    now = datetime.now()
    entities = PokemonEntitiy.objects.filter(appeared_at__lte=now, disappeared_at__gt=now)
    
    for entity in entities:
        pokemon = entity.pokemon
        pokemon_image_url = request.build_absolute_uri(pokemon.photo.url)
        add_pokemon(
            folium_map, entity.lat, entity.lon, pokemon_image_url)

    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.photo.url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    pokemon_entities = PokemonEntitiy.objects.filter(pokemon=requested_pokemon)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            requested_pokemon.photo.path
        )

    pokemon_dict = {
        'pokemon_id': requested_pokemon.id,
        'img_url': requested_pokemon.photo.url,
        'title_ru': requested_pokemon.title,
        'description': requested_pokemon.description,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'previous_evolution': requested_pokemon.previous_evolution,
        'next_evolution': requested_pokemon.next_evolutions.first(),
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_dict
    })
