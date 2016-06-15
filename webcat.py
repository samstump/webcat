from HTMLParser import HTMLParser
import requests

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tag_types = []
        self.skip_tags = ['script', 'style']
        self.remove_chars = "'" + '"()[]<>,.+@|:-=#!?'
        self.data = []

    def clean(self, txt):
        return txt.translate(None, self.remove_chars).lower()

    def handle_starttag(self, tag, attrs):
        self.tag_types += [tag]

    def handle_endtag(self, tag):
        self.tag_types.pop()

    def handle_data(self, data):
        tag_type = ''
        if len(self.tag_types) > 0:
            tag_type = self.tag_types[-1]
        if tag_type not in self.skip_tags:
            s = self.clean(data)
            if len(s) > 0:
                self.data += [s]

    def handle_comment(self, data):
        tag_type = ''
        if len(self.tag_types) > 0:
            tag_type = self.tag_types[-1]
        if tag_type not in self.skip_tags:
            s = self.clean(data)
            if len(s) > 0:
                self.data += [s]


def is_int(x):
    try:
        y = int(x)
        return True
    except ValueError:
        return False


print 'requesting...'
domains = [
    'http://stackoverflow.com/questions/9698614/super-raises-typeerror-must-be-type-not-classobj-for-new-style-class',
    'http://azspcs.net',
    'http://stackoverflow.com/questions/5214578/python-print-string-to-text-file',
    'http://google.com',
    'https://en.wikipedia.org/wiki/Phrenology',
    'https://en.wikipedia.org/wiki/Reductionism',
    'https://en.wikipedia.org/wiki/Rickrolling'
]


skip_words = set([
    'up', 'down', 'left', 'right', 'at', 'of', 'to', 'from', 'in', 'for', 'with', 'as', 'about', 'only', 'by',
    'above', 'below', 'on', 'also',
    'and', 'or', 'not', 'but','just', 'more', 'less',
    'a', 'an', 'the', 'this', 'that',
    'is', 'are', 'be', 'can', 'should', 'must', 'does', 'do', 'may', 'was', 'were', 'had', 'have',
    'who', 'what', 'when', 'how', 'why', 'which', 'whether', 'where', 'while', 'would', 'should', 'could',
    'i', 'me', 'you', 'he', 'she', 'it', 'we', 'they', 'them', 'your', 'my', 'his', 'her', 'its',
])

page = requests.get(domains[6])
print 'done, got page'
print 'saving ...'
with open('sample.response.txt', 'w') as f:
    f.write(page.content)

print 'parsing...'
parser = MyHTMLParser()
parser.feed(page.content)

dict = {}
for s in parser.data:
    for w in s.split():
        if w in skip_words:
            continue
        if len(w) == 1:
            continue
        if is_int(w):
            continue
        if w not in dict:
            dict[w] = 1
        else:
            dict[w] += 1

zzz = []
sum = 0
for s in dict:
    zzz += [(dict[s], s)]
    sum += dict[s]

for (num, val) in sorted(zzz, reverse=True):
    print num, round(100*num/float(sum),2), val