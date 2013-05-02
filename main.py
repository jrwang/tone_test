import random

name_freq_l = [('A4', 440)]

test_l = name_freq_l[:] # copy list
random.shuffle(test_l)

def run(invert=False, questions=10):
    for name, freq in test_l[:questions]:
        if invert:
            right, error = ask_freq(name, freq)
        else:
            right, error = ask_name(name, freq)

def ask_freq(name, freq):
    '''Ask "what frequency is this musical note"? Returns tuple of correctness (bool) and error (float)'''
    ans = input("What frequency is {}?".format(name))
    return ans==freq, ans-freq
    

def ask_name(name, freq):
    '''Ask what letter value is this frequency? Returns tuple of correctness (bool) and error (float). Answer is case-insensitive.'''
    beep(freq)
    ans = input("What note is this frequency? (e.g. 'A4')".format(name))
    return ans==name, scale_dist(name, ans)

def beep(freq, duration=1, volume=1):
    '''Plays a beep of frequency "freq"'''
    print "PLACEHOLDER: freq is {}".format(freq) 

def scale_dist(one, two):
    '''Returns the scale distance between two notes in semitones'''
    print "PLACEHOLDER: {} {}".format(one.lower(), two.lower())


