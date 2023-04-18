import datetime                    #using it to load the current date and time
import sys                   
import pyttsx3                    #using it to convert text to speech
import wikipedia                  #using it to search a wikipedia
import speech_recognition as sr   #using it to recognize speech and convert it to text
import pywhatkit           #using it as the interface between internet and user and opening specific web pages
import os                         #using it to manipulate with the functionality of installed operating system on our system
import random                     #using it to generate random values
import subprocess                 #using it to open and terminate applications as subprocesses
import pandas as pd               #using it to load csv and excel files and fetch values from the readable database
import smtplib                    #using it to send mails with smtp
import pyjokes                    #using it to taking one line joke or jokes to make conversations more fun and comfort '''
import tkinter as tk 
from tkinter import *            #using this to make graphical user interface
import threading                 #using this to make GUi window responsable while working with infinte loop

#creating dictionary for matching condition and run commands accordingly
condition_dictionary={
    "searching_list":["wikipedia","who is","what is","search on google"],
    "time":["time","times"],
    "stop_list":["exit","quit","off","shut down","stop"," wait"],
    "open_and_close":["chrome","google","yahoo","youtube","you tube",
    "geeks for geeks","mail","microsoft edge","notepad","vlc","code","command"],
    "basic_conversation":["say hi to","hello ","say hi to me",  "se hi to",
    " say hello to","how are you","joke"],
    "play_music": ["play "],
    "send_something":["send mail to","send message to","send a mail to","send a message to"]
    }

#initializing engine for python speech to text version 3 module
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice",voices[0].id)

##importing csv to use in email sending and whatsapp messages
dataset_mail=pd.read_csv("emails.csv")
dataset_message=pd.read_csv("emails.csv") 

def run_button():
    '''
     using this function to trigger from the 
    run button and run the system

    return :
    None
    '''
    threading.Thread(target=pre_start_wish).start()
def exit_button():
    ''' using this function to deploy the
    system window

    return:
    None
    '''
    main_win.destroy()
def gui_window():
    ''' using this function to build 
    GUI window to interact with the system

    return:
    None
    '''
    #initializing a graphical user interface and widgets 
    global main_win
    main_win = tk.Tk()
    main_win.resizable(FALSE,FALSE)
    main_win.geometry("800x636+490+210")
    main_win.title("System window")
    
    #Define background window
    background = PhotoImage(file = 'chat-bot.png')
    #creating a canvas
    canvas = Canvas(main_win, width = 80, height = 63)
    canvas.pack(fill = "both", expand = True)

    #set background image
    canvas.create_image(0,0,image=background,anchor="nw")
    global print_on_window

    #initialize label
    print_on_window= tk.Label(canvas,text="Hii\nI'm your virtual assistant\nPress run button to start",font=("Terminal",16,),fg="White",bg="#04acf4")
    print_on_window.pack(padx=30,pady=50,anchor="ne",side=RIGHT)

    frame = tk.Frame(canvas,bg="white",width=300,height=150)
    frame.pack(side=LEFT,anchor="sw")
    
    #initializing buttons
    run_btn = tk.Button(frame,text="Run",command=run_button,font=("Times New Roman",18),bd=5,width=10,height=1,bg="#04acf4",fg="white",cursor="hand2",relief=RAISED)
    run_btn.pack(side=RIGHT,anchor="se")

    exit_btn = tk.Button(frame,text="Exit",command=exit_button,font=("Times New Roman",18),bd=5,width=10,height=1,bg="white",fg="#04acf4",cursor="hand2",relief=RAISED)
    exit_btn.pack(side=RIGHT,anchor="se",)
    
    #window main loop
    main_win.mainloop()

#defining functions
def process_mail():
    """
    using this function to perform online mailing process

    return:
    None
    """
    result= dataset_mail["Name"].where(dataset_mail["Name"]==receiver)
    index=0
    for i in result:
        if i!=receiver:
            index=index+1
        else:
            break
    try:
        to=(dataset_mail.loc[index,"Email"])
        say_text("what should i say")
        content= take_command()
        content= content.replace("say","")
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.ehlo()
        server.starttls()
        server.login("varinderkalyan1@gmail.com","Password-here")
        server.sendmail("varinderkalyan1@gmail.com",to,content)
        server.close()
        say_text("email has been sent successfully")
        print_on_window.config(text="email has been\n sent successfully")
    except Exception as error:
        print(str(error))
        say_text(f"sorry. unable to sent mail to {receiver}")
def process_message():
    """
    using this function to perform online whatsapp message process

    return:
    None
    """
    try:
        result= dataset_message["Name"].where(dataset_message["Name"]==receiver_name)
        index=0
        for i in result:
            if i!=receiver_name:
                index=index+1
            else:
                break
        receiver_num=(dataset_message.loc[index,"Mobile Phone"])
        receiver_num = int(receiver_num)
        receiver_num= str(receiver_num)
        if "+91" not in receiver_num:
            receiver_num= "+91"+receiver_num
        say_text("what should i say")
        content = take_command()
        content = content.replace("say","")
        hour =int(datetime.datetime.now().hour)
        minute =int(datetime.datetime.now().minute)
        minute = minute+1
        pywhatkit.sendwhatmsg(receiver_num,content,hour,minute)
        print_on_window.config(text="sent successfully")
        say_text("message sent successfully")
    except Exception as error:
        print(str(error))
        say_text(f"sorry unable to send message to {receiver_name}")
