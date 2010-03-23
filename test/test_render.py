"""
Our default renderer takes content that is
expected to be plain text and for titles in
a given bag, links to those titles.
"""

import shutil

from tiddlyweb.model.bag import Bag
from tiddlyweb.model.recipe import Recipe
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.config import config
from tiddlywebplugins.manifestopheles.contextify import render
from tiddlywebplugins.utils import get_store

def setup_module(module):

    try:
        shutil.rmtree('store')
    except:
        pass

    store = get_store(config)
    bag = Bag('devil-dictionary')
    store.put(bag)
    bag = Bag('x-manifesto')
    store.put(bag)
    recipe = Recipe('devil')
    recipe.set_recipe([
        ('devil-dictionary', ''),
        ('x-manifesto', ''),
        ])
    store.put(recipe)
    tiddler = Tiddler('fancy', 'devil-dictionary')
    store.put(tiddler)
    tiddler = Tiddler('house car', 'devil-dictionary')
    store.put(tiddler)
    tiddler = Tiddler('car', 'devil-dictionary')
    store.put(tiddler)
    tiddler = Tiddler('The Truth', 'x-manifesto')
    tiddler.text = """
I was walking and spied something fancy.

Truth is, I thought it was a house car,
but it turns out I was wrong.

It was a
      house
         car!

Which is way more fancy.
"""
    store.put(tiddler)


def test_simple():
    store = get_store(config)
    environ = {
            'tiddlyweb.usersign': {'name': 'devil', 'roles': []},
            'tiddlyweb.store': store,
            'tiddlyweb.manifesto': 'devil',
            'tiddlyweb.dictionary': 'devil-dictionary',
            }
    tiddler = store.get(Tiddler('The Truth', 'x-manifesto'))
    output = render(tiddler, environ)

    assert 'something <a title="fancy" href="/manifestos/devil/fancy">fancy</a>.' in output
    assert 'a <a title="house car" href="/manifestos/devil/house%20car">house car</a>,' in output


