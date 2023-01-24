import requests
from bs4 import BeautifulSoup


# turn VPN on!


def show_data(url):
    artist_data = []
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')

    artist = soup.find('h1', class_="Type__TypeElement-sc-goli3j-0 ilmalU gj6rSoF7K4FohS2DJDEm")
    artist_data.append(artist.contents[0])

    tracks = soup.find_all('a', class_="_4R6oAAgA1uWIjEr03kKg")
    for track in tracks:
        x = track.contents
        artist_data.append(x[0])
    listens = soup.find_all('span', class_="Type__TypeElement-sc-goli3j-0 hGXzYa q4zy5NZC9Y8dyoZW76eb")
    for number in listens:
        x = number.contents
        artist_data.append(int(x[0].replace(',', '')))
    print(artist_data)


def prepare_data(url: str):
    artist_data = []
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')

    artist = soup.find('h1', class_="Type__TypeElement-sc-goli3j-0 ilmalU gj6rSoF7K4FohS2DJDEm")
    artist_data.append(artist.contents[0])

    tracks = soup.find_all('a', class_="_4R6oAAgA1uWIjEr03kKg")
    for track in tracks:
        x = track.contents
        artist_data.append(x[0])
    listens = soup.find_all('span', class_="Type__TypeElement-sc-goli3j-0 hGXzYa q4zy5NZC9Y8dyoZW76eb")
    for number in listens:
        x = number.contents
        artist_data.append(int(x[0].replace(',', '')))
    artist_data = [(artist_data[0], artist_data[1], artist_data[6]),
                   (artist_data[0], artist_data[2], artist_data[7]),
                   (artist_data[0], artist_data[3], artist_data[8]),
                   (artist_data[0], artist_data[4], artist_data[9]),
                   (artist_data[0], artist_data[5], artist_data[10])]
    return artist_data
