import unittest

class CommonLoader(unittest.TestCase):
    """
    Common routines used to check parsed information among the loaders.
    """

    def checkSoftwareInfo(self, softwareInfos, softwares):
        """
        Check if the software information is part of the software list.
        """
        self.assertEqual(len(softwares), len(softwareInfos))

        for softwareName, softwareData in softwareInfos.items():
            software = list(filter(lambda x: x.name() == softwareName, softwares))[0]
            if isinstance(softwareData, dict) and 'active' in softwareData:
                activeVersion = softwareData['active']
                softwareData = softwareData['versions'][activeVersion]
                softwareData['version'] = activeVersion

            version = softwareData['version'] if isinstance(softwareData, dict) else softwareData
            self.assertEqual(software.name(), softwareName)
            self.assertEqual(software.version(), version)

            if 'options' in softwareData:
                self.assertEqual(len(software.optionNames()), len(software.optionNames()))

                for optionName, optionValue in softwareData['options'].items():
                    self.assertEqual(software.option(optionName), optionValue)
            else:
                self.assertEqual(len(software.optionNames()), 0)

    def checkAddonsInfo(self, softwareInfos, softwares):
        """
        Check if the addon information is part of the software list.
        """
        for softwareName, softwareData in softwareInfos.items():
            software = list(filter(lambda x: x.name() == softwareName, softwares))[0]
            if isinstance(softwareData, dict) and 'active' in softwareData:
                activeVersion = softwareData['active']
                softwareData = softwareData['versions'][activeVersion]
                softwareData['version'] = activeVersion

            if 'addons' in softwareData:
                for addonName, addonData in softwareData['addons'].items():
                    addon = software.addon(addonName)
                    addonInfo = softwareInfos[addonName]
                    self.assertEqual(addon.name(), addonName)
                    addonVersion = addonInfo['version'] if isinstance(addonInfo, dict) else addonInfo
                    self.assertEqual(addon.version(), addonVersion)

                    # checking addon options
                    if 'options' in addonData:
                        for optionName, optionValue in addonData['options'].items():
                            self.assertEqual(addon.option(optionName), optionValue)
            else:
                self.assertEqual(len(software.addonNames()), 0)
