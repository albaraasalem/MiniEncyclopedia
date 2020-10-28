#importing required packages
import wikipedia
import tkinter
from tkinter import*
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation
from tkinter.font import Font
import io
import base64
import urllib
from io import BytesIO
from PIL import ImageTk, Image

#this program is a mini version of wikipedia. The user inputs whatever he or she
#wants to learn about and a window will pop up with the image an a brief description

#this function checks if an element has a period
def has_period(string):
    for i in string:
        if i == ".":
            return True


#this function will erase excess words after last word of the summary
def erase_words(lst):
    n = lst.split()
    count = 0
    for i in reversed(n):
        if(has_period(i) == True):
            break
        else:
            count +=1

    diff = len(n) - count
    n = n[:diff]
    #now the string ends with a period
    n = " ".join(n)
    return n

#We need to enter  a new line for every 30 words in this long string
def wrap_by_words(s,n):
    '''returns a string where \\n is inserted between every n words'''
    a = s.split()
    ret = ''
    for i in range(0, len(a), n ):
        ret += ' '.join(a[i:i+n]) + '\n'

    return ret

#In case the description is too long, we will shrink it to 300 words max
def cut_words(string):
    n = string.split()
    if len(n) > 300:
        diff = len(n) - 300
        n = n[:-diff]
        n = " ".join(n)
        return wrap_by_words(erase_words(n), 30)
    else:
        return wrap_by_words(string, 30)

#Gui
#creating a function that will upload the wiki
def wiki():
    noun = entry.get()

    #use what was inputted by the user and get the summary of that topic from wikipedia
    summary = wikipedia.summary(noun)

    description = cut_words(summary)

    root = tkinter.Toplevel(window)
    root.wm_geometry("10000x10000") #adjusting window  size
    root.title(("{} Wiki").format(noun.capitalize()))

    my_canvas = Canvas(root)
    my_canvas.pack(fill = BOTH, expand = 1)

    #adding title of the wiki search
    font1 = Font(family = "Times new roman", size = 20, underline = 1)
    my_canvas.create_text(700,30, text = "{}".format(noun.title()), font = font1)

    #adding the summary of the topic
    font2 = Font(family = "Times new roman", size = 20, underline = 1)
    my_canvas.create_text(190, 600, text = "Description:", font = font2)
    my_canvas.create_text(700,700, text = "{}".format(description), font = ("Times new roman", 10))

    #we need to find an image of the input given by the user
    url = "https://en.wikipedia.org/wiki/{}".format(noun)

    #get contents from the url
    content = requests.get(url).content

    #get soup
    soup = BeautifulSoup(content, 'lxml') #choose lxml parser

    #find the tag: : <img ... >
    image_tags = soup.findAll('img')

    #get first image tag in image_tags
    prefix = "http:"
    pic_url = prefix + image_tags[1].get('src')

    #open the web page picture and read it into a memory stream and
    #convert it to an image that Tkinter can handle
    my_page = urlopen(pic_url)

    #create an image file object
    my_picture = io.BytesIO(my_page.read())

    #use PIL to open image formats like .jpg
    pil_img = Image.open(my_picture)

    #convert to an image Tkinter can use
    tk_img = ImageTk.PhotoImage(pil_img)

    my_canvas.create_image(600,100, anchor = NW, image = tk_img).pack()

window = tkinter.Tk()
window.geometry("10000x10000") #adjusting window size
window.title("Wiki Search") #labeling window

canvas = Canvas(window, width = 5000, height = 5000)
canvas.pack()
#Adding a title to the search page
my_font = Font(family = "Times new roman", size = 40 , underline = 0)
canvas.create_text(700,300, text = "Wiki Search", font = my_font)

entry = tkinter.Entry(window)
canvas.create_window(700,350, window = entry)

button1 = tkinter.Button(text = "Search", command = wiki) #search button
button2 = tkinter.Button(text = "Quit", command = window.destroy)

canvas.create_window(700,400, window = button1)
canvas.create_window(700,450, window = button2)

#run gui
window.mainloop()
