import pygame,queue, pygame.mixer
import time as pytime
from pygame import *
import random
from os import path


BIALY     = (255, 255, 255)
CZARNY     = (  0,   0,   0)
NIEBIESKI     = (  0,   0, 255)   
CZERWONY       = (220,   0,   0)
ZIELONY     = (  0, 200,   0)
ZIELONYHEAD = ( 0, 255, 0 )
FIOLET      = (147, 112, 219)
ZOLTY = (255, 255, 0)
CIEMNY_ZIELONY = (0, 150,   0)
SZARY  = ( 30,  30,  30)

sounds_dir = path.join(path.dirname(__file__), 'sounds')

pygame.mixer.init()


przegrana=pygame.mixer.Sound(path.join(sounds_dir,'failureSound.ogg'))
muzyka_w_tle=pygame.mixer.Sound(path.join(sounds_dir,'music.wav'))
hello=pygame.mixer.Sound(path.join(sounds_dir,'hello.wav'))



wynik = 0
WIDTH = 600
HEIGHT = 600

WIDTH_IN_BLOCKS = 20
HEIGHT_IN_BLOCKS = 20

TICK = 0.5
PAUZA = False
BONUS_CZAS = 0
MUREK_CZAS = 20
MUREK_CZAS1 = 20
MUREK_CZAS2 = 20    

pygame.init();

ekran=pygame.display.set_mode((WIDTH, HEIGHT))
image  = pygame.image.load('start.jpg')
image1  = pygame.image.load('grass.jpg')

image2 = pygame.image.load('apple.png')
image3  = pygame.image.load('body.jpg')
image4  = pygame.image.load('end.png')
image5 = pygame.image.load('bonus.png')
image6 = pygame.image.load('obstacle.png')

pygame.display.set_caption('Snake') #tytul
zegar=pygame.time.Clock()

blok = pygame.Surface((WIDTH/WIDTH_IN_BLOCKS, WIDTH/HEIGHT_IN_BLOCKS))
blok.blit(image3,(0,0))
przysmak = pygame.Surface((WIDTH/WIDTH_IN_BLOCKS, WIDTH/HEIGHT_IN_BLOCKS))
przysmak.blit(image2,(0,0))

bonus = pygame.Surface((WIDTH/WIDTH_IN_BLOCKS, WIDTH/HEIGHT_IN_BLOCKS))
bonus.blit(image5,(0,0))

murek = pygame.Surface((WIDTH/WIDTH_IN_BLOCKS, WIDTH/HEIGHT_IN_BLOCKS))
murek.blit(image6,(0,0))

snake = queue.Queue()
x = random.randint(0,WIDTH_IN_BLOCKS-1)
y = random.randint(0,HEIGHT_IN_BLOCKS-1)
snake.put((x,y))  #poczatkowe 4 człony weza
snake.put((x,y))
snake.put((x,y))  
snake.put((x,y))
kierunek=(1,0)   #okreslenie kierunku początkowego węża



def SprawdzCzyKlawisz():
    if len(pygame.event.get(QUIT)) > 0:
        zatrzymanie_gry()
 
    klawisz_event = pygame.event.get(KEYUP)
    if len(klawisz_event) == 0:
        return None
    if klawisz_event[0].key == K_ESCAPE:
        zatrzymanie_gry()
    return klawisz_event[0].key




