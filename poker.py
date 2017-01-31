import random
mydeck = [r+s for r in '23456789TJQKA' for s in 'SHDC']


def deal(numhands, n=5, deck=mydeck):
    random.shuffle(deck)
    return [deck[n*i:n*(i+1)] for i in range(numhands)]
    # "Random.sample doesn't work because te cards might be repeated"
    # h = random.sample(deck, n*numhands)
    # hands = []
    # for i in range(0, numhands):
    #     hands.append(h[n*i: n*(i+1)])
    # return hands


def poker(hands):
    "Return a list of all winning hand: "
    return allmax(hands, key=hand_rank)

def allmax(iterable, key=None):
    """Return a list of all items equal to the max of the iterable."""
    result, maxval = [], None
    key = key or (lambda x: x)
    for x in iterable:
        xval = key(x)
        if not result or xval > maxval:
            result, maxval = [x], xval
        elif xval == maxval:
            result.append(x)
    return result

def hand_rank(hand):
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):            # straight flush
        return (8, max(ranks))
    elif kind(4, ranks):                           # 4 of a kind
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):        # full house
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):                              # flush
        return (5, ranks)
    elif straight(ranks):                          # straight
        return (4, max(ranks))
    elif kind(3, ranks):                           # 3 of a kind
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):                          # 2 pair
        return (2, two_pair(ranks)[0], two_pair(ranks)[1])
    elif kind(2, ranks):                           # kind
        return (1, kind(2, ranks), ranks)
    else:                                          # high card
        return (0, ranks)

def card_ranks(hand): #H, C, S, D for suit, and 2 to 14 for 2 to A
    "hand has to have max 5 cards(items)"
    ranks = ['--23456789TJQKA'.index(r) for r,s in hand]
    ranks.sort(reverse=True)
    # handle Ace low straight
    return [5, 4, 3, 2, 1] if (ranks == [14, 5, 4, 3, 2]) else ranks

def straight(ranks):
    "Return true if cards form a straight"
    return (max(ranks) - min(ranks) == 4) and len(set(ranks)) == 5

def flush(hand):
    "Return true if all cards have same set"
    suits = [s for r,s in hand]
    return len(set(suits)) == 1

def kind(num, ranks):
    """Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-kind in the hand."""
    for r in ranks:
        if ranks.count(r) == num: return r
    return None

def two_pair(ranks):
    """If there are two pair, return the two ranks as a
    tuple: (highest, lowest); otherwise return None."""
    high = kind(2, ranks)
    low = kind(2, list(reversed(ranks)))
    if high and high != low:
        return (high, low)
    return None

def hand_percentages(n=700*1000):
    counts = [0] *9
    for i in range(int(n/10)):
        for hand in deal(10):
            ranking = hand_rank(hand)[0]
            counts[ranking] += 1
    for i in reversed(range(9)):
        print ("%6.3f" % (100 * counts[i]/n))


hand_percentages()
def test():
    "Test cases for the functions in poker program"
    sf = "6C 7C 8C 9C TC".split() # Straight Flush
    fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
    fh = "TD TC TH 7C 7D".split() # Full House
    tp = "TD 9H TH 7C 9S".split() # Two Pair
    assert card_ranks(sf) == [10, 9, 8, 7, 6]
    assert card_ranks(fk) == [9, 9, 9, 9, 7]
    assert card_ranks(fh) == [10,10,10,7, 7]
    assert straight([9, 8, 7, 6, 5]) == True
    assert straight([9, 8, 8, 6, 5]) == False
    assert flush(sf) == True
    assert flush(fk) == False
    fkranks = card_ranks(fk)
    tpranks = card_ranks(tp)
    assert kind(4, fkranks) == 9
    assert kind(3, fkranks) == None
    assert kind(2, fkranks) == None
    assert kind(1, fkranks) == 7
    assert two_pair(tpranks) == (10, 9)
    assert poker([fh, fh]) == [fh, fh]
    assert poker([sf, fh, fk]) == [sf]
    # assert poker([sf] + 99*[fh]) == sf
    # assert hand_rank(sf) == (8, 10)
    # assert hand_rank(fk) == (7, 9, 7)
    # assert hand_rank(fh) == (6, 10, 7)
    return 'tests pass'

print(test())
