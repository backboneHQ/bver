from bver.Loader import Loader, AddonNotFoundError
from .CommonLoader import CommonLoader

class TestLoader(CommonLoader):
    """Test loader object."""

    def test_constructor(self):
        """Should test the constructor."""
        Loader()

    def test_emptySoftwares(self):
        """Should test the result when the loader is empty."""
        loader = Loader()

        self.assertEqual(loader.softwares(), [])

    def test_softwareInfo(self):
        """Should test adding parsed software info to the loader."""
        loader = Loader()

        softwareInfos = {
            'a': {
                'version': '10.1',
                'options': {
                    'a': 1
                }
            },
            'b': {
                'version': '12.1',
                'options': {
                }
            }
        }

        # adding sotwares to the loader
        for softwareName, softwareData in softwareInfos.items():
            loader.addSoftwareInfo(
                softwareName,
                softwareData['version'],
                softwareData['options'],
            )

        # checking if the softwares were parsed properly
        softwares = loader.softwares()
        self.checkSoftwareInfo(softwareInfos, softwares)

    def test_addonInfo(self):
        """Should test adding parsed addon info to the loader."""
        loader = Loader()

        softwareInfos = {
            'a': {
                'version': '10.1',
                'addons': {
                    'c': {
                        'options': {
                            'enabled': False
                        }
                    }
                },
                'options': {
                    'foo': 1
                }
            },
            'b': {
                'version': '12.1',
                'addons': {
                    'c': {},
                    'd': {},
                },
                'options': {
                    'foo': 1
                }
            },
            'c': {
                'version': '12.1',
                'options': {
                }
            },
            'd': {
                'version': '14.1',
                'options': {
                }
            }
        }

        # adding sotwares & addons to the loader
        for softwareName, softwareData in softwareInfos.items():
            loader.addSoftwareInfo(
                softwareName,
                softwareData['version'],
                softwareData['options'],
            )

            # addons
            if 'addons' in softwareData:
                for addonName, addonData in softwareData['addons'].items():
                    if 'options' in addonData:
                        loader.addAddonInfo(
                            softwareName,
                            addonName,
                            addonData['options']
                        )
                    else:
                        loader.addAddonInfo(
                            softwareName,
                            addonName
                        )

        # checking if the softwares were properly parsed
        softwares = loader.softwares()

        # checking addons
        self.checkAddonsInfo(softwareInfos, softwares)

    def test_addonNotFound(self):
        """Should fail when addon is not declared as software."""
        loader = Loader()

        softwareInfos = {
            'a': {
                'version': '10.1',
                'addons': {
                    'missing': {}
                }
            },
            'b': {
                'version': '10.1',
            }
        }

        # adding sotwares & addons to the loader
        for softwareName, softwareData in softwareInfos.items():
            loader.addSoftwareInfo(
                softwareName,
                softwareData['version']
            )

            # addons
            if 'addons' in softwareData:
                for addonName, addonData in softwareData['addons'].items():
                    loader.addAddonInfo(
                        softwareName,
                        addonName
                    )

        success = False
        try:
            loader.softwares()
        except AddonNotFoundError:
            success = True

        self.assertTrue(success)

    def test_customEnv(self):
        """Should assing the version passed by the environment."""
        loader = Loader()

        customEnv = {
            'BVER_A_VERSION': '14',
            'BVER_B_VERSION': '15',
        }

        softwareInfos = {
            'a': {
                'version': '10.1',
                'addons': {
                    'b': {}
                }
            },
            'b': {
                'version': '12.1',
            },
            'c': {
                'version': '11.1'
            }
        }

        softwareInfosFinal = {
            'a': {
                'version': '14',
                'addons': {
                    'b': {}
                }
            },
            'b': {
                'version': '15',
            },
            'c': {
                'version': '11.1'
            }
        }

        # adding sotwares & addons to the loader
        for softwareName, softwareData in softwareInfos.items():
            loader.addSoftwareInfo(
                softwareName,
                softwareData['version']
            )

            # addons
            if 'addons' in softwareData:
                for addonName, addonData in softwareData['addons'].items():
                    loader.addAddonInfo(
                        softwareName,
                        addonName
                    )

        softwares = loader.softwares(customEnv)

        # checking addons
        self.checkSoftwareInfo(softwareInfosFinal, softwares)

        # checking addons
        self.checkAddonsInfo(softwareInfosFinal, softwares)