def menu_poczatkowe():
    
    poz_a = WIDTH/2-155
    poz_b = HEIGHT/2+250
    poz_x = WIDTH/2-160
    poz_xx = WIDTH/2-10
    poz_y = HEIGHT/2 + 60
    szerokosc_przyc = 130
    wysokosc_przyc = 70
    pygame.draw.rect(ekran, ZIELONY,(poz_x,poz_y,szerokosc_przyc,wysokosc_przyc))
    pygame.draw.rect(ekran, CZERWONY,(poz_xx,poz_y,szerokosc_przyc,wysokosc_przyc))
    
    czcionka = pygame.font.SysFont("Comic Sans MS", 50)
    rys_przycisk = czcionka.render('PLAY', True, CZARNY)
    ekran.blit(rys_przycisk,(poz_x,poz_y))
    
    czcionka1 = pygame.font.SysFont("Comic Sans MS", 45)
    rys_przycisk = czcionka1.render('QUIT', True, CZARNY)
    ekran.blit(rys_przycisk,(poz_xx,poz_y))
    
    czcionka2 = pygame.font.SysFont("Comic Sans MS", 20)
    rys_przycisk = czcionka2.render('Press space to pause the game', True, CZARNY)
    ekran.blit(rys_przycisk,(poz_a,poz_b))

    mysz = pygame.mouse.get_pos()
    klikniecie = pygame.mouse.get_pressed()
    
    if poz_x < mysz[0] < poz_x + szerokosc_przyc and poz_y < mysz[1] < poz_y + wysokosc_przyc:  #jak dziala ten warunek?
        
        if klikniecie[0] == 1:
            return "GRAJ"
        
    if poz_xx < mysz[0] < poz_xx + szerokosc_przyc and poz_y < mysz[1] < poz_y + wysokosc_przyc:  #jak dziala ten warunek?
        
        if klikniecie[0] == 1:
            pygame.quit()
            quit()    
            

def ekran_startowy():
    
    czcionka = pygame.font.SysFont("Comic Sans MS", 120)
    start_napis = czcionka.render('SNAKE', True, CZARNY)
    hello.play()
   
   
    while True:
        ekran.blit(image, (0,0))
        ekran.blit(start_napis, (WIDTH/2-210,HEIGHT/2-140))
 
        if SprawdzCzyKlawisz():
            pygame.event.get()
        
        klikniecie = menu_poczatkowe()
        if klikniecie == "GRAJ":
            return 
 
        pygame.display.update()
        
def gameover_screen():
    przegrana.play()
    ekran.fill(BIALY)
    ekran.blit(image4, (0,0))
    czcionka = pygame.font.Font('freesansbold.ttf', 130)
    czcionka1 =  pygame.font.Font('freesansbold.ttf', 40)
    game = czcionka.render('Game', True, CZARNY)
    over = czcionka.render('Over', True, CZARNY)
    ekran.blit(game, (WIDTH/2-250,HEIGHT/2-160))
    ekran.blit(over, (WIDTH/2-70,HEIGHT/2))
    
    wynik_tekst = czcionka1.render('Your score: %s' % wynik, True, CZARNY)
    ekran.blit(wynik_tekst,(WIDTH/2-130,HEIGHT/2+200))

    pygame.display.update()
    pygame.time.wait(3000)
    ekran_startowy()
    
def rys_wynik(wynik):
    czcionka = pygame.font.SysFont("Comic Sans MS", 25)
    wynik_napis = czcionka.render('SCORE: %s' % (wynik), True, CZARNY)
    ekran.blit(wynik_napis, (0, 0))
    
def pauza():
    pygame.time.wait(True)
    czcionka = pygame.font.SysFont("Comic Sans MS", 30)
    rys_pauza = czcionka.render('Press space to resume game', True, SZARY)        
    ekran.blit(rys_pauza, (WIDTH/2-200,HEIGHT/2-10))
    pygame.display.update()
    

def zatrzymanie_gry():
    pygame.mixer.music.stop()
    pygame.quit()
    quit()



def rys_waz(lista):    # lista = [(x1, y1), (x2, y2), ...]
    for i in lista:
        x = (i[0]*int(WIDTH/WIDTH_IN_BLOCKS))  #dlaczego tutaj i[0] a niżej i[1]?
        y = (i[1]*int(HEIGHT/HEIGHT_IN_BLOCKS))
        ekran.blit(blok, (x, y))
        
#PRZYSMAK
def generuj_przysmak(snake):
    x = random.randint(0,WIDTH_IN_BLOCKS-1)
    y = random.randint(0,HEIGHT_IN_BLOCKS-1)
    while ((x,y) in snake or (x,y) ==  bonus): 
         y = random.randint(0,HEIGHT_IN_BLOCKS-1)
    return (x, y)

