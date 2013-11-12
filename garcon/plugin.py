import functools, pkgutil, importlib, logging


class PluginManager:
    """
    Manages the set of installed plugins, providing other parts of the system with access to them.
    """

    def __init__(self, plugin_path):
        self._plugin_path = plugin_path
        self._refresh_plugin_set()


    def _refresh_plugin_set(self):
        """
        Checks disk to refresh the set of installed plugins.
        """
        plugin_package_names = [pkg[1] for pkg in pkgutil.walk_packages([self._plugin_path]) if pkg[2]]
        loaded_plugins = set()
        for package_name in plugin_package_names:
            loaded_plugins.add(importlib.import_module(package_name))
            logging.info("Loaded plugin: %s" % package_name)
        self._active_agents = filter(is_agent, loaded_plugins)

    def get_active_agents(self):
        """
        Returns a set of the currently active plugins.
        """
        return self._active_agents


@functools.total_ordering
class AgentBase:
    """
    The base class for all agents.
    """
    
    # The default priority
    priority = 4

    # Agents should be sorted by priority
    def __eq__(self, other):
        return self.priority == other.priority

    def __lt__(self, other):
        return self.priority < other.priority


def is_agent(plugin_package):
    """
    Returns True iff plugin_package is an agent plug
    For now, all plugins are agents, so this always returns True.
    """
    return True