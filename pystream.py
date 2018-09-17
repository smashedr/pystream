import os
import sys
import requests
import tempfile

CONF = {
    'client_id': 'bsoi6ctwjmevgsovhtwhvsc31qg29o',
    'token_url': 'https://api.twitch.tv/api/channels/{}/access_token',
    'usher_url': 'http://usher.twitch.tv/api/channel/hls/{}.m3u8',
}


def open_twitch(channel):
    token_url = CONF['token_url'].format(channel)
    headers = {'Client-ID': CONF['client_id']}
    token_req = requests.get(token_url, headers=headers, timeout=10)
    j = token_req.json()
    usher_url = CONF['usher_url'].format(channel)
    data = {
        'player': 'twitchweb',
        'token': j['token'],
        'sig': j['sig'],
        'allow_audio_only': 'false',
        'allow_source': 'true',
        'type': 'any',
        'p': '1234',
    }
    usher_req = requests.get(usher_url, params=data)
    temp_file = tempfile.NamedTemporaryFile(
        suffix=os.path.splitext(CONF['usher_url'])[1], mode='w', delete=False
    )
    temp_file.write(usher_req.content.decode())
    temp_file.close()
    os.startfile(temp_file.name)


if __name__ == '__main__':
    try:
        if len(sys.argv) > 1:
            open_twitch(os.path.basename(sys.argv[1]))
        else:
            open_twitch(os.path.basename(input('Twitch username or URL: ')))
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
    except Exception as error:
        print('\nCaught Exception: {}'.format(error))
        input('\n\nYou may close this window or press <enter> to exit...\n')
        sys.exit(1)
