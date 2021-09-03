import unittest
from bver.Versioned import Versioned, InvalidNameError, InvalidOptionError, InvalidVersionError

class TestVersioned(unittest.TestCase):
    """Test versioned object."""

    def test_constructor(self):
        """Should test the values passed to the constructor."""
        name = "foo"
        version = "1.1.0"
        versioned = Versioned(name, version)

        self.assertEqual(versioned.name(), name)
        self.assertEqual(versioned.version(), version)

    def test_validNames(self):
        """Should test valid names."""
        validNames = [
            'foo',
            'foo12',
            'foo_someName',
        ]

        for name in validNames:
            Versioned(name, "1.0.1")

    def test_invalidNames(self):
        """Should fail when trying to use names that contains invalid characters."""
        invalidNames = [
            1,
            '',
            'foo 12',
            'foo#someName',
            'foo-someName',
        ]

        failedCount = 0
        for name in invalidNames:
            try:
                Versioned(name, "1.0.1")
            except InvalidNameError:
                failedCount += 1

        self.assertEqual(failedCount, len(invalidNames))

    def test_validVersions(self):
        """Should test valid versions."""
        validVersions = [
            '1.0.0',
            '1',
            '10.5v',
        ]

        for version in validVersions:
            Versioned("foo", version)

    def test_invalidVersions(self):
        """Should fail when trying to use a version that does not conform with the spec."""
        invalidVersions = [
            1,
            '',
            '10#11',
            '10 1',
        ]

        failedCount = 0
        for version in invalidVersions:
            try:
                Versioned("foo", version)
            except InvalidVersionError:
                failedCount += 1

        self.assertEqual(failedCount, len(invalidVersions))

    def test_defaultOptions(self):
        """Should test the default options of the versioned."""
        versioned = Versioned("foo", "1.1")

        self.assertEqual(len(versioned.optionNames()), 0)

    def test_toBverName(self):
        """Should return a string converted to the bver convention."""
        self.assertEqual(Versioned.toBverName('foo'), "BVER_FOO_VERSION")

    def test_bverName(self):
        """Should return an bver environment variable based on the versioned name."""
        versioned = Versioned("foo", "1.0")

        self.assertEqual(versioned.bverName(), "BVER_FOO_VERSION")

    def test_customOptions(self):
        """Should test the support for custom options."""
        options = {
            'a': 1,
            'b': "foo",
            'c': 3
        }

        versioned = Versioned("foo", "1.0")
        for optionName, optionValue in options.items():
            versioned.setOption(optionName, optionValue)

        optionNames = versioned.optionNames()
        self.assertEqual(len(optionNames), len(options))

        for optionName, optionValue in options.items():
            self.assertIn(optionName, optionNames)
            self.assertEqual(versioned.option(optionName), optionValue)

    def test_invalidOption(self):
        """Should fail to get a value from an option that does not exist."""
        versioned = Versioned("foo", "1.1.0")

        success = False
        try:
            versioned.option('foo')
        except InvalidOptionError:
            success = True

        self.assertTrue(success)
