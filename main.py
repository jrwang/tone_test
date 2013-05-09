import random
from Tkinter import *
from tkSnack import *

root = Tkinter.Tk()
root.withdraw()
initializeSnack(root)

name_freq_l = [('A4', 440), ('A3', 220), ('C4', 262)]

test_l = name_freq_l[:] # copy list
random.shuffle(test_l)

def run(invert=False, questions=10):
    results = []
    for name, freq in test_l[:questions]:
        if invert:
            right, error = ask_freq(name, freq)
        else:
            right, error = ask_name(name, freq)
        results.append((right, error))
    print 'results', results

def ask_freq(name, freq):
    '''Ask "what frequency is this musical note"? Returns tuple of correctness (bool) and error (float)'''
    ans = input("What frequency is {}? (example answer: '440')".format(name))
    return ans == freq, ans - freq

def ask_name(name, freq):
    '''Ask what letter value is this frequency? Returns tuple of correctness (bool) and error (float). Answer is case-insensitive.'''
    beep(freq)
    ans = raw_input("What note was just played? (example answer: 'A4')".format(name))
    return ans.upper() == name, scale_dist(name, ans)

def beep(freq, duration=1, volume=1):
    '''Plays a beep of frequency "freq"'''
    print "BEEP: freq{}".format(freq) 

    s = Sound()
    filt = Filter('generator', 440, 30000, 0.0, 'sine', 8000)

    filt.configure(freq)
    s.play(filter=filt,blocking=1)


def scale_dist(one, two):
    '''Returns how much higher note two is than note one in semitones'''
    print "DIFFERENCE: {} {}".format(one.lower(), two.lower())
    scale = "CDEFGAB" # ignore accidentals for now
    # separate notes into their parts, e.g. A4, C4 = L1N1, L2N2
    l1, n1, l2, n2 = one[0].upper(), int(one[1]), two[0].upper(), int(two[1])
    i1, i2 = scale.index(l1), scale.index(l2)
    
    letter_d = (i2 - i1) % len(scale) # distance of the letter portion of the notes
    # distance of the number portion: one octave for each difference of 1, fewer one octave when the notes span the gap between octaves (e.g. B4 to C5)
    number_d = len(scale) * (n2 - n1 - (i1 > i2)) # last part is a boolean evaluated to an int
    #print letter_d, number_d, letter_d+number_d
    return letter_d + number_d

if __name__ == "__main__":
    run()
    beep(440)

