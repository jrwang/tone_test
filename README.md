#ToneTest

ToneTest is a small app for quizzing frequencies or note names.

## Getting Started

### Install Tkinter

If you already have python-tk, you're fine. Otherwise:
```bash
sudo apt-get install python-tk
```

### Install Snack

Snack is a sound package for TKinter. Download Snack [here](www.speech.kth.se/snack/)

## Usage
Quick demo:
```bash
python test.py 
```

Test note names instead of frequencies
```bash
python test.py --names
```

Test 20 questions instead of the default (10) and with no sharps or no flats
```bash
python test.py -q 20 --nosharps --noflats
```

Test notes from the C5-B6 octaves instead of the default (C4-B4)
```bash
python test.py --octaves 5 6
```

