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
        self._agents = []
        self._services = []

    def initialize(self, app):
        self.app = app
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
            plugin_path = os.path.join(self._plugin_path, package_name, "__init__.py")
            loader = importlib.machinery.SourceFileLoader(package_name, plugin_path)
            loaded_plugins.add(loader.load_module())
            logging.info("Loaded plugin: %s" % package_name)
        agent_classes = _extract_agents(loaded_plugins)
        service_classes = _extract_services(loaded_plugins)
        self._agents = {agent.name: self._wrap_agent(agent) for agent in agent_classes}
        self._services = {service.name: self._wrap_service(service) for service in service_classes}

    def get_active_agents(self):
        """
        Returns a set of the currently active plugins.
        """
        return [agent.get_instance() for agent in self._agents.values()]

    def get_dispatcher(self):
        return self.app.dispatcher

    def _wrap_agent(self, agent_class):
        return _Agent(agent_class, self)

    def _wrap_service(self, service_class):
        return None


def _extract_services(plugins):
    """
    Returns all services found in any plugin in plugins
    """
    services = []
    for plugin in filter(_has_services, plugins):
        services.extend(plugin.services)
    return services


def _extract_agents(plugins):
    """
    Returns any agents found in any plugin in plugins
    """
    agents = []
    for plugin in filter(_has_agents, plugins):
        agents.extend(plugin.agents)
    return agents


def _has_agents(plugin_package):
    """
    Returns True iff plugin_package has any agents
    """
    return hasattr(plugin_package, "agents")


def _has_services(plugin_package):
    """
    Returns True iff plugin_package has any has_services
    """
    return hasattr(plugin_package, "services")


class _Agent:
    """
    Internal class that represents a single agent.
    """
    def __init__(self, agent_class, plugin_manager):
        self.agent_class = agent_class
        self.plugin_manager = plugin_manager
        self.active_instance = None

    def get_instance(self):
        if self.active_instance is None:
            self._instantiate()
        return self.active_instance

    def _instantiate(self):
        logging.debug("Instantiating agent: %s" % (str(self.agent_class)))
        self.active_instance = self.agent_class(self.plugin_manager)


@functools.total_ordering
class AgentBase():
    """
    The base class for all agents.
    """

    # The default priority
    priority = 4

    def __init__(self, plugin_manager):
        self.plugin_manager = plugin_manager

    # Agents should be sorted by priority
    def __eq__(self, other):
        return self.priority == other.priority

    def __lt__(self, other):
        return self.priority < other.priority


class ServiceBase():
    """
    The base class for all services.
    """
    pass