def rys_przysmak(x, y):
    ekran.blit(przysmak,(x*int(WIDTH/WIDTH_IN_BLOCKS),y*int(HEIGHT/HEIGHT_IN_BLOCKS)))
    
#B0NUS    
def generuj_bonus(snake,przysmak):
    x = random.randint(0,WIDTH_IN_BLOCKS-4)
    y = random.randint(0,HEIGHT_IN_BLOCKS-1)
    while ((x,y) in snake or (x,y)==przysmak):
         x = random.randint(0,WIDTH_IN_BLOCKS-4)
         y = random.randint(0,HEIGHT_IN_BLOCKS-1)
    print(x, y)
    return (x, y)

def rys_bonus(x, y):
    global BONUS_CZAS
    
    BONUS_CZAS += 1
    
    if BONUS_CZAS < 40:
        ekran.blit(bonus,(x*int(WIDTH/WIDTH_IN_BLOCKS),y*int(HEIGHT/HEIGHT_IN_BLOCKS)))    
    
    if BONUS_CZAS > 80:
        BONUS_CZAS = 0


#MURKI
def generuj_murek(snake,przysmak,bonus):
    x = random.randint(0,WIDTH_IN_BLOCKS-4)
    y = random.randint(0,HEIGHT_IN_BLOCKS-1)
    flag = True
    while flag:
        while ((x,y) in snake or (x+1 ,y) in snake or (x+2 ,y) in snake or (x+3, y) in snake or (x,y) == przysmak or (x,y) == bonus):
             x = random.randint(0,WIDTH_IN_BLOCKS-4)
             y = random.randint(0,HEIGHT_IN_BLOCKS-1)
        flag = False    
    print(x, y)
    return (x, y)

def generuj_murek1(snake,przysmak,bonus,murek):
    x1 = random.randint(0,WIDTH_IN_BLOCKS-4)
    y1 = random.randint(0,HEIGHT_IN_BLOCKS-1)
    flag = True
    while flag:
        while ((x1,y1) in snake or (x1,y1) == murek or (x1+1,y1) == murek or (x1 +2,y1) == murek or (x1 + 3,y1) == murek or (x1+1 ,y1) in snake or (x1+2 ,y1) in snake or (x1+3, y1) in snake or (x1,y1) == przysmak or (x1+1,y1) == przysmak or (x1+2,y1) == przysmak or (x1 + 3,y1) == przysmak or (x1,y1) == bonus or (x1+1,y1) == bonus or (x1+2,y1) == bonus or (x1 + 3,y1) == bonus ):
             x1 = random.randint(0,WIDTH_IN_BLOCKS-4)
             y1 = random.randint(0,HEIGHT_IN_BLOCKS-1)
        flag = False     
    print(x1, y1)
    return (x1, y1)

def generuj_murek2(snake,przysmak,bonus,murek,murek1):
    x2 = random.randint(0,WIDTH_IN_BLOCKS-4)
    y2 = random.randint(0,HEIGHT_IN_BLOCKS-1)
    flag = True
    while flag:
        while ((x2,y2) in snake or (x2,y2) == murek or (x2+1,y2) == murek or (x2 +2,y2) == murek or (x2 + 3,y2) == murek or (x2,y2) == murek1 or (x2+1,y2) == murek1 or (x2 +2,y2) == murek1 or (x2 + 3,y2) == murek1 or (x2+1 ,y2) in snake or (x2+2 ,y2) in snake or (x2+3, y2) in snake or (x2,y2) == przysmak or (x2+1,y2) == przysmak or (x2+2,y2) == przysmak or (x2 + 3,y2) == przysmak or (x2,y2) == bonus or (x2+1,y2) == bonus or (x2+2,y2) == bonus or (x2 + 3,y2) == bonus ):
             x2 = random.randint(0,WIDTH_IN_BLOCKS-4)
             y2 = random.randint(0,HEIGHT_IN_BLOCKS-1)
        flag = False    
    print(x2, y2)
    return (x2, y2)

