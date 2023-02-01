import random
from database import DataBase

db = DataBase()


def pair_id_generator(db_range: int) -> list:
    """Creates a pair of track IDs, but with gap greater than 4."""
    track_id_1 = random.randint(1, db_range)
    track_id_2 = random.randint(1, db_range)
    while track_id_1 == track_id_2:
        try:
            track_id_2 = random.randint(1, track_id_1 - 1)
        except ValueError:
            track_id_2 = random.randint(track_id_1 + 1, db_range)
    else:
        if abs(track_id_1 - track_id_2) > 4:
            return [track_id_1, track_id_2]
        else:
            track_id_2 = track_id_1 + 5
            if track_id_2 > db_range:
                track_id_2 = track_id_1 - 5
        return [track_id_1, track_id_2]


def task_generator() -> dict:
    """Builds a dictionary storing data for two questions."""
    track_ids = pair_id_generator(150)
    track_data_1 = db.get_track_data('metal', track_ids[0])
    track_data_2 = db.get_track_data('metal', track_ids[1])
    task = {'option_1': f'{track_data_1[0]} - {track_data_1[1]}',
            'streams_1': track_data_1[2],
            'track_id_1': track_data_1[3],
            'photo_1': track_data_1[4],
            'option_2': f'{track_data_2[0]} - {track_data_2[1]}',
            'streams_2': track_data_2[2],
            'track_id_2': track_data_2[3],
            'photo_2': track_data_2[4]
            }
    if task['streams_1'] > task['streams_2']:
        task['comparison'] = '1'
    else:
        task['comparison'] = '2'
    return task