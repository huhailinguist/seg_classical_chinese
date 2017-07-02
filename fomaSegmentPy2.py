'''
forward max match segmentation using foma python2

@author: Hai Hu
'''

from __future__ import print_function
import platform
import sys, codecs, re
import os

def escapeReservedChar(fn_wordlist):
    '''
    add "" around reserved symbols for foma

    e.g. * -> "*"

    All symbols in the ASCII range except [1-9A-Za-z'=] are reserved and need to be escaped
    https://github.com/jrwdunham/foma/blob/master/foma/README.symbols
    '''
    words = set()

    regex = [0] * 6
    regex[0] = re.compile(ur"([\u0000-\u0021])", re.UNICODE)
    regex[1] = re.compile(ur"([\u0023-\u0030])", re.UNICODE)  # quotation mark " is excluded here, which is \u0022
    regex[2] = re.compile(ur"([\u003A-\u0040])", re.UNICODE)
    regex[3] = re.compile(ur"([\u005B-\u0060])", re.UNICODE)
    regex[4] = re.compile(ur"([\u007B-\u00FF])", re.UNICODE)

    regex[5] = \
        re.compile(
            ur"([\u03A3\u03B5\u2192\u2194\u2200\u2203\u2205\u2208\u2218\u2225\u2227\u2228\u2229\u222A\u2264\u2265\u227A\u227B])",
            re.UNICODE)

    unwanted = re.compile(ur"([\u0000-\u001F])", re.UNICODE)

    with open(fn_wordlist, 'r') as f:
        for line in f:
            if line.strip() != '':
                #######################################################
                # now line is string
                line = line.rstrip('\n')  # only strip off \n, not \s

                # for quotation marks, add %, and then continue
                if "\"" in line:
                    line = line.replace("\"", "%\"")
                    words.add(line)
                    continue

                #######################################################
                # now line is utf-8 code points
                line = line.decode('utf-8')

                # skip space/tab; \u0009=\t, full-width space \u3000
                if line == u"\u0020" or line == u"\u3000" or line == u"\u0009":
                    print('\tspace/tab skipped!')
                    continue

                m = unwanted.match(line)  # unwanted are: <= \u0020
                if m:
                    continue

                # for other reserved symbols
                for reg in regex:
                    line = reg.sub(u'\u0022\g<1>\u0022', line)  # add "" around symbols like ! @ ...
                # print("here:", line)
                # print(line.encode('utf-8'))
                words.add(line.encode('utf-8'))
            else:
                print('\tempty line skipped!')

    return words


def convert(fn_wordlist):
    '''
    read in a word list, output .scr which is what foma needs to build FST
    '''
    # fileroot = fn_wordlist.replace('.txt', '')

    words = escapeReservedChar(fn_wordlist)
    words = list(words)

    print('number of unique words in total:', len(words))
    wordsStr = "|".join(words)

    # define words [these|are|chinese|words|separated|by|pipe];

    with open('tmp.scr', 'w') as out:
        # ? is the wildcat in foma regex
        out.write("define words [?|" + wordsStr + "];\n")
        out.write('regex words @> " " ... " " ;\n')  # one \s before and one \s after the word!
        out.write('save stack tmp.fst\n')
    print('done!\n')

def segmentPy(fn_fst, fn_text):
    '''using python API to foma to segment. Too slow'''
    print()
    fst = foma.read_binary(fn_fst)  # name of FST compiled using `foma -f tmp.src'
    fout = codecs.open(fn_text + '.seg', 'w', encoding='utf8')

    lst = []

    counter = 0
    with codecs.open(fn_text, encoding='utf8') as f:
        for line in f:
            counter += 1
            if counter % 1000 == 0:
                print(counter, '\n')
            line = line.rstrip()
            if line == '':
                fout.write('\n')
            else:
                for result in fst.apply_down(line):
                    # print(result)
                    # fout.write(result)
                    lst.append(result)
                # fout.write(' ')
                # fout.write('\n')
                lst.append('\n')

    fout.close()

def main():
    # check OS
    print('OS:', platform.system())
    os_name = platform.system()
    # output:
    # - ubuntu: Linux
    # - mac: Darwin
    # - win: Windows
    if os_name == 'Linux':
        foma_filename = './foma/linux-x86_64/foma'
    elif os_name == 'Darwin':
        foma_filename = './foma/OSX/foma'
    elif os_name == 'Windows':
        os.system("CHCP 65001") # enabling printing utf8 file in cmd
        foma_filename = '.\\foma\\win32\\foma'
    else:
        print('OS is:', os_name, 'It is unsupported!')
        exit(1)

    # do the real work
    fn_wordlist = sys.argv[1]
    fn_text = sys.argv[2]

    # STEP 1
    print('\nSTEP 1: converting the word list to what foma wants ...\n')
    convert(fn_wordlist)

    # STEP 2
    print('STEP 2: compiling FST machine ...\n')
    if os_name != 'Windows':
        os.system(foma_filename + " -f tmp.scr")
    else:
        os.system(foma_filename + " -f tmp.scr")
    print('done!')

    # STEP 3
    print('\n\nSTEP 3: segmentation\n')
    # segmentPy('tmp.fst', fn_text)
    if os_name == 'Darwin':
        os.system("./segment_mac tmp.fst " + fn_text)
    elif os_name == 'Linux':
        os.system("./segment_linux tmp.fst " + fn_text)
    else:
        print('os not supported now')
    # TODO windows

    # clean up
    os.system("rm tmp.scr")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python fomaSegmentPy2.py fn_wordlist fn_text')
        exit(1)
    else:
        main()