def rys_murek(x, y):
    ekran.blit(murek,(x*int(WIDTH/WIDTH_IN_BLOCKS),y*int(HEIGHT/HEIGHT_IN_BLOCKS)))
    ekran.blit(murek,((x+1)*int(WIDTH/WIDTH_IN_BLOCKS),y*int(HEIGHT/HEIGHT_IN_BLOCKS)))
    ekran.blit(murek,((x+2)*int(WIDTH/WIDTH_IN_BLOCKS),y*int(HEIGHT/HEIGHT_IN_BLOCKS)))
    ekran.blit(murek,((x+3)*int(WIDTH/WIDTH_IN_BLOCKS),y*int(HEIGHT/HEIGHT_IN_BLOCKS)))
    

def rys_murek1(x1, y1):
    ekran.blit(murek,(x1*int(WIDTH/WIDTH_IN_BLOCKS),y1*int(HEIGHT/HEIGHT_IN_BLOCKS)))
    ekran.blit(murek,((x1+1)*int(WIDTH/WIDTH_IN_BLOCKS),y1*int(HEIGHT/HEIGHT_IN_BLOCKS)))
    ekran.blit(murek,((x1+2)*int(WIDTH/WIDTH_IN_BLOCKS),y1*int(HEIGHT/HEIGHT_IN_BLOCKS)))
    ekran.blit(murek,((x1+3)*int(WIDTH/WIDTH_IN_BLOCKS),y1*int(HEIGHT/HEIGHT_IN_BLOCKS)))

def rys_murek2(x2, y2):
    ekran.blit(murek,(x2*int(WIDTH/WIDTH_IN_BLOCKS),y2*int(HEIGHT/HEIGHT_IN_BLOCKS)))
    ekran.blit(murek,((x2+1)*int(WIDTH/WIDTH_IN_BLOCKS),y2*int(HEIGHT/HEIGHT_IN_BLOCKS)))
    ekran.blit(murek,((x2+2)*int(WIDTH/WIDTH_IN_BLOCKS),y2*int(HEIGHT/HEIGHT_IN_BLOCKS)))
    ekran.blit(murek,((x2+3)*int(WIDTH/WIDTH_IN_BLOCKS),y2*int(HEIGHT/HEIGHT_IN_BLOCKS)))
    




def zjadl_przysmak(glowa,przysmak):   # (x1, y1),   (x2, y2)
    return glowa == przysmak      #zawsze zapominalam zapytac jak dziala to wydluzanie sie weza, co to znaczy ze glowa == przysmak?

def zjadl_bonus(glowa,bonus):
    return glowa == bonus  

def kolizja(glowa,lista,murek_x, murek_y,murek_x1,murek_y1,murek_x2, murek_y2):
    if glowa in lista:
        return True
    
    if murek_x is None:
        return False
    if murek_x1 is None:
        return False
    if murek_x2 is None:
        return False
    #murek pierwszy
    m1 = (murek_x, murek_y)
    m2 = (murek_x + 1, murek_y)
    m3 = (murek_x + 2, murek_y)
    m4 = (murek_x + 3, murek_y)
    
    #murek drugi
    m11 = (murek_x1, murek_y1)
    m22 = (murek_x1 + 1, murek_y1)
    m33 = (murek_x1 + 2, murek_y1)
    m44 = (murek_x1 + 3, murek_y1)
    
    #murek trzeci
    m111 = (murek_x2, murek_y2)
    m222 = (murek_x2 + 1, murek_y2)
    m333 = (murek_x2 + 2, murek_y2)
    m444 = (murek_x2 + 3, murek_y2)
    
    if m1 in lista or m2 in lista or m3 in lista or m4 in lista or  m111 in lista or m222 in lista or m333 in lista or m444 in lista or  m11 in lista or m22 in lista or m33 in lista or m44 in lista:
        return True
    
    return False

