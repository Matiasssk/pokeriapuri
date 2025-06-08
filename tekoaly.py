'''


def arvioi_kaden_voima(kortit):
    arvo_map = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
        '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }
    pisteet = 0
    for kortti in kortit:
        # Oletetaan kortti merkkijonona esim. '10H', 'AS', '7D'
        arvo = kortti[:-1]  # kaikki paitsi viimeinen merkki (maa)
        pisteet += arvo_map.get(arvo.upper(), 0)
    return pisteet

def analysoi_kasi(tilanne):
    kadessa = tilanne.get('kadessa', [])
    poydassa = tilanne.get('poydassa', [])
    napit = tilanne.get('napit', [])

    kaikki_kortit = kadessa + poydassa

    if not kaikki_kortit:
        return "Ei tunnistettu tarpeeksi tietoa."

    voima = arvioi_kaden_voima(kaikki_kortit)

    # Esimerkkiarvot, voit säätää
    if voima < 30:
        return "Fold"
    elif voima < 50:
        return "Call"
    else:
        return "Raise"
'''
'''
from treys import Card, Evaluator

def arvioi_kaden_voima_treys(kadessa, poydassa):
    # Muunna kortit Treys-muotoon
    def muunna_treys(kortti):
        # Oletetaan kortit muodossa esim. '10H', 'AS', '7D'
        arvo = kortti[:-1].upper()
        maa = kortti[-1].upper()

        # Treys käyttää muotoa esim. 'As', 'Td', '7h' (iso arvo, pieni maa)
        arvo_map = {
            '10': 'T', 'J': 'J', 'Q': 'Q', 'K': 'K', 'A': 'A',
            '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9'
        }
        maa_map = {'H': 'h', 'D': 'd', 'C': 'c', 'S': 's'}

        return Card.new(arvo_map[arvo] + maa_map[maa])

    evaluator = Evaluator()

    käsi = [muunna_treys(k) for k in kadessa]
    pöytä = [muunna_treys(k) for k in poydassa]

    score = evaluator.evaluate(pöytä, käsi)
    # score on matala = hyvä käsi, korkea = huono

    return score

def analysoi_kasi_treys(tilanne):
    kadessa = tilanne.get('kadessa', [])
    poydassa = tilanne.get('poydassa', [])

    if not kadessa:
        return "Ei tunnistettu tarpeeksi tietoa."

    score = arvioi_kaden_voima_treys(kadessa, poydassa)

    # Treys score: alle 100 = erinomainen, 100-500 = hyvä, yli 1000 = heikko
    if score < 100:
        return "Raise"
    elif score < 500:
        return "Call"
    else:
        return "Fold"
'''
'''


from treys import Card, Deck, Evaluator
import random

def muunna_treys(kortti):
    # Oletetaan kortit muodossa esim. '10H', 'AS', '7D'
    arvo = kortti[:-1].upper()
    maa = kortti[-1].upper()

        # Treys käyttää muotoa esim. 'As', 'Td', '7h' (iso arvo, pieni maa)
    arvo_map = {
            '10': 'T', 'J': 'J', 'Q': 'Q', 'K': 'K', 'A': 'A',
            '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9'
    }
    maa_map = {'H': 'h', 'D': 'd', 'C': 'c', 'S': 's'}

    return Card.new(arvo_map[arvo] + maa_map[maa])

def simulate_equity(tilanne, num_opponents=5, num_sims=20000):
    evaluator = Evaluator()
    wins = 0
    ties = 0
    hole_cards = tilanne.get('kadessa', [])
    board_cards = tilanne.get('poydassa', [])
    # Muunna string-muotoiset kortit treys-kirjaston muotoon
    hero_hole = [muunna_treys(k) for k in hole_cards]
    board = [muunna_treys(k) for k in board_cards]

   # hero_hole = [Card.new(c) for c in hole_cards]
   # board = [Card.new(c) for c in board_cards]

    for _ in range(num_sims):
        deck = Deck()

        # Poista käytetyt kortit pakasta
        for c in hero_hole + board:
            if c in deck.cards:
                deck.cards.remove(c)

        # Arvo vastustajille 2 korttia kullekin
        opponents = []
        for _ in range(num_opponents):
            opp_hole = [deck.draw(1)[0], deck.draw(1)[0]]
            opponents.append(opp_hole)

        # Jaa loput pöytäkortit (turn ja river) jos ne puuttuvat
        needed = 5 - len(board)
        community = list(board) + [deck.draw(1)[0] for _ in range(needed)]

        # Arvioi oma käsi
        hero_score = evaluator.evaluate(hero_hole, community)
        # Arvioi vastustajien kädet
        opp_scores = [evaluator.evaluate(opp, community) for opp in opponents]

        best_opp = min(opp_scores)
        if hero_score < best_opp:
            wins += 1
        elif hero_score == best_opp:
            # Jos on tasapeli, jaetaan potki tasaisesti
            num_tied = opp_scores.count(hero_score) + 1
            ties += 1 / num_tied

    equity = (wins + ties) / num_sims
    return equity
'''

from treys import Card, Evaluator, Deck
from functools import lru_cache
import random, math
from concurrent.futures import ProcessPoolExecutor, as_completed

# Pre-calc master deck once
_MASTER_DECK = Deck().cards
EVAL = Evaluator()

@lru_cache(maxsize=None)
def _eval_rank(hand_tuple, board_tuple):
    return EVAL.evaluate(list(hand_tuple), list(board_tuple))


def _simulate_once(args):
    hand_cards, board_cards, num_opponents = args
    deck = _MASTER_DECK.copy()
    for c in hand_cards + board_cards:
        deck.remove(c)
    random.shuffle(deck)
    # sim board
    needed = 5 - len(board_cards)
    board = board_cards + tuple(deck[:needed])
    idx = needed
    hero = _eval_rank(hand_cards, board)
    # opponents
    opp_ranks = []
    for i in range(num_opponents):
        opp = tuple(deck[idx + 2*i: idx + 2*i + 2])
        opp_ranks.append(_eval_rank(opp, board))
    best_opp = min(opp_ranks)
    if hero < best_opp:
        return (1, 0)
    elif hero == best_opp:
        return (0, 1/ (opp_ranks.count(best_opp)+1))
    else:
        return (0, 0)


def run_equity_simulation(kadessa, poydassa, num_opponents=3, num_sims=5000, pot=1, call_amount=0):
    # convert to treys
    def to_card(s):
        v = s[:-1].upper(); v = 'T' if v=='10' else v
        m = s[-1].lower()
        return Card.new(v+m)

    hand = tuple(to_card(k) for k in kadessa)
    board = tuple(to_card(b) for b in poydassa)

    # prepare args for parallel
    args = [(hand, board, num_opponents)] * num_sims
    wins=ties=0
    # parallel
    with ProcessPoolExecutor() as exe:
        for win, tie in exe.map(_simulate_once, args):
            wins+=win; ties+=tie

    equity = (wins+ties)/num_sims
    # confidence interval
    se = math.sqrt(equity*(1-equity)/num_sims)
    ci = (equity-1.96*se, equity+1.96*se)
    # pot odds
    pot_odds = call_amount/(pot+call_amount) if call_amount>0 else 0
    if equity > pot_odds:
        decision = 'Call'
    else:
        decision = 'Fold'
    if equity>0.6: decision='Raise'
    return equity, decision, ci

