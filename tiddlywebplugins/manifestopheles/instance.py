
from tiddlywebplugins.instancer.util import get_tiddler_locations

store_contents = {}
store_structure = {}
store_structure['bags'] = {}

store_contents['static'] = [
        'file:static/feelies.js.tid',
        'file:static/feelies.css.tid',
        ]

store_structure['bags']['static'] = {
        'desc': 'static stuff',
        'policy': {
            'read': [],
            'write': ['R:ADMIN'],
            'create': ['R:ADMIN'],
            'delete': ['R:ADMIN'],
            'manage': ['R:ADMIN'],
            'owner': 'administrator',
            },
        }


instance_config = {
        'system_plugins': ['tiddlywebplugins.manifestopheles'],
        'twanager_plugins': ['tiddlywebplugins.manifestopheles'],
        }

