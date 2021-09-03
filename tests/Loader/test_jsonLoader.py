import json
import os
from bver.Loader import \
    JsonLoader, \
    UnexpectedRootContentError, \
    UnexpectedAddonsDataError, \
    UnexpectedAddonContentError, \
    UnexpectedVersionFormatError, \
    InvalidFileError, \
    InvalidDirectoryError
from .CommonLoader import CommonLoader

class TestJsonLoader(CommonLoader):
    """Test json loader object."""

    __rootPath = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    __jsonDirectory = os.path.join(__rootPath, 'data', 'json')

    def test_constructor(self):
        """Should test the constructor."""
        JsonLoader()

    def test_emptySoftwares(self):
        """Should test the result when the loader is empty."""
        loader = JsonLoader()

        self.assertEqual(loader.softwares(), [])

    def test_addingJson(self):
        """Should test adding json to the loader."""
        loader = JsonLoader()

        softwareInfos = {
            'a': {
                'version': '10.1',
                'options': {
                    'a': 1
                }
            },
            'b': {
                'version': '12.1',
                'addons': {
                    'a': {
                        'options': {
                            'enabled': True
                        }
                    }
                }
            },
            'c': '10.0.1'
        }

        # adding softwares to the loader
        jsonString = json.dumps(softwareInfos)
        loader.addFromJson(jsonString)

        # checking if the softwares were parsed properly
        softwares = loader.softwares()
        self.checkSoftwareInfo(softwareInfos, softwares)
        self.checkAddonsInfo(softwareInfos, softwares)

    def test_unexpectedRootContent(self):
        """
        Should fail when json does not have the proper format for the root.
        """
        loader = JsonLoader()

        softwareInfos = [{
            'a': '10.1'
        }]
        jsonString = json.dumps(softwareInfos)

        success = False
        try:
            loader.addFromJson(jsonString)
        except UnexpectedRootContentError:
            success = True

        self.assertTrue(success)

    def test_unexpectedVersionFormat(self):
        """
        Should fail when json does not have the proper format for the version.
        """
        loader = JsonLoader()

        softwareInfos = {
            'a': ['10.0']
        }
        jsonString = json.dumps(softwareInfos)

        success = False
        try:
            loader.addFromJson(jsonString)
        except UnexpectedVersionFormatError:
            success = True

        self.assertTrue(success)

    def test_unexpectedAddonsData(self):
        """
        Should fail when json does not have the proper format for the addons.
        """
        loader = JsonLoader()

        softwareInfos = {
            'a': {
                'version': '10.1',
                'addons': []
            },
            'b': '10.10'
        }
        jsonString = json.dumps(softwareInfos)

        success = False
        try:
            loader.addFromJson(jsonString)
        except UnexpectedAddonsDataError:
            success = True

        self.assertTrue(success)

    def test_unexpectedAddonContent(self):
        """
        Should fail when json does not have the proper format for the addon itself.
        """
        loader = JsonLoader()

        softwareInfos = {
            'a': {
                'version': '10.1',
                'addons': {
                    'a': None
                }
            },
            'b': '10.10'
        }
        jsonString = json.dumps(softwareInfos)

        success = False
        try:
            loader.addFromJson(jsonString)
        except UnexpectedAddonContentError:
            success = True

        self.assertTrue(success)

    def test_addingJsonDirectory(self):
        """Should test adding a directory with json files to the loader."""
        loader = JsonLoader()

        softwareInfos = {}

        simpleFilePath = os.path.join(self.__jsonDirectory, 'simple.json')
        complexFilePath = os.path.join(self.__jsonDirectory, 'complex.json')
        externalAddons = os.path.join(self.__jsonDirectory, 'externalAddons.json')
        activeVersion = os.path.join(self.__jsonDirectory, 'activeVersion.json')
        for filePath in [simpleFilePath, complexFilePath, externalAddons, activeVersion]:
            with open(filePath, 'r') as f:
                data = json.load(f)
                for key, value in data.items():
                    softwareInfos[key] = value

        # adding softwares to the loader
        loader.addFromJsonDirectory(self.__jsonDirectory)

        # checking if the softwares were parsed properly
        softwares = loader.softwares()
        self.checkSoftwareInfo(softwareInfos, softwares)
        self.checkAddonsInfo(softwareInfos, softwares)

    def test_addingJsonFile(self):
        """Should test adding json files to the loader."""
        loader = JsonLoader()

        softwareInfos = {}

        simpleFilePath = os.path.join(self.__jsonDirectory, 'simple.json')
        complexFilePath = os.path.join(self.__jsonDirectory, 'complex.json')
        externalAddons = os.path.join(self.__jsonDirectory, 'externalAddons.json')
        for filePath in [simpleFilePath, complexFilePath, externalAddons]:
            with open(filePath, 'r') as f:
                data = json.load(f)
                for key, value in data.items():
                    softwareInfos[key] = value

        # adding softwares to the loader
        loader.addFromJsonFile(simpleFilePath)
        loader.addFromJsonFile(complexFilePath)
        loader.addFromJsonFile(externalAddons)

        # checking if the softwares were parsed properly
        softwares = loader.softwares()
        self.checkSoftwareInfo(softwareInfos, softwares)
        self.checkAddonsInfo(softwareInfos, softwares)

    def test_invalidFile(self):
        """
        Should fail when passing an invalid file path.
        """
        loader = JsonLoader()

        success = False
        try:
            loader.addFromJsonFile('/dev/null/invalid.json')
        except InvalidFileError:
            success = True

        self.assertTrue(success)

    def test_invalidDirectory(self):
        """
        Should fail when passing an invalid directory.
        """
        loader = JsonLoader()

        success = False
        try:
            loader.addFromJsonDirectory('/dev/null/invalid')
        except InvalidDirectoryError:
            success = True

        self.assertTrue(success)
