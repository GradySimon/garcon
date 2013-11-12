import os
import dispatch, plugin

def start():
    plugin_path = get_plugin_path()
    plugin_manager = plugin.PluginManager(plugin_path)
    dispatcher = dispatch.Dispatcher(plugin_manager)

def get_plugin_path():
    """
    Returns the path of the directory to look for plugins
    """
    path = os.path.join(os.environ['HOME'], ".garcon")
    os.makedirs(path, exist_ok=True)
    