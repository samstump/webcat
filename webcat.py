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

print 'requesting...'
domains = [
    'http://stackoverflow.com/questions/9698614/super-raises-typeerror-must-be-type-not-classobj-for-new-style-class',
    'http://azspcs.net',
    'http://stackoverflow.com/questions/5214578/python-print-string-to-text-file',
    'http://google.com'
]

skip_words = [
    'up', 'down', 'left', 'right'
]

page = requests.get(domains[0])
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
        if w not in dict:
            dict[w] = 1
        else:
            dict[w] += 1

zzz = []
for s in dict:
    zzz += [(dict[s], s)]

for x in sorted(zzz, reverse=True):
    print x