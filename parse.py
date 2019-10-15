from osrparse import parse_replay_file
import requests
import json

def call_beatmap_data(api_key, beatmap_hash):
    response = requests.get(f'https://osu.ppy.sh/api/get_beatmaps?k={api_key}&h={beatmap_hash}')
    if response.status_code != 200:
        raise Exception('API response: {}'.format(response.status_code))
    return json.loads(response.content)

def main():
    path = '- Mike Greene - Bill Nye the Science Guy Theme Song (Chinese Intro) [Easy] (2019-10-14) Osu.osr'
    parse = parse_replay_file(path)
    play_data = parse.play_data
    
    api_key = ''
    with open('api_key.gitignore') as json_file:
        api_key = json.load(json_file)["api_key"]
    
    CircleSize = int(call_beatmap_data(api_key, parse.beatmap_hash)[0]["diff_size"])
    PlayfieldWidth = 512
    CircleRadius = (PlayfieldWidth / 16) * (1 - (0.7 * (CircleSize - 5) / 5))
    
    print(CircleRadius)

    time = 0
    """

    for obj in play_data:
    #print(str(obj.time_since_previous_action) + " " + str(obj.x)
          #+ " " + str(obj.y) + " " + str(obj.key_pressed))

        if obj.keys_pressed == 5:
            print(time)
            break
    
        time += obj.time_since_previous_action
    """

if __name__ == '__main__':
    main()
