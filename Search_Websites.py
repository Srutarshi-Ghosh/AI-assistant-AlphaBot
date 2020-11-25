import wikipedia
import webbrowser as wb
from AI import speak, get_audio


PREPOSITIONS = ['for', 'in', 'to']
QUESTIONS = ["what", "how", "who"]

SEARCH_STRINGS = ["tell me something about", "search wikipedia", "search wiki"]
GOOGLE_SEARCH_STRINGS = ["search google", "search in google", "search in google for"]
YOUTUBE_SEARCH_STRINGS = ["search youtube", "search in youtube", "search video"]


def youtube_search(text):

    url = "https://www.youtube.com/results?search_query="
    if text == "":
        wb.get().open_new('https://www.youtube.com/')
    else:
        wb.get().open_new(url+text)


def wiki_search(text):
    choice = 0
    if text.strip() == "":
        return "Cannot process your request"
    ans = wikipedia.search(text)
    while True:
        try:
            if choice >= len(ans):
                return "Your Request is not present in wikipedia"
            x = wikipedia.summary(ans[choice], sentences=3)
            return x
        except:
            second_choice = wikipedia.search(ans[choice])
            if second_choice == ans:
                choice += 1


def google_search(text):
    wb.get().open_new("http://www.google.com/search?btnG=1&q=%s" % text)


def parse_search(text):
    text = text.lower()
    content = text.split()


    if 'google' in text:
        for i in GOOGLE_SEARCH_STRINGS:
            if text.startswith(i):
                text.replace(i, "")
                google_search(text)
                return ""

    if 'youtube' in text:
        if 'search' in content[:2]:
            if content[0] == 'search':
                try:
                    if ('youtube' in content[1] and content[2] in PREPOSITIONS) or (
                            'youtube' in content[2] and content[1] in PREPOSITIONS):
                        youtube_search(' '.join(content[3:]))
                    elif 'youtube' in content[-1] and content[-2] in PREPOSITIONS:
                        youtube_search(' '.join(content[1:-2]))
                    else:
                        content.remove('search')
                        content.remove('youtube')
                        youtube_search(' '.join(content))

                    return 1

                except:
                    print("Cannot understand your request")
                    return -1

            elif content[1] == 'search':
                try:
                    youtube_search(' '.join(content[1:]))
                    return 1

                except:
                    print("Cannot understand your request")
                    return -1

        elif 'search' in content[-2:]:
            try:
                if ('search' in content[-1] and 'youtube' in content[-2]) or (
                        'search' in content[-2] and 'youtube' in content[-1]):
                    youtube_search(' '.join(content[:-2]))
                return 1

            except:
                print("Cannot understand your request")
                return -1


    elif 'wikipedia' in text or 'wiki' in text:
        if 'wiki' in content:
            content[content.index('wiki')] = 'wikipedia'

        if 'search' in content[:2]:
            if content[0] == 'search':
                try:
                    if ('wikipedia' in content[1] and content[2] in PREPOSITIONS) or ('wikipedia' in content[2] and content[1] in PREPOSITIONS):
                        return wiki_search(' '.join(content[3:]))
                    elif 'wikipedia' in content[-1] and content[-2] in PREPOSITIONS:
                        return wiki_search(' '.join(content[1:-2]))
                    else:
                        content.remove('search')
                        content.remove('wikipedia')
                        return wiki_search(' '.join(content))

                except:
                    return "Cannot understand your request"


            elif content[1] == 'search':
                try:
                    return wiki_search(' '.join(content))

                except:
                    return "Cannot understand your request"


        elif 'search' in content[-2:]:
            try:
                if ('search' in content[-1] and 'wikipedia' in content[-2]) or ('search' in content[-2] and 'wikipedia' in content[-1]):
                    return wiki_search(' '.join(content[:-2]))

                else:
                    return "Nothing in Wikipedia"

            except:
                return "Cannot understand your request"


    if content[0] in QUESTIONS:
        try:
            ser = wiki_search(' '.join(content))
            if ser == None:
                google_search(text)
            else:
                return ser
            return ""
        except:
            google_search(text)
            return ""

    return None


#print(parse_search("search youtube python"))
#print(parse_search("who is the first president of America"))



if __name__ == "__main__":


    from googlesearch import search
    import urllib.request
    from bs4 import BeautifulSoup

    def google_scrape(url):
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")
        return soup.title.text

    query = 'who is the president of america?'
    for url in search(query, stop=5):
        a = google_scrape(url)
        print(a)
        print(url)
        print()


def manage_search(text):

    for ser in YOUTUBE_SEARCH_STRINGS:
        if ser in text:
            speak("What should I search in Youtube")
            req = get_audio()
            youtube_search(req)
            return 1

    for ser in SEARCH_STRINGS:
        if ser in text:
            text = text.replace(ser, "")
            try:
                ans = wiki_search(text)
                if ans != None:
                    speak(ans)
                    return 1
                else:
                    break
            except:
                google_search(text)

    if 'google' in text:
        for ser in GOOGLE_SEARCH_STRINGS:
            if text.startswith(ser):
                text = text.replace(ser, "")
                google_search(text)
                return 1

    for ques in QUESTIONS:
        if text.startswith(ques):
            google_search(text)
            return 1