def on_and_wait():
    ''' 
    using this function to make ai on wait while the 
    some other time-taking process is on working like
    music playing in the backgroung so that the music voice will 
    not cause a interruption between command fetching process
    return:
    None
    '''
    query=waitcommand()
    if query=="system":
        say_text("please say the command")
        init_system()
    else:
        on_and_wait()
def waitcommand():
    '''
    using this function to take a starting command
    while our ai is on wait mode
    return:
    query
    '''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print_on_window.config(text="waiting..")
        r.pause_threshold = 1
        audio  = r.listen(source)
    try :
        print_on_window.config(text="recognizing...")
        query = r.recognize_google(audio,language="en-in")
        print_on_window.config(text=f"user said :{query}")
    except Exception as e:
        return "None"
    return query
def say_text(audio):
    """
    functionality of this function is to taking a text and 
    convert it into speech using python text to speech module
    return:
    text to audio
    """
    engine.say(audio)
    engine.runAndWait()
def pre_start_wish():
    """
    this function is used to take a time as output from
    dateandtime python module and wish accordingly
    return:
    time
    """
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour <12:
        print_on_window.config(text="Good Morning, Sir")
        say_text("good morning sir")
    elif hour>=12 and hour <18:
        print_on_window.config(text="Good afternoon, Sir")
        say_text("good afternoon sir")
    else:
        print_on_window.config(text="Good evening, Sir")
        say_text("good evening sir")
    print_on_window.config(text="system is all set")
    say_text("system is all set")
    print_on_window.config(text="Please say the command")
    say_text("Please say the command")
    init_system()
