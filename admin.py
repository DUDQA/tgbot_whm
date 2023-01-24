from database import DataBase
from scraper import prepare_data
import artists


def refresh_data_metal():
    db = DataBase()
    db.truncate_table_genre('metal')
    for artist_url in artists.metal:
        url = artists.metal[artist_url]
        prepd = prepare_data(url)
        db.input_track_data('metal', prepd)


refresh_data_metal()

