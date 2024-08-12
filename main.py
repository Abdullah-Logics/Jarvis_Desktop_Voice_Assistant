import webbrowser
import speech_recognition as sr
import pyttsx3
import time
import google.generativeai as genai
import wikipedia
import re
import os

def get_download_path():
    """Return the default download path for the current user."""
    if os.name == 'nt':  # For Windows
        download_path = os.path.join(os.environ['USERPROFILE'], 'Downloads')
    else:  # For macOS/Linux
        download_path = os.path.join(os.environ['HOME'], 'Downloads')
    
    return download_path
# Enter your API Key
api_key = "API Key"

History = "" #This is the empty history this stores the data when the progress goes on

# Removing Emojis from the Gemini Text
def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"  # Dingbats
        u"\U000024C2-\U0001F251" 
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub(r"", text)

# Taking responses from Gemini for special purposes
def gemini(prompt):
    genai.configure(api_key=f"{api_key}")
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 201010,
        "response_mime_type": "text/plain",
    }
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(history=[])
    try:
        response = chat_session.send_message(prompt)
        reply = response.text
        reply = reply.replace("*", "")
        reply = reply.replace("#", "")
        print(reply)
        say("Do You want me to say This Information?")
        yes_no = take_command()
        if "No".lower() in yes_no.lower():
            reply = reply
        else:
            say(reply)
        say("Do you want me to save this text into file.")
        print("Do you want me to save this text into file?")
        yes_no = take_command()
        if "N0".lower() in yes_no.lower():
            return 0
        else:
            p = get_download_path()
            path = p + f"/{prompt[:30]}"
            with open(path, "w") as f:
                f.write(f"Prompt:- {prompt}\nGemini:-\n{reply}")
                return 0
    except:
        print("An error has occurred....\nPlease Try Again...")
        say("An error has occurred. Please Try Again")

# Chat Mode code with Gemini that we did
def chat(title):
    print(f"Chat Begins with title {title}....")
    say(f"Chat Begins with title {title}")
    while True:
        prompt = take_command()
        if "Exit Chat".lower() in prompt.lower():
            print("Chat mode is off now...")
            say("Chat mode is off now!")
            return 0
        print(prompt)
        with open(f"C:/Users/abdul/Downloads/{title}.txt","r+") as fp:
            history = fp.read()
            fp.write(prompt + "\n")
            fp.close()
        prompt = ('I am Abdullah Bin Usman And I want a chat with you. your responses will be as instructed in prompts '
                  'dont be so long except for some generative things. Responses will be like someone is chatting dont '
                  'begin with greeting or anything else.'
                  'Also Response according to the context given to you'
                  f'you are not Gemini while chat. You will be Jarvis. This is the context of chat: {history}.Prompt is {prompt}')
        genai.configure(api_key=f"{api_key}")
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 201010,
            "response_mime_type": "text/plain",
        }
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config = generation_config,
        )
        chat_session = model.start_chat(history=[])
        try:
            response = chat_session.send_message(prompt)
            reply = response.text
            reply = reply.replace("*", "")
            reply = reply.replace("#", "")
            print(reply)
            reply = remove_emojis(reply)
            say(reply)
            p = get_download_path()
            with open(p + f"/{title}.txt","a") as fp:
                fp.write(""
                         "\n"+reply+"\n")
                fp.close()
        except:
            print("An error has occurred....\nPlease Try Again...")
            say("An error has occurred. Please Try Again")

# Normal Everyday Response
def gemini_simple(prompt,history,mode):
    genai.configure(api_key=f"{api_key}")
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 200,
        "response_mime_type": "text/plain",
    }
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(history=[])
    try:
        response = chat_session.send_message(prompt)
        reply = response.text
        reply = reply.replace("*", "")
        reply = reply.replace("#", "")
        print(reply)
        reply = remove_emojis(reply)
        say(reply)
        if mode == "1":
            return history + f'Rely:- {reply}\n'
    except:
        print("An error has occurred....\nPlease Try Again...")
        say("An error has occurred. Please Try Again")

# Change text into speech
def say(prompt):

    engine = pyttsx3.init() # This will create an engine for text to speech

    # Change the voice speed rate in units words per min
    engine.getProperty("rate")
    engine.setProperty("rate", 130)

    # Actually making the speech
    engine.say(prompt)
    engine.runAndWait()  # Wait until the speech finishes


# Search summaries from Wikipedia
def wikipedia_search(query):

    result = wikipedia.summary(query)
    print(result)

    say("Do you want me to say this information?")
    ans = take_command()

    if "Yes".lower() in ans.lower():
        say(result)

    elif "No".lower() in ans.lower():
        return 0

# Take the voice command from your microphone
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listning...\n")
        r.pause_threshold = 1
        audio = r.listen(source)
        # Sometime this fucntion may not recognize the voice therefore we write this part in try except cycle
        try:
            query = r.recognize_google(audio, language="en-us")
            return query
        except Exception as e:
            print(e)
            print("Say that again please...")
            return "None"

