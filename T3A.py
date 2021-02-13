import pygame
import datetime
from pygame.locals import *
from time import sleep
from sys import exit
from math import sin, cos, pi
import random

pygame.init()

scr_size = (640, 480)
win = pygame.display.set_mode(scr_size, 0, 32)
pygame.display.set_caption(" " * 80 + "Tic - Tac - Toe")
game_icon = pygame.image.load("assets/images/icon.png")
pygame.display.set_icon(game_icon)

snd_click = pygame.mixer.Sound("assets/sounds/click.ogg")
snd_line = pygame.mixer.Sound("assets/sounds/line.ogg")
snd_circle = pygame.mixer.Sound("assets/sounds/circle.ogg")
snd_screenshot = pygame.mixer.Sound("assets/sounds/screenshot.ogg")

TEXTCOLOR1 = (255, 97, 95)
TEXTCOLOR2 = (62, 197, 243)
TIECOLOR = (158, 147, 169)
WHITE = (255, 255, 255)
DARK = (40, 40, 40)
RED = (255, 0, 0)

    
class Game():
    
    def __init__(self, mode = "Single"): 
        
        self.xwon = self.ywon = self.drawn = self.move = 0
        self.settings_clicked = False
        self.arrow_y = 90
        self.menu_arrow_y = 160
        self.play_mode = mode
        self.at = 0
        self.comp_x = False
        
    def intro_screen(self):
        
        win.fill(DARK)
        intro_font = pygame.font.SysFont("Cambria", 100)
        splash_img = pygame.image.load("assets/images/splash.png")
        splash_text1 = intro_font.render("TIC", True, TEXTCOLOR1)
        splash_text2 = intro_font.render("TAC", True, TEXTCOLOR2)
        splash_text3 = intro_font.render("TOE", True, TEXTCOLOR1)
        win.blit(splash_img, (20, 10))
        win.blit(splash_text1, (30, 330))
        win.blit(splash_text2, (220, 330))
        win.blit(splash_text3, (420, 330))

        self.du()

        while True:

            for event in pygame.event.get():

                if event.type == QUIT:
                    exit()

                if event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
                    self.menu_screen()
    
    def menu_screen(self):
        
        self.draw_menu()
        self.du()
        
        while True:
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()

                if event.type == KEYDOWN:
                    
                    sleep(0.1)
                    pressed_keys = pygame.key.get_pressed()

                    if pressed_keys[K_UP] and self.arrow_y > 90:

                        self.arrow_y -= 80
                        snd_click.play()

                    if pressed_keys[K_DOWN] and self.arrow_y < 320:

                        self.arrow_y += 80
                        snd_click.play()

                    if pressed_keys[K_RETURN]:

                        snd_click.play()
                        sleep(0.5)

                        if self.arrow_y == 90:
                            self.game_screen()
                        elif self.arrow_y == 170:
                            self.choose_mode()
                        elif self.arrow_y == 250:
                            self.about_screen()
                        elif self.arrow_y == 330:
                            exit()
                    
                    self.draw_menu()
                    self.du()
                    
    def draw_menu(self):
          
        DARK_MODE = (50, 130, 180)
        LIGHT_MODE = (62, 197, 243)
        arrow = pygame.image.load("assets/images/arrow.png")
        win.fill(DARK)
        play_button = pygame.font.SysFont("Calibri", 70).render("Play", True, DARK_MODE if self.arrow_y != 90 else LIGHT_MODE)
        mode_button = pygame.font.SysFont("Calibri", 70).render("Mode", True, DARK_MODE if self.arrow_y != 170 else LIGHT_MODE)
        about_button = pygame.font.SysFont("Calibri", 70).render("About", True, DARK_MODE if self.arrow_y != 250 else LIGHT_MODE)
        quit_button  = pygame.font.SysFont("Calibri", 70).render("Quit", True, DARK_MODE if self.arrow_y != 330 else LIGHT_MODE)
        win.blit(play_button, (150, 70))
        win.blit(mode_button, (150, 150))
        win.blit(about_button, (150, 230))
        win.blit(quit_button, (150, 310))
        win.blit(arrow, (115, self.arrow_y))
          
    def choose_mode(self):
        
        self.draw_choose_mode()
        exitt = False
        
        while not exitt:
            
            for event in pygame.event.get():

                if event.type == QUIT:
                    exit()

                if event.type == KEYDOWN:

                    pressed_keys = pygame.key.get_pressed()
                    
                    if pressed_keys[K_DOWN] and self.menu_arrow_y < 280:
                        
                        snd_click.play()
                        self.menu_arrow_y += 60

                    if pressed_keys[K_UP] and self.menu_arrow_y > 160:

                        snd_click.play()
                        self.menu_arrow_y -= 60

                    if pressed_keys[K_RETURN]:

                        snd_click.play()
                        
                        if self.menu_arrow_y == 160:

                            game = Game("Single")
                            game.menu_screen()
                            exitt = True

                        if self.menu_arrow_y == 220:
                            
                            game = Game("Multi")
                            game.menu_screen()
                            exitt = True

                        if self.menu_arrow_y == 280:

                            exitt = True
                        
                        self.menu_arrow_y = 160
                        
                    self.draw_menu()
                    self.draw_choose_mode()
            
            self.du()
                    
        self.menu_screen()
         
    def draw_choose_mode(self):
        
        window = pygame.Surface((320, 200))
        window.set_alpha(200)
        window.fill(DARK)
        win.blit(window, (160, 120))
        win.blit(pygame.font.SysFont("Calibri", 50).render("Single Player", True, TEXTCOLOR2), (200, 150))
        win.blit(pygame.font.SysFont("Calibri", 50).render("Multi  Player", True, TEXTCOLOR2), (200, 210))
        win.blit(pygame.font.SysFont("Calibri", 50).render("Back", True, TEXTCOLOR2), (200, 265))
        arrow = pygame.image.load("assets/images/arrow.png")
        win.blit(arrow, (170, self.menu_arrow_y))
        self.du()
                    
    def game_screen(self):
        
        self.str_slots_x = ""
        self.str_slots_o = ""
        self.move = 0
        self.settings_clicked = False
        self.display_board()
        self.du()
        self.all_slots = []
        move_x = True
        
        while True:
            
            for event in pygame.event.get():
                
                if event.type == QUIT:
                    exit()  
                
                elif event.type == MOUSEBUTTONDOWN:
                
                    x, y = pygame.mouse.get_pos()
                
                    if pygame.mouse.get_pressed()[0]: 
                        
                        if x in range(15, 75) and y in range(30, 90):
                
                            if not self.settings_clicked:
                    
                                self.settings_clicked = True
                                self.settings_screen()
                        
                        if self.play_mode == "Single":
                            
                            if not self.comp_x:
                                
                                success = self.draw_x(x, y)
                                sleep(0.5)
                                self.check_win()
                                
                                if success:
                                    
                                    self.move += 1
                                    self.get_comp()
                                    self.draw_o(x, y)
                                    self.move += 1  
                                    self.check_win()
                                
                            else:  
                            
                                success = self.draw_o(x, y)
                                sleep(0.5)
                                self.check_win()
                                
                                if success:
                                    
                                    self.move += 1
                                    self.get_comp()
                                    self.draw_x(x, y)
                                    self.move += 1
                                    self.check_win()
                                
                        if self.play_mode == "Multi":
                            
                            if move_x:
                                success = self.draw_x(x, y)
                                if success:
                                    move_x = False
                                    self.move += 1
                                    
                            else:
                                success = self.draw_o(x, y)
                                if success:
                                    move_x = True
                                    self.move += 1
                            
                            self.check_win()
                            
    def about_screen(self):
        
        abfont = pygame.font.SysFont("Calibri", 30)
        abfontlarge = pygame.font.SysFont("Calibri", 40)
        heart = pygame.image.load("assets/images/heart.jpg")
        win.fill(DARK)
        copy = abfontlarge.render("(C) Ravidev Pandey", True, TEXTCOLOR2)
        line1 = abfont.render("Tic - Tac - Toe is an old school game, pretty known", True, WHITE)
        line2 = abfont.render("to everyone. Any of the players who manages to", True, WHITE)
        line3 = abfont.render("make a perfect three (horizontally, vertically, or", True, WHITE)
        line4 = abfont.render("either of the diagonally), wins.", True, WHITE)
        line5 = abfontlarge.render("The AI (Single Player Mode)", True, TEXTCOLOR1)
        line6 = abfont.render("You can't beat the AI. And by can't, I mean can't in", True, WHITE)
        line7 = abfont.render("capital letters (CAN NOT).", True, WHITE)
        line8 = abfont.render("(Music will be added if I get a bunch of free mp3s)", True, WHITE)
        win.blit(copy, (170, 10))
        win.blit(line1, (12, 60))
        win.blit(line2, (12, 95))
        win.blit(line3, (12, 130))
        win.blit(line4, (12, 165))
        win.blit(line5, (90, 230))
        win.blit(line6, (12, 295))
        win.blit(line7, (12, 330))
        win.blit(line8, (12, 375))
        win.blit(abfontlarge.render('Coded with' + " " * 10 + "in Python", True, WHITE), (100, 430))
        win.blit(heart, (305, 420))
        
        self.du()
        
        while True:
            
            for event in pygame.event.get():
                
                if event.type == QUIT:
                    exit()
                    
                if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                    self.menu_screen()     
    
    def settings_screen(self):
        
        self.screenshot()
        
        screenshotted = False
        
        back_icon = pygame.image.load("assets/images/back.png")
        darkness = pygame.Surface((640, 480))
        menu = pygame.Surface((320, 480))
        
        menu.set_alpha(20)
        darkness.set_alpha(150)
        darkness.fill(DARK)
        menu.fill(DARK)
        win.blit(darkness, (0, 0))
        
        for i in range(0, 320, 5):
            
            win.blit(menu, (i - 320, 0))    
            self.du()
            sleep(0.001)
            
        sleep(0.01)
        
        win.blit(pygame.font.SysFont("Calibri", 40).render("Quit", True, WHITE), (15, 30))
        win.blit(pygame.font.SysFont("Calibri", 40).render("Volume", True, WHITE), (15, 80))
        win.blit(pygame.font.SysFont("Calibri", 40).render("Screenshot", True, WHITE), (15, 130))
        win.blit(pygame.font.SysFont("Calibri", 40).render("Exit to menu", True, WHITE), (15, 180))
        win.blit(back_icon, (15, 380))
        self.du()
        
        while self.settings_clicked:
        
            for event in pygame.event.get():
                
                if event.type == QUIT:
                    exit()
                
                if event.type == MOUSEBUTTONDOWN:
                    
                    x, y = pygame.mouse.get_pos()
                    
                    if x in range(15, 75) and y in range(380, 440):
                        
                        self.settings_clicked = False
                    
                    if x in range(15, 85) and y in range(35, 60):
                    
                        exit()
                    
                    if x in range(15, 135) and y in range(85, 110):
                    
                        pass
                    
                    if x in range(15, 190) and y in range(135, 160):
                        
                        self.screenshot(True) 
                        screenshotted = True
                        self.settings_clicked = False
                    
                    if x in range(15, 215) and y in range(185, 210):
                        
                        self.menu_screen()
                        
        if not screenshotted:   
                                 
            scr = pygame.image.load("assets/temp/scrtmp.bmp")
            menu.set_alpha(230)
            
            for i in range(0, - 400, - 10):
                win.blit(scr, (0, 0))
                win.blit(menu, (i, 0))
                self.du()
    
        self.du()
    
    def display_board(self):
        
        win.fill(DARK)
        settings_icon = pygame.image.load("assets/images/settings.png")
        win.blit(pygame.font.SysFont("Cambria", 50).render("X", True, TEXTCOLOR2), (540, 10))
        win.blit(pygame.font.SysFont("Cambria", 20).render("(" + str(self.xwon) + ")", True, TEXTCOLOR2), (585, 30))
        win.blit(pygame.font.SysFont("Cambria", 50).render("O", True, TEXTCOLOR1), (538, 60))
        win.blit(pygame.font.SysFont("Cambria", 20).render("(" + str(self.ywon) + ")", True, TEXTCOLOR1), (585, 80))
        win.blit(pygame.font.SysFont("Cambria", 50).render("T", True, TIECOLOR), (540, 110))
        win.blit(pygame.font.SysFont("Cambria", 20).render("(" + str(self.drawn) + ")", True, TIECOLOR), (585, 130))
        win.blit(settings_icon, (15, 30))
        pygame.draw.rect(win, WHITE, Rect((120, 40), (400, 400)), 5)
        pygame.draw.line(win, WHITE, (100, 173), (540, 173), 3)
        pygame.draw.line(win, WHITE, (100, 307), (540, 307), 3)
        pygame.draw.line(win, WHITE, (253, 20), (253, 460), 3)
        pygame.draw.line(win, WHITE, (387, 20), (387, 460), 3)
    
    def draw_x(self, x, y, draw = False, won = False):
        
        if self.comp_x and self.at == 1 or x in range(120, 253) and y in range(40, 173) and "1" not in self.str_slots_x + self.str_slots_o:
            x = 140; y = 53; self.add_to_strs("1"); draw = True
        if self.comp_x and self.at == 2 or  x in range(256, 387) and y in range(40, 173) and "2" not in self.str_slots_x + self.str_slots_o:
            x = 276; y = 53; self.add_to_strs("2"); draw = True
        if self.comp_x and self.at == 3 or  x in range(390, 523) and y in range(40, 173) and "3" not in self.str_slots_x + self.str_slots_o:
            x = 405; y = 53; self.add_to_strs("3"); draw = True
        if self.comp_x and self.at == 4 or  x in range(120, 253) and y in range(173, 307) and "4" not in self.str_slots_x + self.str_slots_o:
            x = 140; y = 186; self.add_to_strs("4"); draw = True
        if self.comp_x and self.at == 5 or  x in range(256, 387) and y in range(173, 307) and "5" not in self.str_slots_x + self.str_slots_o:
            x = 276; y = 186; self.add_to_strs("5"); draw = True
        if self.comp_x and self.at == 6 or  x in range(390, 523) and y in range(173, 307) and "6" not in self.str_slots_x + self.str_slots_o:
            x = 405; y = 186; self.add_to_strs("6"); draw = True
        if self.comp_x and self.at == 7 or  x in range(120, 253) and y in range(307, 440) and "7" not in self.str_slots_x + self.str_slots_o:
            x = 140; y = 320; self.add_to_strs("7"); draw = True
        if self.comp_x and self.at == 8 or  x in range(256, 387) and y in range(307, 440) and "8" not in self.str_slots_x + self.str_slots_o:
            x = 276; y = 320; self.add_to_strs("8"); draw = True
        if self.comp_x and self.at == 9 or  x in range(390, 523) and y in range(307, 440) and "9" not in self.str_slots_x + self.str_slots_o:
            x = 405; y = 320; self.add_to_strs("9"); draw = True
        if won:
            x = 276; y = 188
            
        if draw:
            
            snd_line.play()
            
            t = y
            for i in range(x, x + 95):
                for j in range(t, t + 15):

                    win.set_at((i, j), TEXTCOLOR2)
                self.du()
                t += 1
                sleep(0.001)
                  
            sleep(0.2)
            
            snd_line.play()
            
            k = x + 95
            t = y

            for i in range(x, x + 95):
                for j in range(t, t + 15):

                    win.set_at((k, j), TEXTCOLOR2)
                k -= 1
                t += 1
                self.du()
                sleep(0.001)
        
            return draw    
    
    def draw_o(self, x, y, draw = False, won = False):
        
        if not self.comp_x and self.at == 1 or x in range(120, 253) and y in range(40, 173) and "1" not in self.str_slots_x + self.str_slots_o:
            x = 140; y = 56; draw = True; self.add_to_strs("1")
        if not self.comp_x and self.at == 2 or x in range(256, 387) and y in range(40, 173) and "2" not in self.str_slots_x + self.str_slots_o:
            x = 273; y = 56; draw = True; self.add_to_strs("2")
        if not self.comp_x and self.at == 3 or x in range(390, 523) and y in range(40, 173) and "3" not in self.str_slots_x + self.str_slots_o:
            x = 405; y = 56; draw = True; self.add_to_strs("3")
        if not self.comp_x and self.at == 4 or x in range(120, 253) and y in range(173, 307) and "4" not in self.str_slots_x + self.str_slots_o:
            x = 140; y = 190; draw = True; self.add_to_strs("4")
        if not self.comp_x and self.at == 5 or x in range(256, 387) and y in range(173, 307) and "5" not in self.str_slots_x + self.str_slots_o:
            x = 273; y = 190; draw = True; self.add_to_strs("5")
        if not self.comp_x and self.at == 6 or x in range(390, 523) and y in range(173, 307) and "6" not in self.str_slots_x + self.str_slots_o:
            x = 405; y = 190; draw = True; self.add_to_strs("6")
        if not self.comp_x and self.at == 7 or x in range(120, 253) and y in range(307, 440) and "7" not in self.str_slots_x + self.str_slots_o:
            x = 140; y = 323; draw = True; self.add_to_strs("7")
        if not self.comp_x and self.at == 8 or x in range(256, 387) and y in range(307, 440) and "8" not in self.str_slots_x + self.str_slots_o:
            x = 273; y = 323; draw = True; self.add_to_strs("8")
        if not self.comp_x and self.at == 9 or x in range(390, 523) and y in range(307, 440) and "9" not in self.str_slots_x + self.str_slots_o:
            x = 405; y = 323; draw = True; self.add_to_strs("9")
        if won:
            x = 273; y = 188
            
        if draw:
            
            i = pi * 2
            
            snd_circle.play()
            
            while int(i) != -1:
                
                pygame.draw.arc(win, TEXTCOLOR1, (x, y, 100, 100), i + pi / 2, pi / 2, 10)
                self.du()
                i -= 0.012
            
            return draw
    
    def add_to_strs(self, pos):
        
        if self.play_mode == "Single":
                    
            if not self.comp_x and self.move % 2 == 0:
                
                self.str_slots_x += pos
                self.all_slots.append(int(pos))
            
            else:
            
                self.str_slots_o += pos
                self.all_slots.append(int(pos))
        
        if self.play_mode == "Multi":
            
            if self.move % 2 == 0:
                self.str_slots_x += pos        
            else:
                self.str_slots_o += pos
    
    def get_comp(self):
        
        move_list = "12 21 23 32 13 31 45 54 56 65 46 64 78 87 79 97 89 98 14 41 17 71 47 74 25 52 28 82 58 85 39 93 69 96 36 63 15 51 59 95 19 91 37 73 35 53 57 75".split()
        to_move = [3, 3, 1, 1, 2, 2, 6, 6, 4, 4, 5, 5, 9, 9, 8, 8, 7, 7, 7, 7, 4, 4, 1, 1, 8, 8, 5, 5, 2, 2, 6, 6, 3, 3, 9, 9, 9, 9, 1, 1, 5, 5, 5, 5, 7, 7, 3, 3]
        sasta_move_list = "2 4 6 8".split()
        sasta_to_move = [4, 2, 8, 6]
        tricky_move_list = "1 3 7 9".split()
        trickt_self_at = "9 7 3 1".split()
        tricky_to_move = [7, 9, 1, 3]
        another_list = "48 84 26 62 86 68 24 42".split()
        another_to_move = [7, 7, 3, 3, 9, 9, 1, 1]
        
        if self.move == 1:
            
            if "5" not in self.str_slots_x:
                
                self.at = 5
                self.all_slots.append(5)

            else:

                rand = random.choice([1, 3, 7, 9])
                self.at = rand
                self.all_slots.append(rand)
 
        elif self.move == 3:
            
            found = False
            
            for i in range(len(move_list)):

                if found:
                    break
                
                if move_list[i] in self.str_slots_x and to_move[i] not in self.all_slots:
                    
                    self.at = to_move[i]
                    self.all_slots.append(to_move[i])
                    found = True
            
            if not found:
                
                if "5" in self.str_slots_x:
                    for i in range(len(tricky_move_list)):
                        
                        if found:
                            break
                        
                        if tricky_move_list[i] in self.str_slots_x and trickt_self_at[i] in self.str_slots_o:
                            
                            self.at = tricky_to_move[i]
                            self.all_slots.append(tricky_to_move[i])
                            found = True
            
            if not found:
                
                for i in range(len(another_list)):
                    
                    if found:
                        break
                    
                    if another_list[i] in self.str_slots_x:
                        
                        self.at = another_to_move[i]
                        self.all_slots.append(another_to_move[i])
                        found = True
            
            if not found:

                for i in range(len(sasta_move_list)):

                    if found:
                        break
                    
                    if sasta_move_list[i] in self.str_slots_x and sasta_to_move[i] not in self.all_slots:
                        self.at = sasta_to_move[i]
                        found = True
                        self.all_slots.append(sasta_to_move[i])
            
            if not found:
                
                ran = random.choice([2, 4, 6, 8])

                while ran in self.all_slots:
                    ran = random.choice([2, 4, 6, 8])
                    
                self.at = ran
                self.all_slots.append(ran)
 
        elif self.move == 5 or self.move == 7:
            
            found = False
            
            for i in range(len(move_list)):
                
                if found:
                
                    self.at = to_move[i - 1]
                    self.all_slots.append(to_move[i - 1])
                    break
                
                if move_list[i] in self.str_slots_o and to_move[i] not in self.all_slots:        
                    
                        self.at = to_move[i]
                        self.all_slots.append(to_move[i])
                        found = True
                        break
                
                for j in range(2):
                    
                    if move_list[i][j] in self.str_slots_o and to_move[i] not in self.all_slots:
                        found = True
                    else:
                        found = False
                        break
            
            if not found:
                
                for i in range(len(move_list)):
                    
                    if found:
                    
                        self.at = to_move[i - 1]
                        self.all_slots.append(to_move[i - 1])
                        break
                    
                    if move_list[i] in self.str_slots_x and to_move[i] not in self.all_slots:        
                            
                            self.at = to_move[i]
                            self.all_slots.append(to_move[i])
                            found = True
                            break
                    
                    for j in range(2):
                    
                        if move_list[i][j] in self.str_slots_x and to_move[i] not in self.all_slots:
                            found = True
                        else:
                            found = False
                            break
            
            if not found:    
                for i in range(1, 10):

                    if i not in self.all_slots:
                        self.at = i
                        break
                
    def check_win(self):
        
        win_pos = "123 456 789 159 357 147 258 369 123".split()
        x_won = False
        o_won = False
        
        if self.play_mode == "Single":
        
            if not self.comp_x:
                slots_x = self.str_slots_x
                slots_o = self.str_slots_o
            else:
                slots_o = self.str_slots_x
                slots_x = self.str_slots_o
                
        if self.play_mode == "Multi":
        
            slots_x = self.str_slots_x
            slots_o = self.str_slots_o
        
        for i in win_pos:
            if x_won:

                self.xwon += 1
                self.display_winner("X")
                break

            for j in range(3):

                if i[j] not in slots_x:
                    x_won = False
                    break
                else:
                    x_won = True
                    
        for i in win_pos:
            if o_won:

                self.ywon += 1
                self.display_winner("O")
                break

            for j in range(3):

                if i[j] not in slots_o:
                    o_won = False
                    break
                else:
                    o_won = True
        
        if len(self.str_slots_x + self.str_slots_o) == 9:
            self.drawn += 1
            self.display_winner("TIE")
    
    def display_winner(self, comp):
        
        sleep(1)    
        result_display = pygame.Surface((640, 200))
        result_display.set_alpha(10)
        k = 640
        
        for i in range(- 640, - 270, 4):
                
            win.blit(result_display, (i, 140))
            win.blit(result_display, (k, 140))
            k -= 4
            self.du()
                
        sleep(1)
        
        if comp == "X":
            
            self.draw_x(276, 188, True, True)
        
        if comp == "O":
        
            self.draw_o(273, 188, True, True)
        
        if comp == "TIE":
            
            win.blit(pygame.font.SysFont("Calibri", 180).render("TIE", True, WHITE), (210, 160))
            self.du()
        
        sleep(1)
        win.blit(pygame.font.SysFont("Calibri", 30).render("Click anywhere to continue", True, WHITE), (160, 310))
        self.du()
        
        clicked = False
        while not clicked:
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                
                if event.type == MOUSEBUTTONDOWN:
                    clicked = True
                    break
        
        result_display.set_alpha(230)
        k = 320
        
        for i in range(- 320, - 680, - 14):
            
            self.display_board()  
            win.blit(result_display, (i, 140))
            win.blit(result_display, (k, 140))
            k += 14
            self.du()
                    
        sleep(1)
        self.game_screen()
    
    def du(self):
        pygame.display.update()
        
    def screenshot(self, save = False):
        
        name = "assets/temp/scrtmp.bmp"
        
        screenshot = pygame.Surface((640, 480))
        
        if not save:
        
            for y in range(480):
                for x in range(640):
                    screenshot.set_at((x, y), win.get_at((x, y)))
                    
            pygame.image.save(screenshot, name)
        
        if save:
            
            screenshot_blur = pygame.Surface((640, 480))
            screenshot_blur.fill(WHITE)
            screenshot_blur.set_alpha(2)
            
            d = datetime.datetime.today()
            dateandtime = ""

            for things in [d.year, d.month, d.day, d.hour, d.minute, d.second]:
                dateandtime += str(things) + " "
            
            scr = pygame.image.load("assets/temp/scrtmp.bmp")
            
            pygame.image.save(scr, "Screenshots/" + dateandtime + ".bmp")
                            
            for i in range(100):

                win.blit(screenshot_blur, (0, 0))
                self.du()
                sleep(0.0001)
            
            snd_screenshot.play()
            
            screenshot_blur.set_alpha(255)
            win.blit(screenshot_blur, (0, 0))
            self.du() 
                            
            sleep(0.5)
                                
            for i in range(250, 0, - 10):
                                
                screenshot_blur.set_alpha(i)
                win.blit(scr, (0, 0))
                win.blit(screenshot_blur, (0, 0))
                self.du()
                sleep(0.005)
                            
            win.blit(scr, (0, 0))
        
        
game = Game()
game.intro_screen()
