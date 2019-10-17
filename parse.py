from osrparse import parse_replay_file
import requests
import json
import math

def main():
    path = '- Mike Greene - Bill Nye the Science Guy Theme Song (Chinese Intro) [Easy] (2019-10-14) Osu.osr'

    parse = parse_replay_file(path)
    
    api_key = get_api_key()

    beatmap_data = call_beatmap_data(api_key, parse.beatmap_hash)

    HitObjectsData = get_hitobjects_data()

    osr_parse = parse_osr(play_data, HitObjectsData, beatmap_data)

    

def parse_osr(parse, HitObjectsData, beatmap_data):
    beatmap_circle_size = int(beatmap_data[0]["diff_size"])
    beatmap_od = int(beatmap_data[0]["diff_overall"])
    beatmap_ar = int(beatmap_data[0]["diff_approach"])

    mod_combination = parse.mod_combination
    play_data = parse.play_data
    
    time_ms = 0
    pointer = 0 #pointer for HitObjectsData
    key_down_prev = 0 #key_down is same format as obj.keys_pressed

    for obj in play_data:
        #temp break
        if time_ms > 1000:
            break

        if obj.keys_pressed != 0:
            if key_down_prev == 0:#if no keys were pressed previously
                #key_down_prev = obj.keys_pressed

                key_down_cur = obj.keys_pressed
                if coord_within_range(HitObjectsData[pointer][],#fix
                                      HitObjectsData[pointer][],#fix
                                      obj.x, obj.y,
                                      CircleSize):
                    cur_hit = determine_current_hit(time1,
                                                    time2,
                                                    beatmap_od,
                                                    mods)
                    
                
            else:
                #should only be relevant on sliders, where you have
                #to hold down the key constantly
                eof = ""
        
        print(str(obj.time_since_previous_action) + " " + str(obj.x)
              + " " + str(obj.y) + " " + str(obj.keys_pressed))

        time_ms += obj.time_since_previous_action

def get_hitobjects_data():
    #parsing .osu file
    #TODO: turn hitobjectdata into 2d array, each entry contains
    #      all information about current hitobject (type, sliderpoints etc...)
    #TODO: add support for sliderheads, sliderticks, sliderends etc...
    
    HitObjectsData = []
    with open('Mike Greene - Bill Nye the Science Guy Theme Song (Chinese Intro) (Monstrata) [Easy].osu') as file:
        for line in reversed(file.readlines()):
            if "[HitObjects]" in line:
                break
            else:
                HitObjectsData.append(line)
    HitObjectsData.reverse()
    return HitObjectsData

def determine_current_hit(time1, time2, beatmap_od, mods):
    #time1 is circle time
    #time2 is cursor keydown time
    
    time_difference = abs(time2 - time1)
    timing_range = od_to_ms_range(beatmap_od, beatmap_ar, mods)

    if time_difference <= timing_range[0]:
        return "300"
    elif time_difference <= timing_range[1]:
        return "100"
    elif time_difference <= timing_range[2]:
        return "50"
    else:#TODO: update this (note locking)
        return "miss"

def od_to_ms_range(beatmap_od, mods):
    #returns [300 ms range, 100 ms range, 50 ms range]
    #TODO: support for DT, HT, EZ

    if mods == "NM":
        return [79 - (beatmap_od * 6) + 0.5,
                139 - (beatmap_od * 8) + 0.5,
                199 - (beatmap_od * 10) + 0.5]
    
    
def coord_within_range(x1, y1, x2, y2, CircleSize):
    #x1 y1 is circle coord
    #x2 y2 is cursor keydown coord
    
    PlayfieldWidth = 512
    CircleRadius = (PlayfieldWidth / 16) * (1 - (0.7 * (CircleSize - 5) / 5))

    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2) <= CircleRadius

def get_api_key():
    #retrieves your API key from api_key.txt
    #TODO: change this from dictionary to simple string
    with open('api_key.txt') as json_file:
        return json.load(json_file)["api_key"]

def call_beatmap_data(api_key, beatmap_hash):
    #getting beatmap data from osu api
    
    link = f'https://osu.ppy.sh/api/get_beatmaps?k={api_key}&h={beatmap_hash}'
    print(link)
    response = requests.get(link)
    if response.status_code != 200:
        raise Exception('API response: {}'.format(response.status_code))
    return json.loads(response.content)

if __name__ == '__main__':
    main()
