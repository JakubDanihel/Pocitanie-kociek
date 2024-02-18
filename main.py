import random
import time

# Nastavenie konštánt pre kocky
KOCKA_WIDTH = 9
KOCKA_HEIGHT = 5
CANVAS_WIDTH = 79
CANVAS_HEIGHT = 24 - 3  # -3 predstavuje veľkosť do ktorej sa môže vložiť celkový súčet na koniec

# Nastavenie času
QUIZ_DURATION = 30
MIN_DICE = 2  # Minimálny počet kociek
MAX_DICE = 6  # Maximálny počet kociek

ODMENA = 4  # Odmena za uhádnutú správnu odpoveď
PENALITY = 1  # Trest za zle uhádnutú odpoveď

# Program skončí ak je počet kociek väčší ako sa môže zmestiť na plochu
assert MAX_DICE <= 14

D1 = ([
    '+-------+',
    '|       |',
    '|   0   |',
    '|       |',
    '+-------+',
], 1)
D2a = ([
    '+-------+',
    '| 0     |',
    '|       |',
    '|     0 |',
    '+-------+',
], 2)
D2b = ([
    '+-------+',
    '|     0 |',
    '|       |',
    '| 0     |',
    '+-------+',
], 2)
D3a = ([
    '+-------+',
    '| 0     |',
    '|   0   |',
    '|     0 |',
    '+-------+',
], 3)
D3b = ([
    '+-------+',
    '|     0 |',
    '|   0   |',
    '| 0     |',
    '+-------+',
], 3)
D4 = ([
    '+-------+',
    '| 0   0 |',
    '|       |',
    '| 0   0 |',
    '+-------+',
], 4)
D5 = ([
    '+-------+',
    '| 0   0 |',
    '|   0   |',
    '| 0   0 |',
    '+-------+',
], 5)
D6a = ([
    '+-------+',
    '| 0 0 0 |',
    '|       |',
    '| 0 0 0 |',
    '+-------+',
], 6)
D6b = ([
    '+-------+',
    '| 0   0 |',
    '| 0   0 |',
    '| 0   0 |',
    '+-------+',
], 6)

ALL_KOCKY = [D1, D2a, D2b, D3a, D3b, D4, D5, D6a, D6b]

print("""Kockova matematika.

Spocitaj celkovu sumu na zobrazenych stenach kociek na ploche. Na odpoved mas {} sekund kde musis odpovedat na co najvacsi pocet spravnych odpovedii.
Za kazdu spravnu odpoved dostanes {} pocet bodov a za kazdu nespravnu odpoved ti bude odpocitany {} pocet bodov.
""".format(QUIZ_DURATION, ODMENA, PENALITY))

input("Stlac ENTER pre pokracovanie: ")

# Uloz celkovy pocet spravne uhadnutých odpovedii
spravneOdpovede = 0
nespravneOdpovede = 0

startTime = time.time()

# Začiatok hlavného cyklu
while time.time() < startTime + QUIZ_DURATION:
    # Zobraz kocky
    sumAnswer = 0
    diceFaces = []

    for i in range(random.randint(MIN_DICE, MAX_DICE)):
        die = random.choice(ALL_KOCKY)
        diceFaces.append(die[0])
        #sum_str = die[2].strip()  # Riadok so strednými bodkami
        sumAnswer += die[1]

    topLeftDiceCorners = []

    #urcenie kde bdu kocky
    for i in range(len(diceFaces)):
        while True:
            left = random.randint(0, CANVAS_WIDTH - 1 - KOCKA_WIDTH)
            top = random.randint(0, CANVAS_HEIGHT - 1 - KOCKA_HEIGHT)
            #toto urci x, y koordynaty vsetkych kociek

            topLeftX = left
            topLeftY = top
            topRightX = left + KOCKA_WIDTH
            topRightY = top
            
            bottomLeftX = left
            bottomLeftY = top + KOCKA_HEIGHT
            bottomRightX = left + KOCKA_WIDTH
            bottomRightY = top + KOCKA_HEIGHT

            #urcenie ci sa kocky neprekrykavaju
            overlaps = False
            for prevKockaLeft, prevKockaTop in topLeftDiceCorners:
                prevKockaRight = prevKockaLeft + KOCKA_WIDTH
                prevKockaBottom = prevKockaTop + KOCKA_HEIGHT

                #urcenie ci jeden z rohou nie je v kocke
                for rohX, rohY in((topLeftX,topLeftY),
                                  (topRightX,topRightY),
                                  (bottomLeftX,bottomLeftY),
                                  (bottomRightX,bottomRightY)):
                    if(prevKockaLeft <= rohX < prevKockaRight and prevKockaTop <= rohY <prevKockaBottom):
                        overlaps = True
            
            if not overlaps:
                #ak sa kocky neprekrivaju tak sa pokracuje
                topLeftDiceCorners.append((left, top))
                break

    #Vykreslenie kocku
    #klucove su koordinaty (x, y) tuple intov, hodnota charakerov v danej pozicii v kocke
    
    canvas = {}

    #loop pre kazdu kocku
    for i, (dieLeft, dieTop) in enumerate(topLeftDiceCorners):
        #loop pre kazdy charakter v stene kocky
        dieFace = diceFaces[i]

        for dx in range(KOCKA_WIDTH):
            for dy in range(KOCKA_HEIGHT):
                #prepisanie charakterov na kocke
                canvasX = dieLeft + dx
                canvasY = dieTop + dy
                #dieFace je list stringov, x a y su preto prehodene
                canvas[(canvasX, canvasY)] = dieFace[dy][dx]

    #vykreslenie na obrazovku
    for cy in range(CANVAS_HEIGHT):
        for cx in range(CANVAS_WIDTH):
            print(canvas.get((cx, cy), ' '), end = '')
        print()
    
    #moznos pre hraca zolit si moznost
    odpoved = input("Zadaj pocet: ").strip()
    if odpoved.isdecimal() and int(odpoved) == sumAnswer:
        spravneOdpovede +=1
    else:
        print("Nespavna, odpoved je: ", sumAnswer)
        time.sleep(2)
        nespravneOdpovede += 1

# zobrazenie finálneho výsledku
skore = (spravneOdpovede * ODMENA) - (nespravneOdpovede * PENALITY)
print("Správne odpovede: ", spravneOdpovede)
print("Nesprávne odpovede: ", nespravneOdpovede)
print("Celkové skore: ", skore)
