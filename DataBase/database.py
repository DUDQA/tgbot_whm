import psycopg2
from contextlib import closing


class DataBase:
    def __init__(self, creds):
        self.creds = creds

    def truncate_table_genre(self, genre: str) -> None:
        with closing(psycopg2.connect(database=self.creds['database'], user=self.creds['user'],
                                      password=self.creds['password'], host=self.creds['host'],
                                      port=self.creds['port'])) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'TRUNCATE TABLE {genre} RESTART IDENTITY')

            conn.commit()

    def create_table_genre(self, genre: str) -> None:
        with closing(psycopg2.connect(database=self.creds['database'], user=self.creds['user'],
                                      password=self.creds['password'], host=self.creds['host'],
                                      port=self.creds['port'])) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f'CREATE TABLE {genre} (track_id serial PRIMARY KEY, artist varchar(32), track_name varchar(64), n_of_plays bigint)')
            conn.commit()

    def input_track_data(self, genre: str, data: list) -> None:
        with closing(psycopg2.connect(database=self.creds['database'], user=self.creds['user'],
                                      password=self.creds['password'], host=self.creds['host'],
                                      port=self.creds['port'])) as conn:
            with conn.cursor() as cursor:
                for track in data:
                    i = 0
                    cursor.execute(f'INSERT into {genre} (artist, track_name, n_of_plays) VALUES (%s, %s, %s)', track)
            conn.commit()

    def get_track_data(self, genre: str, track_id: int) -> list:
        with closing(psycopg2.connect(database=self.creds['database'], user=self.creds['user'],
                                      password=self.creds['password'], host=self.creds['host'],
                                      port=self.creds['port'])) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f'SELECT artist, track_name, n_of_plays, track_id, photo FROM {genre} WHERE track_id = {track_id}')
                data = cursor.fetchall()
            conn.commit()
        return data[0]

    def set_user_data(self, user_id, in_game_status: bool = False, current_points=0, max_points=0):
        with closing(psycopg2.connect(database=self.creds['database'], user=self.creds['user'],
                                      password=self.creds['password'], host=self.creds['host'],
                                      port=self.creds['port'])) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f'INSERT INTO user_data (user_id, in_game_status, current_points, max_points) VALUES ({user_id}, {in_game_status}, {current_points}, {max_points})')
                conn.commit()

    def get_user_data(self, user_id):
        with closing(psycopg2.connect(database=self.creds['database'], user=self.creds['user'],
                                      password=self.creds['password'], host=self.creds['host'],
                                      port=self.creds['port'])) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'SELECT * FROM user_data WHERE user_id={user_id}')
                data = cursor.fetchall()
            conn.commit()
        if not data:
            return None
        else:
            user_data = {'user_id': user_id,
                         'in_game_status': data[0][1],
                         'current_points': data[0][2],
                         'task_1': data[0][3],
                         'task_2': data[0][4],
                         'streams_1': data[0][5],
                         'streams_2': data[0][6],
                         'comparison': data[0][7],
                         'max_points': data[0][8]
                         }
            return user_data

    def upd_user_data(self, user_id: int, task1: str = None, task2: str = None, number1: int = None,
                      number2: int = None, comp: str = None):
        with closing(psycopg2.connect(database=self.creds['database'], user=self.creds['user'],
                                      password=self.creds['password'], host=self.creds['host'],
                                      port=self.creds['port'])) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"UPDATE user_data SET task1 = '{task1}', task2 = '{task2}', "
                    f"number1 = {number1}, number2 = {number2}, comp = {comp} WHERE user_id = {user_id}")
            conn.commit()

    def change_points(self, user_id: int, add: bool = False, current_points: int = None, max_points: int = None):
        with closing(psycopg2.connect(database=self.creds['database'], user=self.creds['user'],
                                      password=self.creds['password'], host=self.creds['host'],
                                      port=self.creds['port'])) as conn:
            with conn.cursor() as cursor:
                if add is True:
                    cursor.execute(f"UPDATE user_data SET current_points = current_points+1 WHERE user_id = {user_id}")
                elif max_points is not None:
                    cursor.execute(f"UPDATE user_data SET max_points = {max_points} WHERE user_id = {user_id}")
                else:
                    cursor.execute(f"UPDATE user_data SET current_points = {current_points} WHERE user_id = {user_id}")
            conn.commit()

    def change_status(self, user_id: int, in_game_status: bool = False):
        with closing(psycopg2.connect(database=self.creds['database'], user=self.creds['user'],
                                      password=self.creds['password'], host=self.creds['host'],
                                      port=self.creds['port'])) as conn:
            with conn.cursor() as cursor:
                if in_game_status is True:
                    cursor.execute(f"UPDATE user_data SET in_game_status = True WHERE user_id = {user_id}")
                else:
                    cursor.execute(f"UPDATE user_data SET in_game_status = False WHERE user_id = {user_id}")
            conn.commit()

    def set_msgid(self, user_id: int, message_id1, message_id2) -> None:

        with closing(psycopg2.connect(database=self.creds['database'], user=self.creds['user'],
                                      password=self.creds['password'], host=self.creds['host'],
                                      port=self.creds['port'])) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f'INSERT INTO messages (user_id, msg1, msg2) VALUES ({user_id}, {message_id1}, {message_id2})')
            conn.commit()

    def upd_msgid(self, user_id: int, message_id1, message_id2) -> None:

        with closing(psycopg2.connect(database=self.creds['database'], user=self.creds['user'],
                                      password=self.creds['password'], host=self.creds['host'],
                                      port=self.creds['port'])) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f'UPDATE messages SET msg1 = {message_id1}, msg2 = {message_id2} WHERE user_id = {user_id}')
                conn.commit()

    def get_msgid(self, user_id):
        with closing(psycopg2.connect(database=self.creds['database'], user=self.creds['user'],
                                      password=self.creds['password'], host=self.creds['host'],
                                      port=self.creds['port'])) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'SELECT msg1, msg2 FROM messages WHERE user_id={user_id}')
                data = cursor.fetchall()
            conn.commit()
        if not data:
            return None
        else:
            return data[0]
