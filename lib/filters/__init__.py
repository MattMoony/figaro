"""Home of the filter manager"""

import os
from yapsy.PluginInfo import PluginInfo
from yapsy.PluginManager import PluginManager
from typing import List

from lib import params
from lib.filters.filter import Filter

"""The manager for all Figaro filters"""
manager: PluginManager = PluginManager()
"""The path to all Figaro filters"""
fpath: str = os.path.join(params.BPATH, 'res', 'filters')

manager.setPluginPlaces([fpath])
manager.setCategoriesFilter({
    'Filter': Filter,
})

def get(name: str, category: str = 'Filter') -> PluginInfo:
    return manager.getPluginByName(name, category)

def get_all() -> List[PluginInfo]:
    manager.collectPlugins()
    return manager.getAllPlugins()

def get_names() -> List[str]:
    manager.collectPlugins()
    return list(map(lambda p: type(p.plugin_object).__name__, manager.getAllPlugins()))