# kuvantunnistus.py
import pyautogui
import cv2
import numpy as np
import os
import pytesseract

# Lisää polku jos ei ole PATH:ssa
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


#print(pyautogui.position())
KORTIT_DIR = 'korttikuvat'
NAPIT_DIR = 'templates'

# Ruudunkaappauksen alueet (muokkaa omien asetusten mukaan)
KASI_ALUE = (1340, 495, 100, 40)       # käsikorttien alue
POYTA_ALUE = (1235, 275, 350, 40)       # pöytäkorttien alue
NAPPI_ALUE = (1450, 600, 500, 150)
POTTI_ALUE = (1400, 250, 50, 20)
CALL_ALUE = (1705, 692,52, 27)
VIHUJEN_PANOSTUS = [()]

def hae_ruudunkaappaus(x, y, w, h):
    kuva = pyautogui.screenshot(region=(x, y, w, h))
    return cv2.cvtColor(np.array(kuva), cv2.COLOR_RGB2BGR)


def vertaa_templateen(kuva, template_path):
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        #print(f"VAROITUS: Ei löydy template-kuvaa {template_path}")
        return 0.0
    kuva_harmaa = cv2.cvtColor(kuva, cv2.COLOR_BGR2GRAY)

    th, tw = template.shape[:2]
    ih, iw = kuva_harmaa.shape[:2]
    if th > ih or tw > iw:
        print(f"Ohitetaan {os.path.basename(template_path)}: template ({th}x{tw}) suurempi kuin kuva ({ih}x{iw})")
        return 0.0

    res = cv2.matchTemplate(kuva_harmaa, template, cv2.TM_CCOEFF_NORMED)
    _, maksimi, _, _ = cv2.minMaxLoc(res)
    return maksimi

def tunnista_potti():
    potti_kuva = hae_ruudunkaappaus(*POTTI_ALUE)
    harmaa = cv2.cvtColor(potti_kuva, cv2.COLOR_BGR2GRAY)
    _, binari = cv2.threshold(harmaa, 180, 255, cv2.THRESH_BINARY)

    teksti = pytesseract.image_to_string(binari, config='--psm 7')
    # Suodata numeroita
    try:
        numerot = ''.join(c for c in teksti if c.isdigit() or c == '.')
        potti = float(numerot)
    except:
        potti = 0.0

    # Debug-kuva
    cv2.imwrite("debug_potti.png", potti_kuva)
    print(f"Potti luettu: {teksti.strip()} → {potti}")
    return potti

def tunnista_call_maksu():
    call_kuva = hae_ruudunkaappaus(*CALL_ALUE)
    harmaa = cv2.cvtColor(call_kuva, cv2.COLOR_BGR2GRAY)
    _, binari = cv2.threshold(harmaa, 180, 255, cv2.THRESH_BINARY)

    teksti = pytesseract.image_to_string(binari, config='--psm 7')
    # Suodata numeroita
    try:
        numerot = ''.join(c for c in teksti if c.isdigit() or c == '.')
        call = float(numerot)
    except:
        call = 0.0

    # Debug-kuva
    cv2.imwrite("debug_call.png", call_kuva)
    print(f"call luettu: {teksti.strip()} → {call}")
    return call

def tunnista_kortit(kuva):
    kortit = []
    for nimi in os.listdir(KORTIT_DIR):
        polku = os.path.join(KORTIT_DIR, nimi)
        arvo = vertaa_templateen(kuva, polku)
        #print(f"Template {nimi} osuma: {arvo:.2f}")
        if arvo > 0.95:
            kortit.append(nimi.replace('.png', ''))
    return kortit


def tunnista_napit(kuva):
    napit = []
    for nimi in os.listdir(NAPIT_DIR):
        polku = os.path.join(NAPIT_DIR, nimi)
        arvo = vertaa_templateen(kuva, polku)
        #print(f"Template {nimi} osuma: {arvo:.2f}")
        if arvo > 0.8:
           
            napit.append(nimi.replace('.png', ''))
    return napit


def tunnista_kortit_ja_napit():
    kasi_kuva = hae_ruudunkaappaus(*KASI_ALUE)
    poyta_kuva = hae_ruudunkaappaus(*POYTA_ALUE)
    nappikuva = hae_ruudunkaappaus(*NAPPI_ALUE)
    pottikuva = hae_ruudunkaappaus(*POTTI_ALUE)

    kadessa = tunnista_kortit(kasi_kuva)
    poydassa = tunnista_kortit(poyta_kuva)
    napit = tunnista_napit(nappikuva)
    potti = tunnista_potti()
    call = tunnista_call_maksu()
    #print(pyautogui.position())
    # debug-tallennus
    cv2.imwrite("debug_kasi.png", kasi_kuva)
    cv2.imwrite("debug_ptti.png", pottikuva)
    cv2.imwrite("debug_poyta.png", poyta_kuva)
    cv2.imwrite("debug_napit.png", nappikuva)

    return {'kadessa': kadessa, 'poydassa': poydassa, 'napit': napit, 'potti': potti, 'call': call}
