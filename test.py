import random, sys, re
from Tkinter import *
from tkSnack import *
import argparse

root = Tkinter.Tk()
root.withdraw()
initializeSnack(root)

base_freq_l = [
('C0', 16.35),
('C#0', 17.32),
('D0', 18.35),
('D#0', 19.45),
('E0', 20.60),
('F0', 21.83),
('F#0', 23.12),
('G0', 24.50),
('G#0', 25.96),
('A0', 27.50),
('A#0', 29.14),
('B0', 30.87),
]

def split(note):
    '''Helper function to split a note name into its constituent parts'''
    return filter(lambda s: not s.isdigit(), note).upper(), int(filter(lambda s: s.isdigit(), note))

def is_note(string):
    '''Check if string is well-formed note'''
    note = re.compile('^[a-gA-G][#b]?([0]|[1-9][0-9]*)$')
    return re.match(note, string)

def gen_octave(start, end):
    '''Generate the tones to test from, using the C0-B0 octave as a starting point'''
    tones = []
    while start <= end: # while we haven't reached the last octave we want
        for note, freq in base_freq_l:
            name, number = split(note)
            tones += [(name + str(number+start), freq*2**start)]
        start += 1
    return tones
    
def run(questions=10, invert=False, start_oct=4, end_oct=4):
    '''Main function that presents the stimuli and prints results'''
    test_l = gen_octave(start_oct, end_oct)
    while questions > len(test_l): # e.g. asking 50 questions about 12 notes
        test_l.append(test_l)
    random.shuffle(test_l)

    right_l, error_l = [], []
    for name, freq in test_l[:questions]:
        if invert:
            right, error = ask_name(name, freq)
        else:
            right, error = ask_freq(name, freq)
        right_l.append(right)
        error_l.append(error)
    
    print "Overall: {}/{} correct".format(right_l.count(True), questions)
    units = "semitones" if invert else "Hz"
    print "Off by an average of {:.0f} {}".format(sum(error_l)/len(error_l), units)
    print 'Full results: ', zip(right_l, error_l)


def ask_freq(name, freq):
    '''Ask "what frequency is this musical note"? Returns tuple of correctness (bool) and error (float)'''
    def is_float(s):
        try:
            float(s)
            return True
        except:
            return False
    ans = ''
    while not is_float(ans):
        ans = raw_input("What frequency is {}? (example answers: '440', '440.2') ".format(name))
    ans = float(ans)
    return ans == freq, ans - freq

def ask_name(name, freq):
    '''Ask what letter value is this frequency? Returns tuple of correctness (bool) and error (float). Answer is case-insensitive.'''
    beep(freq)
    ans = ''
    while not is_note(ans):
        ans = raw_input("What note was just played? (example answers: 'A4', 'a4') ".format(name))
    return ans.upper() in name, scale_dist(name, ans)

def beep(freq, duration=1, volume=1):
    '''Plays a beep of frequency "freq"'''
    s = Sound()
    filt = Filter('generator', 440, 30000, 0.0, 'sine', 8000)
    filt.configure(freq)
    s.play(filter=filt,blocking=1)

def scale_dist(one, two):
    '''Returns how much higher note two is than note one in semitones'''
    #print "DIFFERENCE: {} {}".format(one.lower(), two.lower())
    scale = map(lambda x: split(x[0])[0], base_freq_l) # just the note names
    # separate notes into their parts, e.g. A4, C4 = L1N1, L2N2
    (l1, n1), (l2, n2) = split(one), split(two)
    i1, i2 = scale.index(l1), scale.index(l2)
    
    letter_d = (i2 - i1) % len(scale) # distance of the letter portion of the notes
    # distance of the number portion: one octave for each difference of 1
    #   , fewer one octave when the notes span the gap between octaves (e.g. B4 to C5)
    number_d = len(scale) * (n2 - n1 - (i1 > i2)) # last part is a boolean evaluated to an int
    #print letter_d, number_d, letter_d+number_d
    return letter_d + number_d

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', type=int, dest='questions', default=10)
    parser.add_argument('--names', action='store_const', const=True, default=False)
    args = parser.parse_args()

    run(args.questions, args.names)

