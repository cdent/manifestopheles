"""
A TiddlyWeb renderer which marks up a manifesto
and friends.
"""

# XXX tiddlyweb 1.0

import re
import urllib

from tiddlyweb.model.bag import Bag
from tiddlyweb.store import NoBagError

def render(tiddler, environ):
    """
    Link found phrases to other tiddlers.
    """
    try:
        store = environ['tiddlyweb.store']
        manifesto = environ['tiddlyweb.manifesto']
        dictionary = environ['tiddlyweb.dictionary']
        bag = store.get(Bag(dictionary))
    except (KeyError, NoBagError):
        return '<pre>\n%s\n</pre>' % tiddler.txt

    def space_count(input):
        return input.count(' ')

    tiddler_titles = [btiddler.title.lower() for btiddler in store.list_bag_tiddlers(bag)]
    tiddler_titles.sort(key=space_count, reverse=True)

    try:
        tiddler_titles.remove(tiddler.title.lower())
    except ValueError:
        pass # this tiddler not in titles


    text = tiddler.text

    # build the regular expression
    pat = []
    for title in tiddler_titles:
        title = re.sub(r'\s+', r'\s+', title)
        pat.append(title)
    pat = '|'.join(pat)
    pat = r'\b(%s)\b' % pat
    pat = re.compile(pat, re.I)
    replace = r'<a title="\1" href="/manifestos/%s/\1">\1</a>' % manifesto

    output = pat.sub(replace, text)

    def clean_attribute(match):
        attr = match.group(1)
        value = match.group(2)
        value = re.sub('\s+', ' ', value)
        if attr == 'href':
            value = urllib.quote(value.lower())
        return '%s="%s"' % (attr, value)

    output = re.sub(r'(title|href)="([^"]+)"', clean_attribute, output)
    
    return output
