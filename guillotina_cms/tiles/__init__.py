

# from guillotina.configure import _base_decorator
from guillotina.configure import register_configuration_handler


def load_tiletype(_context, tile):
    config = tile['config']
    app_settings['available_tiles'][config['name']] = {
        'title': config['title'],
        'name': config['name'],
        'add_permission': config['add_permission'],
        'view_permission': config['view_permission'],
        'edit_permission': config['edit_permission'],
        'description': config['description'],
        'icon': config['icon'],
        'schema': config['schema']
    }
register_configuration_handler('tile', load_tiletype) # noqa


# class tilestype(_base_decorator):  # noqa: N801
#    configuration_type = 'contenttype'
