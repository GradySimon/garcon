import os, logging
from garcon import dispatch, plugin, console


def start():
    prepare_directories()
    configure_logging(logging.DEBUG)
    plugin_path = get_plugin_path()
    plugin_manager = plugin.PluginManager(plugin_path)
    dispatcher = dispatch.Dispatcher(plugin_manager)
    console.accept_commands_forever(dispatcher)

def get_base_path():
    """
    Returns the base path for all garcon files
    """
    return os.path.join(os.environ['HOME'], ".garcon")

def get_plugin_path():
    """
    Returns the path of the plugin directory
    """
    return os.path.join(get_base_path(), "plugins")

def get_log_path():
    """
    Returns the path for the log file
    """
    return os.path.join(get_base_path(), "garcon.log")

def prepare_directories():
    prepare_base_directory()
    prepare_plugin_directory()

def prepare_base_directory():
    base_path = get_base_path()
    if not os.path.exists(base_path):
        logging.info("Base Garcon path doesn't yet exist. Creating it at %s" % (base_path))
        os.makedirs(base_path)

def prepare_plugin_directory():
    """
    Ensures the plugin path is created and ready for reading
    """
    plugin_path = get_plugin_path()
    if not os.path.exists(plugin_path):
        logging.info("Plugin path doesn't yet exist. Creating it at %s" % (plugin_path))
        os.makedirs(plugin_path)


def configure_logging(logging_level):
    logging.basicConfig(level=logging_level,
                        filename=get_log_path(),
                        format='%(levelname)s: %(asctime)s - %(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S')

if __name__ == '__main__':
    start()
