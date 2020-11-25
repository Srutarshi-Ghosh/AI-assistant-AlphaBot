import os
import subprocess

app_data = {
            "vlc": ['cd C:\Program Files (x86)\VideoLAN\VLC', 'start vlc.exe'],
            ("google chrome", "chrome"): ['cd C:\Program Files (x86)\Google\Chrome\Application', 'start chrome'],
            "calculator": ['calc'],
            "command prompt": ['cmd'],
            "notepad": ['note'],
            ("vs code", "v s code", "code"): ['cd C:\\Users\Srutarshi Ghosh\AppData\Local\Programs\Microsoft VS Code', 'start code'],
            ("gmail", "mail", "email"): ['cd C:\\Users\Srutarshi Ghosh',
                           'explorer.exe shell:appsFolder\microsoft.windowscommunicationsapps_8wekyb3d8bbwe!microsoft.windowslive.mail'],
            "calendar": ['cd C:\\Users\Srutarshi Ghosh',
                           'explorer.exe shell:appsFolder\microsoft.windowscommunicationsapps_8wekyb3d8bbwe!microsoft.windowslive.calendar'],
            ("edge", "microsoft edge"): ['cd C:\\Users\Srutarshi Ghosh',
                                         'explorer.exe shell:appsFolder\Microsoft.MicrosoftEdge_8wekyb3d8bbwe!MicrosoftEdge'],
            ("c", "c plus plus"): ['cd C:\Program Files (x86)\Dev-Cpp', 'start devcpp']
            }

SONG_FILE = "C:\Users\Srutarshi Ghosh\PycharmProjects\Advanced\Songs"

def open_app(app):

    try:
        for file in app_data:
            if type(file) == tuple:
                for name in file:
                    if name == app:
                        [subprocess.Popen(i, shell=True) for i in app_data[file]]
                        return "App Opened Successfully"

            else:
                if file == app:
                    [subprocess.Popen(i, shell=True) for i in app_data[file]]
                    return "App Opened Successfully"


        os.system(app)
        subprocess.Popen(app)
        return "App Opened Successfully"
    except Exception as e:
        print(e)
        return "App Could not be opened"

#subprocess.call('explorer.exe shell:appsFolder\microsoft.windowscommunicationsapps_8wekyb3d8bbwe!microsoft.windowslive.calendar', shell=True)
#print(open_app("edge"))
#open_app("vlc")

os.chdir(SONG_FILE)
realnames = []
list_of_songs = []


def isword(word):

    for c in word:
        if c.isalpha():
            return True

    return False


def test_name(request):
    cont = request.split()
    song = ""
    curr_match = 0
    for song_name in realnames:
        match = 0
        for s in cont:
            if s in song_name.lower():
                match += 1
        print(match)

        if (song == "" and match >= len(cont)//2) or match >= curr_match:
            song = song_name
            curr_match = match

    return song


def parse_song_names():
    for file in os.listdir(SONG_FILE):
        if file.endswith('.mp3') or file.endswith('.mp4'):
            temp = file.split('-')[-1].strip()[:-4].split('(')
            name = temp[0].split()

            for i in range(len(name)):
                if '_' in name[i]:
                    name[i] = name[i].replace('_', ' ')

                if not isword(name[i]):
                    name.remove(name[i])

            realnames.append(' '.join(name))
            list_of_songs.append(file)

    #(list_of_songs)
    #print(*realnames)


def parse_song_req(text):
    cont = text.split()[1:]
    if 'by' in cont:
        ind = cont.index('by')
        song = ' '.join(cont[:ind])
    else:
        song = ' '.join(cont)

    x = song_open(song)
    if x:
        return ""
    else:
        return "Song not found"



def song_open(song):
    try:
        song = test_name(song)
        print(song)
        for song_name in realnames:
            if song != "" and song == song_name:
                ind = realnames.index(song_name)
                print(list_of_songs[ind])
                s = 'start wmplayer ' + '"' + SONG_FILE + "\\" + list_of_songs[ind] + '"'
                print(s)
                subprocess.call(s, shell=True)
                return True

        return False
    except:
        return False

parse_song_names()
#print(test_name("everything"))
#parse_song_req("play evrything")
#print(song_open("awakening"))
#subprocess.call('start wmplayer "C:\\Users\Srutarshi Ghosh\Desktop\Songs\Everything.mp3"', shell=True)

if __name__ == '__main__':
    print(open_app("mail"))
'''
def write_names():

    tag = eyed3.Tag()
    with open("songnames.txt", 'w') as f:
        for file in os.listdir(SONG_FILE):
            if file.endswith('.mp3'):
                tag.link(file)
                title = eyed3.Tag().getTitle()
                print(title)

write_names()

'''

