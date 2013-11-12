class Dispatcher:
    """
    Accepts commands from the user, dispatches them to the appropriate plugin.
    """

    def __init__(self, plugin_manager):
        self._plugin_manager = plugin_manager
        self._refresh_agents()

    def dispatch(self, command):
        """
        Dispatches the command to the lowest priority plugin that can handle __init__.
        """
        for agent in self._active_agents:
            if agent.can_handle(command):
                agent.handle(command)
    
    def _refresh_agents(self):
        """
        Makes sure the _active_agents PriorityQueue is up to date.
        """
        active_agents = self._plugin_manager.get_active_agents()
        self._active_agents = sorted(active_agents)
