import spotipy
import spotipy.util as util
import random

#認証設定
username = '____your_username____'
my_id = '____your_ClientID____'
my_secret = '____your_ClientSecret____'
redirect_uri = '____your_Redirect_URI____'

#権限付与
scope = 'user-library-read user-read-playback-state playlist-read-private user-read-recently-played playlist-read-collaborative playlist-modify-public playlist-modify-private'
#認証
token = util.prompt_for_user_token(username, scope, my_id, my_secret, redirect_uri)
spotify = spotipy.Spotify(auth = token)

def creat_play_list(list_name = 'apiプレイリスト'):
    spotify.user_playlist_create(username, list_name)
    list_data = spotify.user_playlists(username)
    for i in range(list_data['total']):
        play_list_name = list_data['items'][i]['name']
        if play_list_name == list_name:
            url = list_data['items'][i]['external_urls']['spotify']
        else:
            pass
    return(url)

def track_info(limit = 50):
    track_urls = []
    track_times = []
    offset = 0
    saved_tracks = spotify.current_user_saved_tracks(limit = limit, offset = offset)
    total = saved_tracks['total']
    while True:
        if (total > 50):
            set = 50
            total = total -50
        else:
            set = total
        saved_tracks = spotify.current_user_saved_tracks(limit = limit, offset = offset)
        for i in range(set):
            track_url = saved_tracks['items'][i]['track']['external_urls']['spotify']
            track_urls.append(track_url)
            track_time = saved_tracks['items'][i]['track']['duration_ms']
            track_times.append(track_time)
        if saved_tracks['next'] is not None:
            offset += 50
        else:
            break
    track = list(zip(track_urls,track_times))
    return (track)

list_time = float(input("制作したいプレイリストの時間入力してください(分)："))

track = track_info()
random.shuffle(track)
now_time = 0
ans = 0
just_list = []
for i in range(len(track)):
    if ans < list_time:
        now_time = track[i][1]
        ans += now_time/60000
        just_list.append(track[i][0])

num = random.randrange(1, 9999)
playlist_url = creat_play_list(str(int(list_time)) + '分_#' + str(num))
spotify.user_playlist_add_tracks(username, playlist_url,just_list)
