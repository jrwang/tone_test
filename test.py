import random
from Tkinter import *
from tkSnack import *
import argparse

from noteutils import *

root = Tkinter.Tk()
root.withdraw()
initializeSnack(root)

def run(questions, invert, octaves):
    '''Main function that presents the stimuli and prints results'''
    base = []
    if not nonaturals:
        base += naturals_freq_l
    if not nosharps:
        base += sharps_freq_l
    if not noflats:
        base += flats_freq_l

    test_l = gen_octave(base, *octaves)
    while questions > len(test_l): # e.g. asking 50 questions about 12 notes
        test_l.extend(test_l)
    random.shuffle(test_l)

    right_l, error_l = [], []
    for name, freq in test_l[:questions]:
        if invert:
            right, error = ask_name(name, freq)
        else:
            right, error = ask_freq(name, freq)
        right_l.append(right)
        error_l.append(error)
    
    correct = right_l.count(True)
    print "Overall: {}/{} correct, {:.1%}%".format(correct, questions, float(correct)/questions)
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
    if training:
        print "Answer: {} Hz".format(freq)
    return float(ans) == freq, float(ans) - freq

def ask_name(name, freq):
    '''Ask what letter value is this frequency? Returns tuple of correctness (bool) and error (float). Answer is case-insensitive.'''
    beep(freq)
    ans = ''
    while not is_note(ans):
        ans = raw_input("What note was just played? (example answers: 'A4', 'a4') ".format(name))
    if training:
        acc = '/{}'.format(sharp_flat(name)) if is_acc(name) else ''
        print "Answer: {}{}".format(name, acc)
    ans = ans[0].upper() + ans[1:]
    return ans == name or sharp_flat(ans) == name, scale_dist(name, ans)

def beep(freq, duration=1, volume=1):
    '''Plays a beep of frequency "freq"'''
    s = Sound()
    filt = Filter('generator', 440, 30000, 0.0, 'sine', 8000)
    filt.configure(freq)
    s.play(filter=filt,blocking=1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', type=int, dest='questions', default=10)
    parser.add_argument('--names', action='store_const', const=True, default=False)
    parser.add_argument('--training', action='store_const', const=True, default=False)
    parser.add_argument('--nonaturals', action='store_const', const=True, default=False)
    parser.add_argument('--nosharps', action='store_const', const=True, default=False)
    parser.add_argument('--noflats', action='store_const', const=True, default=False)
    parser.add_argument('--octaves', type=int, nargs=2, default=[4,4])
    args = parser.parse_args()
    training, nosharps, noflats, nonaturals = args.training, args.nosharps, args.noflats, args.nonaturals

    run(args.questions, args.names, args.octaves)

