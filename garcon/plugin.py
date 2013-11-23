import os
import functools
import pkgutil
import importlib
import logging


class PluginManager:
    """
    Manages the set of installed plugins, providing other parts of the system
    with access to them.
    """

    def __init__(self, plugin_path):
        self._plugin_path = plugin_path
        self._refresh_plugin_set()

    def _refresh_plugin_set(self):
        """
        Checks disk to refresh the set of installed plugins.
        """
        plugin_package_names = [pkg[1] for pkg in
                                pkgutil.walk_packages([self._plugin_path])
                                if pkg[2]]
        loaded_plugins = set()
        for package_name in plugin_package_names:
            plugin_path = os.path.join(self._plugin_path, package_name,
                                                        "__init__.py")
            loader = importlib.machinery.SourceFileLoader(package_name,
                                                            plugin_path)
            loaded_plugins.add(loader.load_module())
            logging.info("Loaded plugin: %s" % package_name)
        self._active_agents = {agent.name: agent for agent in extract_agents(loaded_plugins)}
        self._active_services = {service.name: service for service in extract_services(loaded_plugins)}
        
    
    def get_active_agents(self):
        """
        Returns a set of the currently active plugins.
        """
        return self._active_agents.values()


def extract_services(plugins):
    """
    Returns all services found in any plugin in plugins
    """
    services = []
    for plugin in filter(has_services, plugins):
        services.extend(plugin.services)
    return services


def extract_agents(plugins):
    """
    Returns any agents found in any plugin in plugins
    """
    agents = []
    for plugin in filter(has_agents, plugins):
        agents.extend(plugin.agents)
    return agents


def has_agents(plugin_package):
    """
    Returns True iff plugin_package has any agents
    """
    return hasattr(plugin_package, "agents")


def has_services(plugin_package):
    """
    Returns True iff plugin_package has any has_services
    """
    return hasattr(plugin_package, "services")


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

class