def poruszanie_wezem(kierunek, rzeczywisty_kierunek):
    global PAUZA
    
    for e in pygame.event.get():

        if e.type == QUIT:
            pygame.quit()
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_UP and rzeczywisty_kierunek!=(0,1):kierunek=(0,-1);
            elif e.key == K_DOWN and rzeczywisty_kierunek!=(0,-1):kierunek=(0,1)
            elif e.key == K_LEFT and rzeczywisty_kierunek!=(1,0):kierunek=(-1,0)
            elif e.key == K_RIGHT and rzeczywisty_kierunek!=(-1,0):kierunek=(1,0)
            elif e.key == K_SPACE:
                PAUZA = True if PAUZA == False else False
                
    return kierunek

last_timestamp = pytime.time()  #czy to jest czas trwanie gry?
przys_x, przys_y = generuj_przysmak(list(snake.queue))
rys_przysmak(przys_x, przys_y)

bon_x, bon_y = generuj_bonus(list(snake.queue),(przys_x, przys_y))
rys_bonus(bon_x, bon_y)

murek_x, murek_y = generuj_murek(list(snake.queue), (przys_x, przys_y), (bon_x, bon_y))
murek_x1, murek_y1 = generuj_murek1(list(snake.queue), (przys_x, przys_y), (bon_x, bon_y),(murek_x, murek_y))
murek_x2, murek_y2 = generuj_murek2(list(snake.queue), (przys_x, przys_y), (bon_x, bon_y),(murek_x, murek_y),(murek_x1, murek_y1))

flag = True
while flag:
    if ((przys_x,przys_y)==(bon_x, bon_y) or(przys_x,przys_y) == (murek_x, murek_y)or (przys_x,przys_y) == (murek_x1, murek_y1) or (przys_x,przys_y) ==(murek_x2, murek_y2)):
           przys_x, przys_y = generuj_przysmak(list(snake.queue))
    else:
        flag = False
flag1 = True
while flag1:       
    if   ((bon_x, bon_y) == (murek_x, murek_y) or (bon_x, bon_y)==(murek_x1, murek_y1)or (bon_x, bon_y)==(murek_x2, murek_y2)):
        bon_x, bon_y = generuj_bonus(list(snake.queue),(przys_x, przys_y))
    else:
        flag1 = False


rys_murek(murek_x, murek_y)
rys_murek1(murek_x1, murek_y1)
rys_murek2(murek_x2, murek_y2)

rzeczywisty_kierunek = kierunek
ekran_startowy()

