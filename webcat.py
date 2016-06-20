#
# -*- coding: UTF-8 -*-

import sys
from collections import defaultdict
from HTMLParser import HTMLParser
import requests
import json
import re


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)

        self.skip_tags = [u'script', u'style', u'figure']
        self.skip_words = self.read_unhelpful_words('unhelpful_words.dat')
        self.tag_type_stack = [] # keeps track of the tag_type ...
        self.word_histogram = {}
        self.total_words_analyzed = 0
        self.tags_seen = set()

        # TODO
        # if it looks plural, process the singular
        # https://pypi.python.org/pypi/inflect
        #
        # TODO
        # phrases like 'the left', 'the right' and winged derivatives.


    def filter(self, data, tag_type):
        val = []
        self.tags_seen.add(tag_type)
        if len(tag_type) == 0 or tag_type in self.skip_tags:
            return val

        adjusted_data = re.split('\W+', data.lower().strip())
        self.total_words_analyzed += len(adjusted_data)

        for s in adjusted_data:
            if len(s) < 2:
                continue
            if s in self.skip_words:
                continue
            val += [s]
        return val

    def read_unhelpful_words(self, file_name):
        with open(file_name) as f:
            data = json.loads(unicode(f.read()))
        meaningless_words = set()
        for pos in data:
            for w in data[pos]:
                meaningless_words.add(w)
        return meaningless_words


    ### tag handling
    def handle_starttag(self, tag, attrs):
        self.tag_type_stack += [tag]

    def handle_endtag(self, tag):
        self.tag_type_stack.pop()

    #### content_handlers, call filter(content)
    def handle_data(self, data):
        tag_type = u''
        if len(self.tag_type_stack) > 0:
            tag_type = self.tag_type_stack[-1]
        for s in self.filter(data, tag_type):
            if s not in self.word_histogram:
                self.word_histogram[s] = 1
            else:
                self.word_histogram[s] += 1


    def handle_comment(self, data):
        tag_type = u''
        if len(self.tag_type_stack) > 0:
            tag_type = self.tag_type_stack[-1]
        for s in self.filter(data, tag_type):
            if s not in self.word_histogram:
                self.word_histogram[s] = 1
            else:
                self.word_histogram[s] += 1

def is_int(x):
    try:
        y = int(x)
        return True
    except ValueError:
        return False

# actually, score_resource
def score_domain(domain, save_to_file = False):

    page = requests.get(domain)
    if save_to_file:
        with open(domain + '.txt', 'w') as f:
            f.write(page.content)
    parser = MyHTMLParser()
    try:
        parser.feed(page.content.decode('utf-8'))
    except UnicodeDecodeError as e:
        print '$exception'
        pass

    score_vector = []
    unique_words = 0
    for word in parser.word_histogram.keys():
        unique_words += parser.word_histogram[word]
        score_vector += [(parser.word_histogram[word], word)]

    return (sorted(score_vector, reverse=True), unique_words, parser.total_words_analyzed, parser.tags_seen)



shortcuts = {
    'so_1': 'http://stackoverflow.com/questions/9698614/super-raises-typeerror-must-be-type-not-classobj-for-new-style-class',
    'az': 'http://azspcs.net',
    'so_2' :  'http://stackoverflow.com/questions/5214578/python-print-string-to-text-file',
    'g': 'http://google.com',
    'phren': 'https://en.wikipedia.org/wiki/Phrenology',
    'reduct': 'https://en.wikipedia.org/wiki/Reductionism',
    'rickroll': 'https://en.wikipedia.org/wiki/Rickrolling',
    'comb': 'https://en.wikipedia.org/wiki/Combinatorics',
    'getty': 'https://en.wikipedia.org/wiki/Battle_of_Gettysburg',
    'orvis': 'http://www.orvis.com',
    'espn': 'http://espn.go.com/',
    '270': 'http://hosted.ap.org/dynamic/stories/U/US_CAMPAIGN_2016_ROAD_TO_270',
    'nra': 'http://www.cnn.com/2016/06/19/politics/donald-trump-chris-cox-nra-orlando-shooting/index.html'
}

verbose = True

if len(sys.argv) < 2:
    print u'usage: python {} uri|keyword'.format(sys.argv[0].split('/')[-1])
    print u'keywords in: {}'.format(','.join(shortcuts.keys()))
    exit(1)

for a in sys.argv[1:]:
    arg = a.lower()
    if arg in shortcuts:
        domain = shortcuts[arg].lower()
    else:
        domain = arg

    print 'Analyzing: ' + arg
    (score_vector, num_unique_words, num_analyzed_words, tags_seen) = score_domain(domain)

    if verbose:
        print u'tags seen: {}'.format(','.join(list(tags_seen)))
        P = 0.0
        idx = 1
        # non-unique words
        for (count, word) in filter(lambda (i, s): i > 1, score_vector):
            p = float(count)/num_unique_words
            P += p
            print u'{} : {}/{} ({:5.5}) [{}] "{}" {:5.5}'.format(idx, count, num_unique_words, p, int(10000*p), word, P).encode('utf-8'), word in domain
            idx += 1

        print u'{}: {} unique words, {} words analyzed, word set covers {:.3}%'.format(arg, num_unique_words, num_analyzed_words, 100*P)
        print 'Done'

