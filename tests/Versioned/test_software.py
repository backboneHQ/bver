import unittest
from bver.Versioned import Software, Addon, InvalidAddonError

class TestSoftware(unittest.TestCase):
    """Test software object."""

    def test_constructor(self):
        """Should test the values passed to the constructor."""
        name = "foo"
        version = "1.1.0"
        software = Software(name, version)

        self.assertEqual(software.name(), name)
        self.assertEqual(software.version(), version)

    def test_defaultOptions(self):
        """Should test the default options of the software."""
        software = Software("foo", "1.1")

        self.assertEqual(len(software.optionNames()), 0)

    def test_addons(self):
        """Should add addons to the software."""
        software = Software("foo", "1.1")

        addons = {
            "a": None,
            "b": None,
            "c": None
        }

        for addonName in addons:
            addon = Addon(addonName, "1.0")
            addons[addonName] = addon
            software.addAddon(addon)

        self.assertEqual(len(addons), len(software.addonNames()))

        # should be the same instance
        for addonName in addons.keys():
            self.assertIs(software.addon(addonName), addons[addonName])

    def test_disabledAddons(self):
        """Should disabled addons in the software."""
        software = Software("foo", "1.1")

        addons = {
            "a": None,
            "b": None,
            "c": None
        }

        for addonName in addons:
            addon = Addon(addonName, "1.0")
            addon.setOption('enabled', False)
            addons[addonName] = addon
            software.addAddon(addon)

        self.assertEqual(len(addons), len(software.addonNames()))

        # should be the same instance
        for addonName in addons.keys():
            self.assertEqual(
                software.addon(addonName).bverEnabledName(software),
                'BVER_{}_{}_ENABLED'.format(
                    software.name().upper(),
                    addonName.upper()
                )
            )

    def test_invalidAddons(self):
        """Should fail to get an invalid addon."""
        software = Software("foo", "1.1")

        success = False
        try:
            software.addon('invalid')
        except InvalidAddonError:
            success = True

        self.assertTrue(success)
