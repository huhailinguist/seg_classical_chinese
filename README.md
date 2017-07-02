# Maximum Match Segmentation Using Foma
Hai Hu, Lwin Moe

It is originally written by Lwin Moe to do segmentation in Burmese. (see https://github.com/lwinmoe)
I adapted it to Chinese segmentation. 

## How to run
On mac and linux systems, open terminal and run:
```
python2 fomaSegmentPy2.py fn_wordlist fn_text
```
where fn_wordlist is the word list, fn_text is the text to be segmented.

To test, you can run:
```
python2 fomaSegmentPy2.py ancient_words_clean.dic test2.txt
```
where ancient_words_clean.dic is the test dictionary and test2.txt is some test text file.


## How it works
This little program will do maximum matching segmentation using the foma library which is a finite-state machine library for morphological analysis. 

More info about foma: https://fomafst.github.io/

STEP 1:
Convert the dictionary to a format that foma can read.

STEP 2:
Compile the finite-state machine using foma, this will result in tmp.fst

STEP 3:
Segmentation. This calls the executable `segment_mac' or `segment_linux', which has been compiled on mac os and linux separately, source code of segment can be found in ./src.
The segmented file will be saved to 'output.txt'
