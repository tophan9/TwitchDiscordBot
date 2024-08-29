import requests
from secret import client_secret, client_id

class Stream:

    def __init__(self, title, streamer, game):
        self.title = title
        self.streamer = streamer
        self.game = game


def getOAuthToken():
    body = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }

    try:
        response = requests.post('https://id.twitch.tv/oauth2/token', data=body)
        response.raise_for_status()  # Raise an exception for any HTTP error
        token_data = response.json()
        return token_data.get('access_token')
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def checkIfLive(channel):
    url = f"https://api.twitch.tv/helix/streams?user_login={channel}"
    token = getOAuthToken()

    HEADERS = {
        'Client-ID': client_id,
        'Authorization': 'Bearer ' + token
    }

    try: 

        req = requests.get(url, headers=HEADERS)

        res = req.json()

        if 'data' in res and len(res['data']) > 0:
            data = res['data'][0]
            title = data['title']
            streamer = data['user_name']
            game = data['game_name']
            thumbnail_url = data['thumbnail_url']
            stream = Stream(title, streamer, game, thumbnail_url)
            return stream
        else:
            return "OFFLINE"
    except Exception as e:
        return "An error occured:" + str(e)