while (True):
    muzyka_w_tle.play()

    
    current_timestamp = pytime.time()
    kierunek = poruszanie_wezem(kierunek, rzeczywisty_kierunek)

    if PAUZA == True:
        pauza()
        continue
   

    if not current_timestamp  > last_timestamp + TICK:  #to chyba odpowiada za przechodzenie przes scianki, tylko jak dokladnie?
        continue

    last_timestamp = current_timestamp

    ekran.blit(image1, (0,0))
    glowa=list(snake.queue)[-1]  #tzn ze ostatni element kolejki jest poczatkiem weza?
    nowaGlowa=((kierunek[0]+glowa[0]) % WIDTH_IN_BLOCKS, (kierunek[1]+glowa[1]) % HEIGHT_IN_BLOCKS) #czym jest teraz now glowa?
    
    if kolizja(nowaGlowa,list(snake.queue),murek_x,murek_y,murek_x1,murek_y1,murek_x2,murek_y2):
        muzyka_w_tle.stop()
        gameover_screen() 
        #przegrana.play()
        wynik = 0
        TICK = 0.5
        murek_x, murek_y = generuj_murek(list(snake.queue), (przys_x, przys_y), (bon_x, bon_y))
        murek_x1, murek_y1 = generuj_murek1(list(snake.queue), (przys_x, przys_y), (bon_x, bon_y),(murek_x, murek_y))
        murek_x2, murek_y2 =generuj_murek2(list(snake.queue), (przys_x, przys_y), (bon_x, bon_y),(murek_x, murek_y),(murek_x1, murek_y1))


        snake = queue.Queue()
        x = random.randint(0,WIDTH_IN_BLOCKS-1)
        y = random.randint(0,HEIGHT_IN_BLOCKS-1)
        snake.put((x,y))  
        snake.put((x,y))
        snake.put((x,y))  
        snake.put((x,y))
        kierunek=(1,0)
    
    if BONUS_CZAS > 49:
        bon_x, bon_y = generuj_bonus(list(snake.queue),(przys_x, przys_y))
        flag2 = True
        while flag2:       
            if   ((bon_x, bon_y) == (murek_x, murek_y) or (bon_x, bon_y)==(murek_x1, murek_y1)or (bon_x, bon_y)==(murek_x2, murek_y2)):
                bon_x, bon_y = generuj_bonus(list(snake.queue),(przys_x, przys_y))
            else:
                flag2 = False
    
    MUREK_CZAS += 1
    MUREK_CZAS1 += 1
    MUREK_CZAS2 += 1

    
    if MUREK_CZAS > 40:
        MUREK_CZAS = 0
        murek_x, murek_y = generuj_murek(list(snake.queue), (przys_x, przys_y), (bon_x, bon_y))
        
    if MUREK_CZAS1 > 40:
        MUREK_CZAS1 = 0
        murek_x1, murek_y1 = generuj_murek1(list(snake.queue), (przys_x, przys_y), (bon_x, bon_y),(murek_x, murek_y))
    
    if MUREK_CZAS2 > 40:
        MUREK_CZAS2 = 0
        murek_x2, murek_y2 =generuj_murek2(list(snake.queue), (przys_x, przys_y), (bon_x, bon_y),(murek_x, murek_y),(murek_x1, murek_y1))
    
    
    if zjadl_przysmak(nowaGlowa,(przys_x,przys_y)):
        #dzwiek_zjadanego_jablka.play()
        przys_x, przys_y = generuj_przysmak(list(snake.queue))
        flag3 = True
        while flag:
            if ((przys_x,przys_y)==(bon_x, bon_y) or(przys_x,przys_y) == (murek_x, murek_y)or (przys_x,przys_y) == (murek_x1, murek_y1) or (przys_x,przys_y) ==(murek_x2, murek_y2)):
                przys_x, przys_y = generuj_przysmak(list(snake.queue))
            else:
                flag3 = False
        wynik += 1
        
        if wynik%4 == 0:
            TICK -= 0.03
            if TICK < 0.15:
                TICK = 0.15
    elif zjadl_bonus(nowaGlowa,(bon_x,bon_y)) and BONUS_CZAS < 40:
        bon_x, bon_y = generuj_bonus(list(snake.queue),(przys_x, przys_y))
        flag4 = True
        while flag4:       
            if   ((bon_x, bon_y) == (murek_x, murek_y) or (bon_x, bon_y)==(murek_x1, murek_y1)or (bon_x, bon_y)==(murek_x2, murek_y2)):
                bon_x, bon_y = generuj_bonus(list(snake.queue),(przys_x, przys_y))
            else:
                flag4 = False
        if BONUS_CZAS > 20:
            BONUS_CZAS += 20
        else:
            BONUS_CZAS += 30
      
        wynik += 3
        
        if wynik%4==0:
            TICK -= 0.03 
            if TICK < 0.15:
                TICK = 0.15
    else:
        snake.get() #wyciagniecie pierwszego elementu z kolejki FIFO - to odpowiada za wydluzenie weza?
                
    snake.put(nowaGlowa)  #jaka jest tego funcja?
    rys_waz(list(snake.queue))
    rzeczywisty_kierunek = kierunek
    rys_przysmak(przys_x, przys_y)
    rys_bonus(bon_x, bon_y)
    
    rys_murek(murek_x, murek_y)
    rys_murek1(murek_x1, murek_y1)
    rys_murek2(murek_x2, murek_y2)


    rys_wynik(wynik)
    
    pygame.display.update() #odswiezenie ekranu
