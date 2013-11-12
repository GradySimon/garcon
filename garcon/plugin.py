import functools, pkgutils, importlib


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
        plugin_package_names = [pkg[1] for pkg in pkgutils.walk_packages(self._plugin_path) if pkg[2]]
        imported_plugin_packages = [importlib.import_module(pkg) for pkg in plugin_package_names]
        self._active_agents = filter(is_agent, imported_plugin_packages)

    def get_active_agents(self):
        """
        Returns a set of the currently active plugins.
        """
        _refresh_plugin_set()
        return self._active_agents

    @staticmethod
    def _is_agent(plugin_package):
        """
        Returns True iff plugin_package is an agent plugin.

        For now, all plugins are agents, so this always returns True.
        """
        return True


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
