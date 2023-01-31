import re

# compatibility with python 2/3
try:
    basestring
except NameError:
    basestring = str

class InvalidNameError(Exception):
    """Invalid name error."""

class InvalidOptionError(Exception):
    """Invalid option error."""

class InvalidVersionError(Exception):
    """Invalid version error."""

class Versioned(object):
    """
    Abstract versioned object.
    """

    __nameRegEx = re.compile('^[^\W]+$')

    def __init__(self, name, version):
        """
        Create a versioned object.
        """
        self.__options = {}
        self.__setName(name)
        self.__setVersion(version)

    def version(self):
        """
        Return the version.
        """
        return self.__version

    def bverName(self):
        """
        Return the environment variable name of the versioned.
        """
        return Versioned.toBverName(self.name())

    def setOption(self, name, value):
        """
        Set an option.
        """
        assert (isinstance(name, basestring)), \
            "Option name needs to be string"

        assert len(name), "option name cannot be empty"

        self.__options[name] = value

    def option(self, name):
        """
        Return the option value.
        """
        if name not in self.__options:
            raise InvalidOptionError('option "{0}" does not exist!'.format(name))

        return self.__options[name]

    def optionNames(self):
        """
        Return the list of option names.
        """
        return self.__options.keys()

    def name(self):
        """
        Return the versioned name.
        """
        return self.__name

    @staticmethod
    def toBverName(*parts):
        """
        Convert the input versioned parts to the bver env name convention.
        """
        name = '_'.join(parts)
        return 'BVER_{0}_VERSION'.format(
            name.upper()
        )

    def __setName(self, name):
        """
        Set the addon name.

        @private
        """
        if not (isinstance(name, basestring) and len(name) and self.__nameRegEx.match(name)):
            raise InvalidNameError(
                'Invalid addon name: "{0}"'.format(name)
            )

        self.__name = name

    def __setVersion(self, version):
        """
        Set a version.

        @private
        """
        if not (isinstance(version, basestring) and len(version)):
            raise InvalidVersionError(
                'version needs to be defined as valid string "{0}"'.format(
                    version
                )
            )

        self.__version = version
