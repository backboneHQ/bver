from .Versioned import Versioned
from .Addon import Addon

class InvalidAddonError(Exception):
    """Invalid addon error."""

class Software(Versioned):
    """
    Implements software support to the versioned.
    """

    def __init__(self, *args, **kwargs):
        """
        Create a software object.
        """
        super(Software, self).__init__(*args, **kwargs)

        self.__addons = {}

    def addAddon(self, addon):
        """
        Add an addon to the software.
        """
        assert isinstance(addon, Addon), "Invalid addon type!"

        self.__addons[addon.name()] = addon

    def addon(self, name):
        """
        Return an addon object.
        """
        if name not in self.__addons:
            raise InvalidAddonError('Invalid addon "{0}"'.format(name))

        return self.__addons[name]

    def addonNames(self):
        """
        Return a list of addon names.
        """
        return self.__addons.keys()

    def bverName(self, addon=None):
        """
        Return the environment variable name of the versioned.
        """
        if addon:
            assert isinstance(addon, Addon), "Invalid addon type!"
            return Versioned.toBverName(self.name(), addon.name())

        return Versioned.toBverName(self.name())
