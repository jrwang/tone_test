import re


def split(note):
    '''Helper function to split a note name into its constituent parts'''
    return filter(lambda s: not s.isdigit(), note), int(filter(lambda s: s.isdigit(), note))

#
# Frequencies
#
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

scale = map(lambda x: split(x[0])[0], base_freq_l) # just the note names
#
# structure a little messy because of dependencies
#

def is_sharp(note):
    return '#' in note

def is_flat(note):
    return 'b' in note[1:] # ignore the first note in case lowercase B

def is_acc(note):
    return is_sharp(note) or is_flat(note)

def sharp_flat(note):
    '''Return the flatted equivalent of a sharp or vice versa. Returns naturals unchanged.'''
    naturals = filter(lambda n: '#' not in n, scale)
    name, octave = split(note)
    accidentals = [('#', 1, 'b'), ('b', -1, '#')]
    a = filter(lambda x: x[0] in name, accidentals) # find the relevant accidental
    if a:
        name = naturals[naturals.index(name[0]) + a[0][1]] + a[0][2] # replace
    return name + str(octave)

def is_note(string):
    '''Check if string is well-formed note'''
    note = re.compile('^[a-gA-G][#b]?([0]|[1-9][0-9]*)$')
    return re.match(note, string)

def gen_octave(base, start, end):
    '''Generate the tones to test from, using the C0-B0 octave as a starting point.
    Only the tones that match tones from the base octave supplied will be generated'''
    tones = []
    while start <= end: # while we haven't reached the last octave we want
        for note, freq in base:
            name, number = split(note)
            tones += [(name + str(number+start), freq*2**start)]
        start += 1
    return tones

def scale_dist(one, two):
    '''Returns how much higher note two is than note one in semitones'''
    # convert all flats to sharps for this
    if is_flat(one):
        one = sharp_flat(one)
    if is_flat(two):
        two = sharp_flat(two)

    # separate notes into their parts, e.g. A4, C4 = L1N1, L2N2
    (l1, n1), (l2, n2) = split(one), split(two)
    i1, i2 = scale.index(l1), scale.index(l2)
    
    letter_d = (i2 - i1) % len(scale) # distance of the letter portion of the notes
    # distance of the number portion: one octave for each difference of 1
    #   , fewer one octave when the notes span the gap between octaves (e.g. B4 to C5)
    number_d = len(scale) * (n2 - n1 - (i1 > i2)) # last part is a boolean evaluated to an int
    return letter_d + number_d


naturals_freq_l = filter(lambda n: '#' not in n[0], base_freq_l)
sharps_freq_l = filter(lambda n: '#' in n[0], base_freq_l) # only sharps
flats_freq_l = map(lambda n: (sharp_flat(n[0]), n[1]), sharps_freq_l) # only flats
