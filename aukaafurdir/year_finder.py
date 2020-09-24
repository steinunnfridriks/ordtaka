# tuple með orði + ári og freqdic á tíðnina á hverju tuple. finna þannig hvort notkun orðana er meiri fyrir eða eftir einhvern ákveðinn tíma

from rmh_extractor import RmhWord, RmhExtractor
from string import punctuation
import argparse
import xml.etree.ElementTree as ET
import glob
import matplotlib
import matplotlib.pyplot as plt

# In the command line, a target word needs to be specified (the word to be examined)
parser = argparse.ArgumentParser()
parser.add_argument('targetword', nargs='+')
#parser.add_argument('targetword')
args = parser.parse_args()

# Choose which folder to examine (if not all)
xml_files = glob.glob(f'../../corpora/CC_BY/**/**/*.xml', recursive=True)

freqdic = {}
i = 1
for file in xml_files:
    with open(file, 'r', encoding='utf-8') as content:
        try:
            tree = ET.parse(content)
            root = tree.getroot()   
            if 'date' in str(root[0][0][3][0][0][1]):             # when there's an author, the year will be one place later
                year = root[0][0][3][0][0][1].text[:4]
            else:
                year = root[0][0][3][0][0][2].text[:4]
            for word in tree.iter():
                lemma = word.attrib.get('lemma')
                for tw in args.targetword:
                    if lemma == tw:
                        if (lemma,year) not in freqdic:
                            freqdic[(lemma,year)] = 1       # The dictionary keys are tuples indicating the target word lemma and year, the values are the frequencies
                        else:
                            freqdic[(lemma,year)] += 1
        except ET.ParseError:   # Skip errors that occur in the xml files
            continue
        except IndexError:
            continue

        print(f'Files processed: {i} of {len(xml_files)}')
        print(file)
        i += 1

for key, value in sorted(freqdic.items()):
    print(key,value)

years = []
freqs = []
for tw in args.targetword:
    temp_year = []
    temp_freq = []
    for key, value in sorted(freqdic.items()):
        if any(i.isdigit() for i in key[1]) :   # make sure no accidental wordstring gets passed as a year
            if tw == key[0]:
                if int(key[1]) > 1950:   # If the frequency is from a year earlier than 1950, skip it
                    temp_year.append(key[1])
                    temp_freq.append(value)
    years.append(temp_year)
    freqs.append(temp_freq)

# Plot the resulting data as line plots
x = 0
while x < len(years):
    fig, ax = plt.subplots()
    ax.plot(years[x], freqs[x])
    ax.tick_params(axis="x", labelsize=5)
    ax.tick_params(axis="y", labelsize=5)

    ax.set(xlabel='ár', ylabel='tíðni', title='Tíðni orðsins "'+args.targetword[x]+'" eftir árum')
    ax.grid()

    fig.savefig(args.targetword[x]+"freq.png")
    plt.show()
    x+=1