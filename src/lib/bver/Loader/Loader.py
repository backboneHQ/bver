from ..Versioned import Versioned
from ..Versioned import Software
from ..Versioned import Addon

class AddonNotFoundError(Exception):
    """Addon not found in the softwares error."""

class Loader(object):
    """
    Abstract loader.

    Returns a list of software instances based on the addon and software
    information (@see softwares)
    """

    def __init__(self):
        """
        Create a software.
        """
        self.__softwares = {}
        self.__addons = {}

    def addSoftwareInfo(self, softwareName, version, options={}):
        """
        Add an addon to a specific software.
        """
        assert isinstance(options, dict), \
            'options need to be a dictionary'

        self.__softwares[softwareName] = {
            'version': version,
            'options': dict(options)
        }

    def addAddonInfo(self, softwareName, addonName, options={}):
        """
        Add an addon to a specific software.
        """
        assert isinstance(options, dict), \
            'options need to be a dictionary'

        if softwareName not in self.__addons:
            self.__addons[softwareName] = {}

        self.__addons[softwareName][addonName] = {
            'options': dict(options)
        }

    def softwares(self, env={}):
        """
        Return a list of softwares based on the added software/addon info.

        In case there is a version assigned in the input environment, it's
        going to use that instead of the parsed version. The version
        in the input env needs to be defined following {@link versioned.bverName}.
        """
        # now creating softwares
        result = []
        for softwareName in self.__softwares.keys():
            softwareVersion = self.__softwareVersion(softwareName, env)
            softwareOptions = self.__softwares[softwareName]['options']

            # creating a software instance
            software = Software(
                softwareName,
                softwareVersion
            )

            # setting software options
            self.__setVersionedOptions(software, softwareOptions)

            # adding addons to the software
            self.__addAddonsToSoftware(software, env)

            # adding software to result
            result.append(software)

        return result

    def __softwareVersion(self, name, env):
        """
        Return the version for the input software.

        @private
        """
        version = self.__softwares[name]['version']

        # in case there is a version override under the env
        bverName = Versioned.toBverName(name)
        if bverName in env:
            version = env[bverName]

        return version

    def __addAddonsToSoftware(self, software, env):
        """
        Add addons to a software.

        @private
        """
        assert isinstance(software, Software), \
            "Invalid software type!"

        softwareName = software.name()

        if softwareName not in self.__addons:
            return

        # creating addons for the software
        for addonName, addonContent in self.__addons[softwareName].items():
            if addonName not in self.__softwares:
                raise AddonNotFoundError(
                    'Could not find a version for the addon "{0}" for the software: "{1}"'.format(
                        addonName,
                        softwareName
                    )
                )

            addonVersion = self.__softwareVersion(addonName, env)
            addonOptions = addonContent['options']

            # creating addon
            addon = Addon(
                addonName,
                addonVersion if 'version' not in addonOptions else addonOptions['version']
            )

            # setting addon options
            self.__setVersionedOptions(addon, addonOptions)

            # adding addon to software
            software.addAddon(addon)

    def __setVersionedOptions(self, versioned, options):
        """
        Set options to a versioned instance.

        @private
        """
        assert isinstance(versioned, Versioned), \
            "Invalid versioned type"

        for optionName, optionValue in options.items():
            versioned.setOption(optionName, optionValue)
