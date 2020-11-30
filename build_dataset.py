from tqdm import tqdm
from face_ult.data_updater import ArtistDataBuilder, ArtistGenerator


if __name__ == '__main__':
    artists = ArtistGenerator.get_artist()

    DIR = 'data'
    # print(artists)
    for i, artist in tqdm(enumerate(artists, start=1)):
        print(f"\n term {i} - building: {artist}")
        builder = ArtistDataBuilder(DIR, artist)
        builder.launch()
        print(f'\n {i} - finish \n')
