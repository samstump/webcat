import requests
import re
import json

pronouns = set([
    'I', 'me', 'my', 'mine', 'myself',
    'you', 'you', 'your', 'yours', 'yourself',
    'he', 'him', 'his', 'his', 'himself',
    'she', 'her', 'her', 'hers', 'herself',
    'it', 'it', 'its', 'itself',
    'we', 'us', 'our', 'ours', 'ourselves',
    'you', 'you', 'your', 'yours', 'yourselves',
    'they', 'them', 'their', 'theirs', 'themselves'
])

state_of_being_verbs = set([
    'be', 'is', 'am', 'are', 'was', 'were', 'will', 'would', 'can',
    'could', 'shall', 'should', 'may', 'might', 'must', 'have', 'has',
    'had', 'do', 'did', 'does', 'being', 'having', 'doing'
])

def get_prepositions():
    domains = [
        (
            'wikipedia',
            'https://en.wikipedia.org/wiki/List_of_English_prepositions',
            '<li><a href="//en.wiktionary.org/wiki/.*">(.*)</a></li>'
        ),
#      (
#            'wiktionary',
#            'https://en.wiktionary.org/wiki/Category:English_prepositions',
#           '<li><a href="/wiki/.*">(.*)</a></li>'
#       )
]

    prepositions = set()
    for (title, domain, regex_str) in domains:
        print 'scanning: ' + title + '...'
        page = requests.get(domain)
        result = re.findall(regex_str, page.content.decode('utf-8'))
        for r in result:
            if len(r.split()) == 1:
                prepositions.add(r)
            else:
                for x in r.split():
                    prepositions.add(x)
        print 'done'
    return prepositions

speech = {
    "pronouns" : map(lambda x: unicode(x), pronouns),
    "state_of_being_verbs" : map(lambda x: unicode(x), state_of_being_verbs),
    "prepositions" : map(lambda x: unicode(x), get_prepositions()),
    "articles" : map(lambda x: unicode(x), ['an', 'the', 'a']),
    "conjunctions": map(lambda x: unicode(x), ['and', 'but', 'or', 'nor', 'this', 'that', 'not']),
    "questioning": map(lambda x: unicode(x), ['who', 'what', 'when', 'where', 'why', 'how', 'which'])
}

file_name = 'bad_words'


with open(file_name, 'w') as f:
    f.write(json.dumps(speech, indent=4, separators=(',',': ')))
'''
with open(file_name) as f:
    data = json.loads(f.read())

meaningless_words = set()
for pos in data:
#    print pos
    for w in data[pos]:
        meaningless_words.add(w)

for w in meaningless_words:
    print w
'''
