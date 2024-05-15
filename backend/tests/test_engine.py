from src.utils.utils import (
    get_artist,
    search_artist,
    get_playlist,
    search_playlist,
    get_recommendation
)
import json


def test_search_artist():
    """
    Search artist given name
    """
    artist = search_artist("Justin Bieber")
    assert artist['items'][0]['name'] == "Justin Bieber"

    artist = search_artist("Hà Anh Tuấn")
    print(json.dumps(artist, indent=2))
    assert artist['items'][0]['name'] == "Hà Anh Tuấn"


def test_get_artist():
    """
    Get artist given artist id
    """
    artist = get_artist('1uNFoZAHBGtllmzznpCI3s')
    print(json.dumps(artist, indent=2))
    assert artist['name'] == "Justin Bieber"


def test_get_playlist():
    """
    Get playlist given url
    """
    playlist = get_playlist(
        "https://open.spotify.com/playlist/2xukpbxolEK8C9HdpANzZu?si=bbe1304cc2f74b31")
    assert playlist['type'] == 'playlist'


def test_search_playlist():
    """
    Search playlist with keyword
    """
    playlist = search_playlist("korean soft indie")
    print(json.dumps(playlist, indent=2))
    assert "korean" in playlist['name']


def test_get_recommendation():
    artist_ids = ['1uNFoZAHBGtllmzznpCI3s', '5IH6FPUwQTxPSXurCrcIov']
    data = get_recommendation(artist_ids)
    print(json.dumps(data, indent=2))

    # Check each track data has the same structure
    keys = data[0].keys()
    for item in data[1:]:
        assert item.keys() == keys
