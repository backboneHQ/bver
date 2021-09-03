class SoftwareNotFoundError(Exception):
    """Software not found error."""

class AddonNotFoundError(Exception):
    """Addon not found error."""

class Query(object):
    """
    Queries softwares and addons.
    """

    def __init__(self, softwares):
        """Create a query object."""
        self.__setSoftwares(softwares)

    def softwares(self):
        """Return a list of softwares used for queries."""
        return self.__softwares

    def softwareNames(self):
        """
        Return a list of software names.
        """
        return list(map(lambda x: x.name(), self.softwares()))

    def softwareBverNames(self):
        """
        Return a list of software bver names.
        """
        return list(map(lambda x: x.bverName(), self.softwares()))

    def addonNames(self):
        """
        Return a list of all addon names among the softwares.
        """
        result = set()

        for software in self.softwares():
            for addonName in software.addonNames():
                result.add(addonName)

        return list(result)

    def addonBverNames(self):
        """
        Return a list of all addon bver names among the softwares.
        """
        result = set()

        for software in self.softwares():
            for addon in map(lambda x: software.addon(x), software.addonNames()):
                result.add(addon.bverName())

        return list(result)

    def softwareByName(self, name):
        """
        Return a software instance based on software's name.
        """
        for software in self.softwares():
            if name == software.name():
                return software

        raise SoftwareNotFoundError(
            'Could not find software "{0}"'.format(name)
        )

    def softwareByBverName(self, bverName):
        """
        Return a software instance based on software's bver name.
        """
        for software in self.softwares():
            if bverName == software.bverName():
                return software

        raise SoftwareNotFoundError(
            'Could not find software "{0}"'.format(bverName)
        )

    def softwaresByAddonName(self, name):
        """
        Return a list of software instances based on addon's name.
        """
        result = []
        for software in self.softwares():
            if name in software.addonNames():
                result.append(software)

        if not result:
            raise AddonNotFoundError(
                'Could not find any software with addon "{0}"'.format(name)
            )

        return result

    def softwaresByAddonBverName(self, bverName):
        """
        Return a list of software instances based on addon's bver name.
        """
        result = []
        for software in self.softwares():
            for addon in map(lambda x: software.addon(x), software.addonNames()):
                if addon.bverName() == bverName:
                    result.append(software)

        if not result:
            raise AddonNotFoundError(
                'Could not find any software with addon "{0}"'.format(bverName)
            )

        return result

    def __setSoftwares(self, softwares):
        """Set a list of softwares that should be used by the query."""
        assert isinstance(softwares, list), "Unexcepted type!"

        self.__softwares = softwares
