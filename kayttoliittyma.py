'''

import tkinter as tk

ikkuna = None
teksti_label = None

def nayta_suositus(suositus, kadessa=None, poydassa=None):
    print("suositus", suositus, kadessa, poydassa)
    if type(suositus) is str:
        print("teksti")
    else:
        print("täällä")
        print("suosss", suositus, kadessa, poydassa)
        suositus = suositus * 100
        suositus = round(float(suositus), 1)
        global ikkuna, teksti_label
        teksti = f"{str(suositus)} %"
        if kadessa or poydassa:
            teksti += "\n"
            if kadessa:
                teksti += f"\nKädessä: {', '.join(kadessa)}"
            if poydassa:
                teksti += f"\nPöydässä: {', '.join(poydassa)}"

        if ikkuna is None:
            ikkuna = tk.Tk()
            ikkuna.title("Pokeriapuri")
            ikkuna.geometry("600x600+10+10")
            ikkuna.attributes('-topmost', True)
            ikkuna.overrideredirect(True)

            teksti_label = tk.Label(ikkuna, text=teksti, font=("Helvetica", 16), fg="white", bg="black", justify="center")
            teksti_label.pack(expand=True, fill='both')
            ikkuna.update()
        else:
            teksti_label.config(text=teksti)
            ikkuna.update()


'''
import tkinter as tk
ikkuna=teksti_label=None

def nayta_suositus(suositus,kadessa=None,poydassa=None):
    global ikkuna, teksti_label
    txt=suositus
    if kadessa or poydassa:
        txt+='\n'
        if kadessa: txt+=f"\nKädessä: {', '.join(kadessa)}"
        if poydassa: txt+=f"\nPöydässä: {', '.join(poydassa)}"
    if ikkuna is None:
        ikkuna=tk.Tk();ikkuna.title('Pokeriapuri');ikkuna.geometry('400x250+10+10');ikkuna.attributes('-topmost',True);ikkuna.overrideredirect(True)
        teksti_label=tk.Label(ikkuna,text=txt,font=('Helvetica',14),fg='white',bg='black',justify='center');teksti_label.pack(expand=True,fill='both');ikkuna.update()
    else:
        teksti_label.config(text=txt);ikkuna.update()