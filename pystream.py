import os
import sys
import requests
import tempfile
import urllib.parse

os.environ['TWITCH_CLIENT_ID'] = 'bsoi6ctwjmevgsovhtwhvsc31qg29o'


def hls(channel):
    token_url = 'https://api.twitch.tv/api/channels/{}/access_token'.format(
        channel
    )
    headers = {'Client-ID': os.environ['TWITCH_CLIENT_ID']}
    r = requests.get(token_url, headers=headers, timeout=10)
    j = r.json()
    uri = 'http://usher.twitch.tv/api/channel/hls/{}.m3u8'.format(channel)
    data = {
        'player': 'twitchweb',
        'token': j['token'],
        'sig': j['sig'],
        'allow_audio_only': 'true',
        'allow_source': 'true',
        'type': 'any',
        'p': '1234',
    }
    params = urllib.parse.urlencode(data)
    r = requests.get('{}?{}'.format(uri, params))
    temp_file = tempfile.NamedTemporaryFile(suffix='.m3u8', mode='w', delete=False)
    temp_file.write(r.content.decode())
    temp_file.close()
    os.startfile(temp_file.name)


if __name__ == '__main__':
    try:
        if len(sys.argv) > 1:
            hls(sys.argv[1])
        else:
            hls(input('Twitch username: '))
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
    except Exception as error:
        print('\nCaught Exception: {}'.format(error))
        input('\n\nYou may close this window or <enter> to exit...')
        sys.exit(1)
