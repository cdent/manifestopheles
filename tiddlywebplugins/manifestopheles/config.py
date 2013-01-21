from tiddlywebplugins.instancer.util import get_tiddler_locations

from tiddlywebplugins.manifestopheles.instance import store_contents

config = {
        'instance_tiddlers': get_tiddler_locations(store_contents,
            'tiddlywebplugins.manifestopheles'),
}
