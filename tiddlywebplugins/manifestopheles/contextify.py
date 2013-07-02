"""
A TiddlyWeb renderer which marks up a manifesto
and friends.
"""

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
        return '<pre>\n%s\n</pre>' % tiddler.text

    def space_count(content):
        return content.count(' ')

    try:
        tiddler_titles = [btiddler.title.lower() for btiddler in
                store.list_bag_tiddlers(bag)]
    except AttributeError:
        tiddler_titles = [btiddler.title.lower() for
                btiddler in bag.list_tiddlers()]

    tiddler_titles.sort(key=space_count, reverse=True)

    try:
        tiddler_titles.remove(tiddler.title.lower())
    except ValueError:
        pass  # this tiddler not in titles

    text = tiddler.text

    # build the title regular expression
    pat = []
    for title in tiddler_titles:
        title = re.sub(r'\s+', r'\s+', title)
        pat.append(title)
    if pat:
        pat = '|'.join(pat)
        pat = r'\b(%s)\b' % pat
        pat = re.compile(pat, re.I)
        replace = r'<a title="\1" href="/manifestos/%s/\1">\1</a>' % manifesto

        output = pat.sub(replace, text)
    else:
        output = text

    def clean_attribute(match):
        attr = match.group(1)
        value = match.group(2)
        value = re.sub(r'\s+', ' ', value)
        if attr == 'href':
            value = urllib.quote(value.lower())
        return '%s="%s"' % (attr, value)

    output = re.sub(r'(title|href)="([^"]+)"', clean_attribute, output)

    http_linker_re = re.compile(r'(\s+)(http://[^\s]+?)(\s+|$)', re.I)
    http_linker_replace = r'\1<a title="\2" href="\2">\2</a>\3'
    output = http_linker_re.sub(http_linker_replace, output)

    return output
