import re


def main():
    line = 'I think i understand regular expressions'

    match_result = re.match(r'think', line, re.M|re.I)
    if match_result:
        print('Match found:' + match_result.group())
    else:
        print('No match was found!')

    search_result = re.search(r'think', line, re.M|re.I)
    if search_result:
        print('Search found: ' + search_result.group())
    else:
        print('Nothing found in search!')


if __name__ == '__main__':
    main()

