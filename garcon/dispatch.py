import logging

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
        logging.info("Dispatch received command '%s'. Looking for an agent who can handle it." % (command))
        logging.debug("Currently have %d agents." % (len(self._active_agents)))
        for agent in self._active_agents:
            if agent.can_handle(command):
                logging.info("Agent %s can handle command '%s', dispatching command to it." % (agent.name, command))
                agent.handle(command)
                return
        logging.info("Dispatch couldn't find an agent to handle command '%s'." % (command))
    
    def _refresh_agents(self):
        """
        Makes sure the _active_agents list is up to date.
        """
        active_agents = self._plugin_manager.get_active_agents()
        self._active_agents = sorted(active_agents)
