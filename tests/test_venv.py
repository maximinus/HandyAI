import unittest
from pathlib import Path

from ide.virtual_env import get_python_version, get_installed_packages, get_pip_executable

TEST_VENV = Path(__file__).parent.parent / 'venv'


class TestVirtualEnvDetection(unittest.TestCase):
    def test_correct_version(self):
        version = get_python_version(TEST_VENV)
        self.assertEqual(version, 'Python 3.11.9')

    def test_empty_string_with_no_venv(self):
        version = get_python_version(__file__)
        self.assertEqual(len(version), 0)

    def test_empty_string_on_invalid_dir(self):
        version = get_python_version('rubbish')
        self.assertEqual(len(version), 0)


class TestEnvironmentDetails(unittest.TestCase):
    def test_correct_libs(self):
        libs = get_installed_packages(TEST_VENV)
        self.assertTrue(len(libs) > 20)

    def test_empty_with_no_venv(self):
        libs = get_installed_packages(__file__)
        self.assertEqual(len(libs), 0)

    def test_empty_on_invalid_dir(self):
        libs = get_installed_packages('rubbish')
        self.assertEqual(len(libs), 0)


class TestPipExists(unittest.TestCase):
    def test_get_pip(self):
        pip = get_pip_executable(TEST_VENV)
        self.assertIsNotNone(pip)

    def test_empty_with_no_venv(self):
        pip = get_pip_executable(__file__)
        self.assertIsNone(pip)

    def test_empty_on_invalid_dir(self):
        pip = get_pip_executable('rubbish')
        self.assertIsNone(pip)
