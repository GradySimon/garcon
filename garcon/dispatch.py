from Queue import PriorityQueue


class Dispatcher:
    """
    Accepts commands from the user, dispatches them to the appropriate plugin.
    """

    def __init__(self, plugin_manager):
        self._plugin_manager = plugin_manager
        _refresh_plugins()

    def dispatch(self, command):
        """
        Dispatches the command to the lowest priority plugin that can handle __init__.
        """
        for agent in _active_agents:
            if agent.can_handle(command):
                agent.handle(command)
    
    def _refresh_plugins(self):
        """
        Makes sure the _active_agents PriorityQueue is up to date.
        """
        active_plugins = self._plugin_manager.get_active_agents()
        self._active_plugins = PriorityQueue(self._plugin_manager)
