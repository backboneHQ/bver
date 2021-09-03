import unittest
from bver.Versioned import Addon

class TestAddon(unittest.TestCase):
    """Test addon object."""

    def test_constructor(self):
        """Should test the values passed to the constructor."""
        name = "foo"
        version = "1.1.0"
        addon = Addon(name, version)

        self.assertEqual(addon.name(), name)
        self.assertEqual(addon.version(), version)

    def test_defaultOptions(self):
        """Should test the default options of the addon."""
        addon = Addon("foo", "1.1")

        self.assertEqual(len(addon.optionNames()), 1)
        self.assertEqual(addon.option('enabled'), True)
