from database import DataBase
from scraper import Scraper
import artists


db = DataBase()
sc = Scraper()


def refresh_data_metal(genre: str) -> None:
    db.truncate_table_genre(genre)
    for artist_url in artists.metal:
        url = artists.metal[artist_url]
        prepared_data = sc.prepare_data(url)
        db.input_track_data('metal', prepared_data)