# A fun feature of making Jarvis Repeat what ever you say
def repeat_function():
    say("I will Repeat Your words!...")
    while True:
        prompt = take_command()
        if "Stop".lower() in prompt.lower():
            print("Repeat Mode is Stopped!...")
            say("Repeat Mode is Stopped!")
            break
        print(prompt, "...")
        say(prompt)


# Beginning of the Program By Greeting

say(str(gemini_simple("Its the start of the conversation and you have to greet me Abdullah Bin Usman like any voice assistant and your name is Jarvis",History,"0")).replace("None",""))
text_to_speech = 1

while True:
    prompt = take_command()

    if text_to_speech == 1:
        print(prompt)

    # Exit to the program
    if "bye".lower() in prompt.lower():
        bye = str(gemini_simple("Say good bye to your user (Abdullah Bin Usman) as a voice assistant Jarvis. Just good bye or Take care like stuff",History,"0")).replace("None","")
        print(bye,"...")
        say(bye)
        break

    if "Jarvis".lower() in prompt.lower():
        prompt = prompt.lower()
        index = prompt.index("jarvis") + 7
        prompt = prompt[index:]
        try:
            # Open Websites
            if "Open".lower() in prompt.lower():
                index = prompt.index("open") + 5
                site1 = prompt[index:]
                site = site1.replace(" ", "")
                print(f"Opening {site1} ...")
                say(f"Opening {site1} ...")
                webbrowser.open(f"https://{site}.com")

            #     Open Text on Screen
            elif "Show Text".lower() in prompt:
                text_to_speech = 1
                print("Text Mode is on...")
                say("Text Mode is on.")
            elif "Disappear Text".lower() in prompt:
                text_to_speech = 0
                print("Text Mode is off...")
                say("Text Mode is off.")

            #     Search Things on YouTube
            elif "Search on Youtube".lower() in prompt:
                prompt = prompt.lower()
                index = prompt.index("youtube") + 8
                site = prompt[index:]
                path = f"https://www.youtube.com/results?search_query={site}"
                webbrowser.open(path)
                print(f"Searching {site} on Youtube...")
                say(f"Searching {site} on Youtube.")

            #     Search on Web
            elif "Search".lower() in prompt.lower() and not ("on Wikipedia".lower() in prompt.lower()):
                index = prompt.index("search") + 7
                site = prompt[index:]
                print(f"Searching {site} ...")
                say(f"Searching {site} ...")
                webbrowser.open(f"https://www.google.com/search?q={site}")

            #     Tell The Time
            elif "Time".lower() in prompt.lower():
                if int(time.strftime("%H")) < 12:
                    state = "AM"
                else:
                    state = "PM"
                print("Its ", int(time.strftime('%H')) % 12, ":", time.strftime('%M'), state)
                say("Its " + str(int(time.strftime('%H')) % 12) + " " + time.strftime('%M') + state)

            #     Repeat Mode
            elif "Repeat with me".lower() in prompt.lower() or "Repeat my Words".lower() in prompt.lower():
                repeat_function()

            # Search on Wikipedia

            elif "Search on wikipedia".lower() in prompt.lower():
                prompt = prompt.lower()
                index = prompt.index("wikipedia") + 10
                query = prompt[index:]
                print(f"Searching {query} on Wikipedia...")
                if query.index("About".lower()) == 0:
                    query = query[5:]
                say(f"Searching {query} on Wikipedia")
                wikipedia_search(query)

            #     Chat Mode
            elif "Chat".lower() in prompt.lower():
                print("Chat mode is on....")
                say("Chat Mode is on. Before starting just give it a title.")
                title = take_command()
                p = get_download_path()
                with open(p + f"/{title}.txt","w") as fp:
                    fp.write("Title: " + title + "\n")
                chat(title)

            #     Clear the Conversation History
            elif "Clear History".lower() in prompt.lower():
                History = ""
                print("Your His tory is Cleared...")
                say("Your His tory is Cleared")

            #     Special Things you want to generate from Gemini
            elif "Ask Gemini".lower() in prompt.lower():
                prompt = prompt.lower()
                index = prompt.index("gemini") + 7
                query = prompt[index:]
                print(f"Asking Gemini {query}....")
                say(f"Asking Gemini {query}")
                gemini(query)

            #     Normal Conversation
            else:
               History = History + prompt
               History = gemini_simple("Answer this query in max two line or 200 words like a voice assistant. You are a voice "
                              "assistant and the person giving you the instruction is Abdullah Bin Usman. Your name is "
                              f"Jarvis. Dont make him Feel like you are Gemini and dont greet at the beginning dont repeat my name unnecessary. Your prompt is\"{prompt}\" I am providing you the context. use it and answer my query. The context is: \"{History}\"",History,"1")
        except:
            print("Error...")
