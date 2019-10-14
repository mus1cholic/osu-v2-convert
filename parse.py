from osrparse import parse_replay_file

path = '- Mike Greene - Bill Nye the Science Guy Theme Song (Chinese Intro) [Easy] (2019-10-14) Osu.osr'
parse = parse_replay_file(path)
play_data = parse.play_data

time = 0

for obj in play_data:
    #print(str(obj.time_since_previous_action) + " " + str(obj.x)
          #+ " " + str(obj.y) + " " + str(obj.keys_pressed))

    if obj.keys_pressed == 5:
        print(time)
        break
    
    time += obj.time_since_previous_action

#print(parse)
