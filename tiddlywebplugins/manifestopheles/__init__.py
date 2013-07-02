"""
A manifesto contextualizer.
"""

import urllib

from httpexceptor import HTTP404

from tiddlyweb.manage import make_command, usage
from tiddlyweb.model.recipe import Recipe
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.store import NoRecipeError, NoTiddlerError
from tiddlyweb.util import merge_config
from tiddlyweb.web.util import get_route_value
from tiddlyweb.wikitext import render_wikitext

from tiddlywebplugins.templates import get_template
from tiddlywebplugins.utils import do_html, get_store, ensure_bag

from tiddlywebplugins.manifestopheles.config import config as twmconfig


def init(config):
    merge_config(config, twmconfig)
    if 'selector' in config:
        config['selector'].add('/', GET=home)
        config['selector'].add('/manifestos', GET=manifestos)
        config['selector'].add('/manifestos/{manifesto_name:segment}',
                GET=manifestor)
        config['selector'].add(
                '/manifestos/{manifesto_name:segment}/{definition:segment}',
                GET=definition)
    config['wikitext.default_renderer'] = (
            'tiddlywebplugins.manifestopheles.contextify')

    @make_command()
    def manifest(args):
        """Make a new manifesto. <manifesto name> <dictionary prefix>"""
        store = get_store(config)
        try:
            recipe_name = args[0]
            bag_name = args[1] + '-dictionary'
        except IndexError:
            usage("manifesto name and dictionary prefix required")
        # add policy info later
        ensure_bag(recipe_name, store)
        ensure_bag(bag_name, store)
        recipe = Recipe(recipe_name)
        recipe.set_recipe([
            (bag_name, ''),
            (recipe_name, '')])
        recipe = store.put(recipe)


def home(environ, start_response):
    pass


@do_html()
def manifestos(environ, start_response):
    store = environ['tiddlyweb.store']
    recipes = store.list_recipes()
    template = get_template(environ, 'list.html')
    return template.generate(recipes=recipes)


@do_html()
def manifestor(environ, start_response):
    store = environ['tiddlyweb.store']
    manifesto = environ['wsgiorg.routing_args'][1]['manifesto_name']
    manifesto = urllib.unquote(manifesto).decode('utf-8')

    try:
        recipe = Recipe(manifesto)
        recipe = store.get(recipe)
    except NoRecipeError, exc:
        raise HTTP404('no such manifesto: %s' % exc)

    manifesto_bag, _ = recipe.get_recipe()[-1]

    tiddler = Tiddler('manifesto', manifesto_bag)
    try:
        tiddler = store.get(tiddler)
    except NoTiddlerError:
        pass

    dictionary_bag = None
    for bag, filter in recipe.get_recipe():
        if bag.endswith('-dictionary'):
            dictionary_bag = bag
            break

    environ['tiddlyweb.manifesto'] = manifesto
    environ['tiddlyweb.dictionary'] = dictionary_bag
    output = render_wikitext(tiddler, environ)

    if output == '':
        output = 'Pontificate!'

    template = get_template(environ, 'display.html')
    return template.generate(weAuthed='hi', tiddler='manifesto',
            dictionary=dictionary_bag, bag=manifesto_bag, title=manifesto,
            output=output)


@do_html()
def definition(environ, start_response):
    store = environ['tiddlyweb.store']
    manifesto = get_route_value(environ, 'manifesto_name')
    definition = get_route_value(environ, 'definition')

    try:
        recipe = Recipe(manifesto)
        recipe = store.get(recipe)
    except NoRecipeError, exc:
        raise HTTP404('no such manifesto: %s' % exc)

    kept_bag = None
    for bag, filter in recipe.get_recipe():
        if bag.endswith('-dictionary'):
            kept_bag = bag
            break

    tiddler = Tiddler(definition, kept_bag)
    try:
        tiddler = store.get(tiddler)
    except NoTiddlerError:
        pass

    environ['tiddlyweb.manifesto'] = manifesto
    environ['tiddlyweb.dictionary'] = kept_bag
    output = render_wikitext(tiddler, environ)

    if output == '':
        output = 'Pontificate!'

    template = get_template(environ, 'display.html')
    return template.generate(weAuthed='hi', tiddler=definition, bag=kept_bag,
            dictionary=kept_bag, title=manifesto, output=output)
