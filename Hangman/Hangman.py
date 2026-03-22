
'''      Created on 04 August 2020
        @ Created by: Ashutosh Kamboj
'''


from word import *
import pygame
import random
import math
import tkinter as tk
from tkinter import ttk


win=tk.Tk()
win.title("HANGMAN")
l=ttk.Label(win,text="Choose the category to PLAY the game with.",font="Arial 15").grid()

# setting up Radio Buttons
cat=tk.StringVar()
b1=ttk.Radiobutton(win,text="Fruits",value="fruit",variable=cat)
b1.grid(row=1,column=0)

b2=ttk.Radiobutton(win,text="Vegetables",value="vegetable",variable=cat)
b2.grid(row=2,column=0)

b3=ttk.Radiobutton(win,text="Cars",value="car",variable=cat)
b3.grid(row=3,column=0)




def actions():

    # setup screen
    pygame.init()
    width, height = 1200, 700

    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("HANGMAN GAME")
    done = True
    clock = pygame.time.Clock()

    # Getting word
    word_list=[]
    if 'fruit' == cat.get():
        word_list = fruit_list[:]
    elif 'vegetable'== cat.get():
        word_list = veg_list[:]
    elif 'car'== cat.get():
        word_list = car_list[:]

    word = random.choice(word_list)


    word=word.upper()
    guessed=[]


    # loading hangman images
    images = []
    for i in range(8):
        image = pygame.image.load("hm" + str(i) + ".png")
        images.append(image)

    # buttons
    rad = 30
    gap = 15
    store = []
    startx = round((width - (rad * 2 + gap) * 13) / 2)
    starty = 500
    A=65
    for i in range(26):
        x = startx + gap * 2 + ((rad * 2 + gap) * (i % 13))
        y = starty + ((i // 13) * (gap + rad * 2))
        store.append([x,y,chr(A+i),True])

    lf=pygame.font.SysFont("Arial black",35)
    wf1=pygame.font.SysFont("Castellar ",55)
    wf = pygame.font.SysFont("Timesroman ", 55)
    def draw():
        win.fill((255, 200, 150))
        text=wf1.render("HANGMAN GAME",1,(0,0,0))
        win.blit(text,(text.get_width()//2,10))
        display_word=""
        for l in word:
            if l in guessed:
                display_word += l + " "
            else:
                display_word += "_ "
        text= wf.render(display_word,1,(0,0,0))
        win.blit(text,(350,180))
        text=wf.render("Word Consists "+str(len(word))+ " letters.",1,(0,0,0))
        win.blit(text, (350, 80))
        for l in store:
            x , y , ch , visible = l
            if visible:
                pygame.draw.circle(win, (0, 0, 0), (x, y), rad, 5)
                text =lf.render(ch,1,(0,0,0))
                win.blit(text,(x- text.get_width()//2,y- text.get_height()//2))
        win.blit(images[tries], (30, 100))

        # If Tries got finished
        if tries ==0:
            win.fill((0,0,0))
            win.blit(images[tries], (30, 30))
            text = wf.render("THE "+cat.get().upper()+" WAS:", 1, (255,255,255))
            win.blit(text, (400, 160))
            text = wf.render(word, 1, (255,255,255))
            win.blit(text, (400, 230))
            pygame.display.update()
            pygame.time.delay(5000)
            exit(1)


        # if WON
        if "_ " not in display_word:
            win.fill((0, 0, 0))
            win.blit(images[7],(400, 200))
            text = wf.render("YOU WON!", 2, (255, 255, 255))
            win.blit(text,(400, 30))
            pygame.display.update()
            pygame.time.delay(5000)
            exit(1)

        pygame.display.update()

    # game on screen setup
    tries = 6
    while done:
        clock.tick(60)

        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x,pos_y=pygame.mouse.get_pos()
                for l in store:
                    x,y,ch,visible= l
                    distance= math.sqrt((x-pos_x)**2+(y-pos_y)**2)
                    if visible:
                        if distance<rad:
                            l[3]=False
                            guessed.append(ch)
                            if ch not in word:
                                tries-=1



    pygame.display.flip()
    pygame.quit()


l1=ttk.Label(win,text="Click Below  To Play Hangman",font="Calibiri")
l1.grid()

# setiing up submit button
submit=tk.Button(win,text="PLAY",font='Calibiri',width="20",command=actions)
submit.grid()
win.mainloop()
