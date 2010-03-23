"""
A TiddlyWeb renderer which marks up a manifesto
and friends.
"""

# XXX tiddlyweb 1.0

import re
import urllib

from tiddlyweb.model.bag import Bag

def render(tiddler, environ):
    """
    Link found phrases to other tiddlers.
    """
    store = environ['tiddlyweb.store']
    manifesto = environ['tiddlyweb.manifesto']
    bag = store.get(Bag(environ['tiddlyweb.dictionary']))

    def space_count(input):
        return input.count(' ')

    tiddler_titles = [btiddler.title for btiddler in bag.gen_tiddlers()]
    tiddler_titles.sort(key=space_count, reverse=True)

    text = tiddler.text

    # build the regular expression
    pat = []
    for title in tiddler_titles:
        title = re.sub(r'\s+', r'\s+', title)
        pat.append(title)
    pat = '|'.join(pat)
    pat = r'\b(%s)\b' % pat
    replace = r'<a title="\1" href="/manifestos/%s/\1">\1</a>' % manifesto

    output = re.sub(pat, replace, text)

    def clean_attribute(match):
        attr = match.group(1)
        value = match.group(2)
        value = re.sub('\s+', ' ', value)
        if attr == 'href':
            value = urllib.quote(value)
        return '%s="%s"' % (attr, value)

    output = re.sub(r'(title|href)="([^"]+)"', clean_attribute, output)
    
    return output
