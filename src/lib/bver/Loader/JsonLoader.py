import os
import sys
import glob
import json
from .Loader import Loader
from ..Versioned import Versioned

# compatibility with python 2/3
try:
    basestring
except NameError:
    basestring = str

class UnexpectedRootContentError(Exception):
    """Unexpected root content error."""

class UnexpectedAddonsDataError(Exception):
    """Unexpected addons data error."""

class UnexpectedAddonContentError(Exception):
    """Unexpected addon content error."""

class UnexpectedVersionFormatError(Exception):
    """Unexpected version format error."""

class InvalidDirectoryError(Exception):
    """Invalid directory Error."""

class InvalidFileError(Exception):
    """Invalid file Error."""

class JsonLoader(Loader):
    """
    Loads a list of softwares from a json.
    """

    def __init__(self, *args, **kwargs):
        """
        Create a json loader object.
        """
        super(JsonLoader, self).__init__(*args, **kwargs)

        self.__cache = {}

    def addFromJson(self, jsonContents, activeVersionFromEnv=None, ignoreAddons=False):
        """
        Add softwares and addons from json contents.

        Supported formats:
        {
            "a": "1.0.0",
            "b": "1.1.0",
            "c": {
                "version": "1.2.5",
                "addons": {
                    "a": {
                        "options": { // options as addon
                            "version": "1.0.0",
                            "enabled": true
                        }
                    },
                    "b": {
                        "options": {
                            "enabled": false
                        }
                    }
                },
                "options": { // options as standalone
                    "foo": 10
                }
            }
        }

        or

        {
            "c": {
                "active": "1.2.5",
                "versions": {
                    "1.2.5": {
                        "addons": {
                            "kombi": {
                                "options": {
                                    "version": "1.0.0",
                                    "enabled": true
                                }
                            }
                        }
                    }
                }
            }
        }
        """
        contents = json.loads(jsonContents)

        # root checking
        if not isinstance(contents, dict):
            raise UnexpectedRootContentError('Expecting object as root!')

        for softwareName, softwareContents in contents.items():
            self.__addParsedSoftware(
                softwareName,
                softwareContents,
                activeVersionFromEnv,
                ignoreAddons
            )

    def addFromJsonFile(self, fileName, activeVersionFromEnv=None, ignoreAddons=False):
        """
        Add json from a file.

        The json file need to follow the format expected
        by {@link addFromJson}.
        """
        # making sure it's a valid file
        if not os.path.exists(fileName) or not os.path.isfile(fileName):
            raise InvalidFileError(
                'Invalid file "{0}"!'.format(fileName)
            )

        if fileName not in self.__cache:
            with open(fileName, 'r') as f:
                self.__cache[fileName] = f.read()

        try:
            self.addFromJson(
                self.__cache[fileName],
                activeVersionFromEnv,
                ignoreAddons
            )
        except Exception as e:
            sys.stderr.write('Error on loading version file: {}\n'.format(fileName))
            raise e

    def addFromJsonDirectory(self, directory, activeVersionFromEnv=None):
        """
        Add json from inside of a directory with json files.

        The json file need to follow the format expected
        by {@link addFromJson}.
        """
        # making sure it's a valid directory
        if not (os.path.exists(directory) and os.path.isdir(directory)):
            raise InvalidDirectoryError(
                'Invalid directory "{0}"!'.format(directory)
            )

        # collecting the json files and loading them to the loader.
        allJsonFiles = glob.glob(os.path.join(directory, '*.json'))

        # finally loading files
        # first without the addons, so it can load all softwares
        for jsonFile in allJsonFiles:
            self.addFromJsonFile(jsonFile, activeVersionFromEnv, ignoreAddons=True)

        # now we load with addons (therefore a software can be referred as addon
        # in others json files
        for jsonFile in allJsonFiles:
            self.addFromJsonFile(jsonFile, activeVersionFromEnv)

    def addFromJsonPaths(self, paths, activeVersionFromEnv=None):
        """
        Load the json configuration from paths pointing to json files or/and directories containing json files.
        """
        allJsonFiles = []
        for path in paths:
            # skipping invalid paths
            if not path or not os.path.exists(path):
                continue

            if os.path.isfile(path):
                allJsonFiles.append(path)
            else:
                for fileName in glob.glob(os.path.join(path, '*.json')):
                    allJsonFiles.append(fileName)

        # finally loading files
        # first without the addons, so it can load all softwares
        for jsonFile in allJsonFiles:
            self.addFromJsonFile(jsonFile, activeVersionFromEnv, ignoreAddons=True)

        # now we load with addons (therefore a software can be referred as addon
        # in others json files
        for jsonFile in allJsonFiles:
            self.addFromJsonFile(jsonFile, activeVersionFromEnv)

    def clear(self):
        """
        Clear the cache.
        """
        self.__cache.clear()

    def __addParsedSoftware(self, softwareName, softwareContents, activeVersionFromEnv, ignoreAddons=False):
        """
        Add a software based on the parsed software contents.

        @private
        """
        options = {}
        addons = {}
        softwareBverName = Versioned.toBverName(softwareName)
        version = activeVersionFromEnv[softwareBverName] if activeVersionFromEnv and softwareBverName in activeVersionFromEnv else None

        # if case the contents contain multiple versions
        # loading the information from the specific version
        if 'versions' in softwareContents:
            # skipping the parsing in case the contents does not have configuration
            # for the particular version
            if version and version not in softwareContents['versions']:
                return
            version = version or softwareContents['active']
            softwareContents = dict(softwareContents['versions'][version])
            softwareContents['version'] = version

        if isinstance(softwareContents, dict):
            if version is None and 'version' in softwareContents:
                version = softwareContents['version']

            if 'options' in softwareContents:
                options = softwareContents['options']

            if 'addons' in softwareContents:
                addons = softwareContents['addons']

        # when the value is a string (version)
        elif isinstance(softwareContents, basestring):
            version = softwareContents

        # otherwise there's a problem
        if not version:
            raise UnexpectedVersionFormatError(
                'Could not decode version for "{0}"'.format(softwareName)
            )

        # adding software
        self.addSoftwareInfo(softwareName, version, options)

        # adding addons
        if not ignoreAddons:
            self.__addParsedAddons(softwareName, addons)

    def __addParsedAddons(self, softwareName, addons):
        """
        Add an addon based on the parsed addon contents.

        @private
        """
        # addon checking
        if not isinstance(addons, dict):
            raise UnexpectedAddonsDataError('Expecting object for addons!')

        for addonName, addonData in addons.items():
            addonOptions = {}

            if not isinstance(addonData, dict):
                raise UnexpectedAddonContentError('Expecting object as content for addon!')

            if 'options' in addonData:
                addonOptions = addonData['options']

            self.addAddonInfo(softwareName, addonName, addonOptions)
