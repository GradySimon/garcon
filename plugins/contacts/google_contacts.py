import garcon.plugin


class GoogleContactsService(garcon.plugin.ServiceBase):

    def get_contact_methods(self, contact_name):
        """
        Returns a dict of {contact_method_name: contact_method_address}
        """
        pass
        # Stupid Google and their stupid not suporting Python 3. 
