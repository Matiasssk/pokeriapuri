from kuvantunnistus import tunnista_kortit_ja_napit
from tekoaly import run_equity_simulation
from kayttoliittyma import nayta_suositus
import time


def main():
    print("Pokeriapuri käynnistyy...")
    pot = 100
    call_amount = 10
    while True:
        tilanne = tunnista_kortit_ja_napit()
        kadessa = tilanne.get("kadessa", [])
        poydassa = tilanne.get("poydassa", [])

        if len(kadessa) < 2:
            nayta_suositus("Ei tunnistettu käden kortteja.", kadessa, poydassa)
        else:
            equity, decision, ci = run_equity_simulation(
                kadessa, poydassa,
                num_opponents=3,
                num_sims=2000,
                pot=pot,
                call_amount=call_amount
            )
            teksti = f"{decision} ({equity:.2%}), CI [{ci[0]:.2%}, {ci[1]:.2%}]"
            nayta_suositus(teksti, kadessa, poydassa)

        time.sleep(2)

if __name__ == "__main__":
    main()


'''

def main():
    print("Pokeriapuri käynnistyy...")
    while True:
        tilanne = tunnista_kortit_ja_napit()
        # Debug: tulosta tunnistetut kortit ja napit
        print(f"Tunnistetut kortit: {tilanne['kortit']}, napit: {tilanne['napit']}")
        suositus = analysoi_kasi(tilanne)
        nayta_suositus(suositus)
        time.sleep(2)


if __name__ == "__main__":
    main()
'''