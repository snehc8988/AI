#date created 2/6/2023 10:46pm
#voice-controlled AI assistant using python.
from datetime import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha

#speech engine initialisation
engine = pyttsx3.init()
voices =  engine.getProperty("voices")
engine.setProperty("voices", voices[1].id) #0 = male, 1 = female
activationWord = "mina"

#config browser
#set the path
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome_path))

appId = "6GVXXH-LKVLV74V53"
wolframClient = wolframalpha.Client(appId)
def speak(text, voice_id='female', rate=120):
    voices = engine.getProperty('voices')
    if voice_id == 'male':
        engine.setProperty('voice', voices[0].id)
    elif voice_id == 'female':
        engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()
def parseCommand(max_tries=3):
    r = sr.Recognizer()
    tries = 0
    while tries < max_tries:
        with sr.Microphone() as source:
            print("Listening for a command....")
            audio =  r.listen(source)
        try:
            print("Recognizing Speech....")
            query = r.recognize_google(audio, language="en_gb")
            print(f"you said: {query}")
            return query
        except Exception as exception:
            print("Could not understand audio")
            speak("Could not understand audio")
            print(exception)
            tries += 1
    speak("Sorry, I was unable to understand your command.")
    return ""

def search_wikipedia(query):
    try:
        search_results = wikipedia.search(query)
        if not search_results:
            print("No Wikipedia results found.")
            return ""
        
        page = wikipedia.page(search_results[0])
        title = page.title
        summary = page.summary
        url = page.url
        
        result = f"Title: {title}\nSummary: {summary}\nURL: {url}"
        return result
    
    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options[:5]
        print("Disambiguation Error. Possible options:")
        for i, option in enumerate(options):
            print(f"{i+1}. {option}")
        return ""
    
    except wikipedia.exceptions.PageError:
        print("Page not found.")
        return ""
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

def listOrDict(var):
    if isinstance(var, list):
        if len(var) > 0 and "plaintext" in var[0]:
            return var[0]["plaintext"]
        else:
            raise ValueError("List argument does not contain a dictionary with a 'plaintext' key")
    elif isinstance(var, dict):
        if "plaintext" in var:
            return var["plaintext"]
        else:
            raise ValueError("Dictionary argument does not contain a 'plaintext' key")
    else:
        raise TypeError("Argument is not a list or dictionary")
def search_wolframalpha(query=""):
    response = wolframClient.query(query)

    if response["@success"] == "false":
        print("Computation failed. Trying Wikipedia search...")
        return search_wikipedia(query)

    pod0 = response["pod"][0]
    pod1 = response["pod"][1]

    if (("result") in pod1["@title"].lower()) or (pod1.get("@primary", "false") == "true") or ("definition" in pod1["@title"].lower()):
        result = listOrDict(pod1["subpod"])
        return result.split("(")[0]

    else:
        question = listOrDict(pod0["subpod"])
        print("Could not find a direct result. Searching Wikipedia for more information...")
        return search_wikipedia(question)
if __name__ == "__main__":
    speak("All systems nominal.")
    while True:
        try:
            #parse
            query = parseCommand().lower().split()
            if query[0] == activationWord:
                #query.pop(0)
                #listen command
                if query[1] == "say":
                    if "hello" in query:
                        speak("Hello, my love")
                    else:
                        query.pop(0)
                        speech = " ".join(query)
                        speak(speech)
                # Navigation
                if query[1] == "go" and query[2] == "to":
                    speak("Opening....")
                    query = " ".join(query[3:])
                    webbrowser.get("chrome").open_new(query)
                #wiki
                if query[1] == "wikipedia":
                    query = " ".join(query[1:])
                    speak("Querying the universal databank.")
                    result = search_wikipedia(query)
                    if result:
                        speak(result)
                    else:
                        speak("No result found.")

                # wolframe alpha
                if query[0] == "compute" or query[0] == "computer":
                    query = " ".join(query[1:])
                    speak("Computing...")
                    try:
                        result = search_wolframalpha(query)
                        if result:
                            speak(result)
                        else:
                            speak("Unable to compute.")
                    except:
                        speak("Unable to compute.")
        except Exception as e:
            speak("An error occurred: " + str(e))
            continue