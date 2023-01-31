import random
from database import DataBase

db = DataBase()


class Option:

    def __init__(self, artist: str, song_name: str, number: int, track_id: int, photo: str):
        self.track_id = track_id
        self.artist = artist
        self.song_name = song_name
        self.number = number
        self.photo = photo


def pair_generator(db_range):   #генератор 2 случайных song_id с необходимыми условиями
    id1 = random.randint(1, db_range)
    id2 = random.randint(1, db_range)
    while id1 == id2:
        try:
            id2 = random.randint(1, id1 - 1)
        except ValueError:
            id2 = random.randint(id1 + 1, db_range)
    else:
        if abs(id1 - id2) > 4:
            return [id1, id2]
        else:
            id2 = id1 + 5
            if id2 > db_range:
                id2 = id1 - 5
        return id1, id2


def gen_q():  #генератор вопроса
    song_ids = pair_generator(150)
    data1 = db.get_track_data('metal', song_ids[0])
    data2 = db.get_track_data('metal', song_ids[1])
    opt1 = Option(data1[0], data1[1], data1[2], data1[3], data1[4])
    opt2 = Option(data2[0], data2[1], data2[2], data2[3], data2[4])
    if opt1.number > opt2.number:
        comparison = '1'
    else:
        comparison = '2'
    task1 = f"{opt1.artist} - {opt1.song_name}"
    task2 = f"{opt2.artist} - {opt2.song_name}"
    number1 = opt1.number
    number2 = opt2.number
    photo1 = opt1.photo
    photo2 = opt2.photo
    return task1, task2, number1, number2, comparison, photo1, photo2





