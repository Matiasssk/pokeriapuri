# kuvantunnistus.py
import pyautogui
import cv2
import numpy as np
import os

KORTIT_DIR = 'korttikuvat'
NAPIT_DIR = 'templates'

# Ruudunkaappauksen alueet (muokkaa omien asetusten mukaan)
KASI_ALUE = (1340, 495, 100, 40)       # käsikorttien alue
POYTA_ALUE = (1235, 275, 350, 40)       # pöytäkorttien alue
NAPPI_ALUE = (1450, 600, 500, 150)
POTTI_ALUE = (1200, 600, 300, 300)


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
    pass

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

    kadessa = tunnista_kortit(kasi_kuva)
    poydassa = tunnista_kortit(poyta_kuva)
    napit = tunnista_napit(nappikuva)

    # debug-tallennus
    cv2.imwrite("debug_kasi.png", kasi_kuva)
    cv2.imwrite("debug_poyta.png", poyta_kuva)
    cv2.imwrite("debug_napit.png", nappikuva)

    return {'kadessa': kadessa, 'poydassa': poydassa, 'napit': napit}
