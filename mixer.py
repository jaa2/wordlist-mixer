""" Wordlist Mixer by jaa2
    https://github.com/jaa2/wordlist-mixer """

import argparse
import itertools
import sys

def read_all_lines(fname):
    with open(fname, "r") as f:
        content = f.read().splitlines()
    return content

def main(args):
    # Read word lists
    wlists = []
    for wordlist in args.wordlists:
        this_list = read_all_lines(wordlist)
        wlists.append(this_list)
    
    # Read formats
    if args.formatfile is not None:
        formats = [[int(num) for num in line]
                    for line in read_all_lines(args.formatfile)]
    elif args.permuteall:
        formats = itertools.permutations(range(1, len(wlists) + 1))
    else:
        formats = [range(1, len(wlists) + 1)]
    
    # Form the wordlists
    f = open(args.out, "w") if args.out is not None else sys.stdout
    for format_ in formats:
        # Decrease by 1
        format_f = [x - 1 for x in format_]
        if any([x < 0 or x >= len(wlists) for x in format_f]):
            print("Error in format '{}': digit outside the range of 1-{}"
                .format(''.join([str(num) for num in format_]), len(wlists)))
            exit(1)
        lists = [wlists[num] for num in format_f]
        for tup in itertools.product(*lists):
            f.write("".join(tup) + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wordlist mixer")
    parser.add_argument("--out", "-o", help="Output file")
    parser.add_argument("--formatfile", "-ff",
        help="Format file (with 123, 122, 311, etc. on each line)")
    parser.add_argument("--permuteall", action="store_true",
        help="If no format file is provided, the format will be permuted, "
            + "resulting in many more combinations.")
    parser.add_argument("wordlists", nargs="+", help="Input wordlists")
    
    args = parser.parse_args()
    main(args)