def take_command():
    """
    it takes speech input from user using microphone and then convert it into
    text using google api for speech recognition
    return:
    converted text from user speech
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print_on_window.config(text="listening...")
        r.pause_threshold = 1
        audio  = r.listen(source)
    try :
        print_on_window.config(text="recognizing...")
        query = r.recognize_google(audio,language="en-in")
        print_on_window.config(text=f"User said :{query}")
    except Exception as e:
        say_text("say that again please")
        return "None"
    return query   
def init_system():
    """
    using this function to call all the AI related functions.
    and defining various set of conditions to performing AI
    
    return:
    loop of listening and performing actions
    """
    while True:
        query = take_command().lower() 
        query = query.replace("system","")
        for i in condition_dictionary["searching_list"]:
            index=condition_dictionary["searching_list"].index(i)
            if i in query:
                say_text("searching wikipedia...")
                query = query.replace(i,"")
                print_on_window.config(text=f"wikipedia of {query}")
                results = wikipedia.summary(query,sentences=1)
                say_text("according to wikipedia")
                say_text(results)
                break
            elif query.endswith("on google") and index==3:
                query = query.replace("search","")
                query = query.replace("on google","")
                query = query.strip()
                say_text(f"searching {query} on google...")
                pywhatkit.search(query)
                break
            else:
                continue
        for i in condition_dictionary["time"]:
            if i in query:
                time = datetime.datetime.now().strftime("%I:%M %p")
                say_text(f"current time is {time}")
                break
            else:
                continue
        for i in condition_dictionary["stop_list"]:
            index= condition_dictionary["stop_list"].index(i)
            if i in query and index!=5:
                say_text("system"+i)
                main_win.destroy()
                sys.exit("stopped")
                
            elif i in query and index==5:
                say_text("ok  i'm waiting")
                on_and_wait()
            else:
                continue
        for i in condition_dictionary["open_and_close"]:
            index=condition_dictionary["open_and_close"].index(i)
            if i in query and index==0:
                if "open" in query:
                    chrome=subprocess.Popen("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
                    say_text("chrome opened")
                    break
                elif "close" in query:
                    chrome.terminate()
                    say_text("chrome closed")
                    break
                else:
                    continue
            elif i in query and index==1:
                if "open" in query:
                    google= subprocess.Popen(["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe","www.google.com"])
                    say_text("google opened")
                    print_on_window.config(text="what should i search")
                    say_text("what should i search on google")
                    search = take_command()
                    search=search.replace("search","")
                    search=search.replace("on google","")
                    search=search.strip()
                    say_text(f"searching {search} on google")
                    #pywhatkit.search(search)
                    break
                elif "close" in query:
                    google.terminate()
                    say_text("google closed")
                    break
                else:
                    continue
            elif i in query and index==2 :
                if "open" in query:
                    yahoo= subprocess.Popen(["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe","www.yahoo.com"])
                    say_text("yahoo opened")
                    break
                elif "close" in query:
                    yahoo.terminate()
                    say_text("yahoo closed")
                    break
                else:
                    continue
            elif i in query and index==3:
                if "open" in query:
                    youtube= subprocess.Popen(["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe","www.youtube.com"])
                    say_text("youtube opened")
                    break
                elif "close" in query:
                    youtube.terminate()
                    say_text("youtube closed")
                    break
                else:
                    continue
            elif i in query and index==4:
                if "open" in query:
                    you_tube= subprocess.Popen(["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe","www.youtube.com"])
                    say_text("youtube opened")
                    break
                elif "close" in query:
                    you_tube.terminate()
                    say_text("youtube closed")
                    break
                else:
                    continue
            elif i in query and index==5 :
                if "open" in query:
                    geeksforgeeks= subprocess.Popen(["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe","www.geeksforgeeks.org"])
                    say_text("geeks for geeks opened")
                    break
                elif "close" in query:
                    geeksforgeeks.terminate()
                    say_text("geeksforgeeks closed")
                    break
                else:
                    continue
            elif i in query and index==6:
                if "open" in query:
                    mail= subprocess.Popen(["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe","mail.google.com/mail/u/0/#inbox"])
                    say_text("mail opened")
                    break
                elif "close" in query:
                    mail.terminate()
                    say_text("mail closed")
                    break
                else:
                    continue
            elif i in query and index==7:
                if "open"  in query:
                    edge=subprocess.Popen("C:\\Program Files (x86)\\Microsoft\Edge\\Application\\msedge.exe")
                    say_text("microsoft edge opened")
                    break
                elif "close" in query:
                    edge.terminate()
                    say_text("microsoft edge closed")
                    break
                else:
                    continue
            elif i in query and index==8:
                if "open" in query:
                    notepad=subprocess.Popen("C:\\Windows\\system32\\notepad.exe")
                    say_text("notepad opened")
                    break
                elif "close" in query:
                    notepad.terminate()
                    say_text("notepad closed")
                    break
                else:
                    continue
            elif i in query and index==9:
                if "open" in query:
                    vlc=subprocess.Popen("C:\\Program Files\\VideoLAN\\VLC\\vlc.exe")
                    say_text("video app opened")
                    break
                elif "close" in query:
                    vlc.terminate()
                    say_text(" video app closed")
                    break
                else:
                    continue
            elif i in query and index==10:
                if "open" in query:
                    vs_code=subprocess.Popen("C:\\Users\\varinder\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")
                    say_text("visual studio code opened")
                    break
                elif "close" in query:
                    vs_code.terminate()
                    say_text(" visual studio code closed")
                    break
                else:
                    continue
            elif i in query and index==11:
                if "open" in query:
                    command=subprocess.Popen("C:\\Windows\\system32\\cmd.exe")
                    say_text("command prompt opened")
                    break
                elif "close" in query:
                    command.terminate()
                    say_text("command prompt closed")
                    break
                else:
                    continue
            else:
                continue
        for i in condition_dictionary["basic_conversation"]:
            index = condition_dictionary["basic_conversation"].index(i)
            if i in query and index==0 and query.endswith("me")==False:
                query = query.replace(i,"")
                say_text("hello"+query)
                break
            elif i in query and index==1 and query.startswith("hello")==True:
                say_text("hello sir")
                say_text("great to hear you")
                break
            elif i in query and index==2 and query.endswith("me")==True:
                say_text("hello mr. kalyan")
                say_text("greate to hear you")
                break
            elif i in query and index==3 and query.endswith("me")==False:
                query = query.replace(i,"")
                say_text("hello"+query)
                break
            elif i in query and index==4 and query.endswith("me")==False:
                query = query.replace(i,"")
                say_text("hello"+query)
                break
            elif i in query and index==5:
                say_text("I'm busy with lot's of comparison and operations")
                break
            elif i in query and index==6:
                joke = pyjokes.get_joke(language="en",category="neutral")
                say_text("ok listen")
                say_text(joke)
            else:
                continue
        for i in condition_dictionary["play_music"]:
            index=condition_dictionary["play_music"].index(i)
            if query.endswith("music") == True or  query.endswith("songs") == True or query.endswith("song")==True: 
                music_dir= "C:\\Program Files (x86)\\Windows Media Player\\songs"
                songs= os.listdir(music_dir)
                random_song = random.randint(0,len(songs)-1)
                music=os.startfile(os.path.join(music_dir,songs[random_song]))
                on_and_wait()
            elif i in query and index==0:
                song=query.replace("play","")
                say_text("playing"+song)
                pywhatkit.playonyt(song)
                on_and_wait()
            else:
                continue  
        for i in condition_dictionary["send_something"]:
            index=condition_dictionary["send_something"].index(i)
            global receiver
            global receiver_name
            if i in query and index==0:
                query=query.replace(i,"")
                query= query.strip()
                receiver = query.upper()
                process_mail()
            elif i in query and index==1:
                query = query.replace(i,"")
                query = query.strip()
                receiver_name = query;
                process_message()
            elif i in query and index==2:
                query=query.replace(i,"")
                query= query.strip()
                receiver = query.upper()
                process_mail()
            elif i in query and index==3:
                query = query.replace(i,"")
                query = query.strip()
                receiver_name = query
                process_message()
            else:
                continue
if __name__=="__main__":    
    gui_window()
