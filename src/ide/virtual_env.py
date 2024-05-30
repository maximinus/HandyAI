import os
import venv
import subprocess


class VenvDetails():
    def __init__(self, version, packages):
        self.version = version
        self.packages = packages


def get_python_version(venv_dir):
    # The path to the python executable within the virtual environment
    python_executable = os.path.join(venv_dir, 'bin', 'python')
    if not os.path.exists(python_executable):
        python_executable = os.path.join(venv_dir, 'Scripts', 'python.exe')

    if os.path.exists(python_executable):
        version_command = f'"{python_executable}" --version'
        version = os.popen(version_command).read().strip()
        return version
    else:
        return ''


def get_installed_packages(venv_dir):
    # get the path to the pip executable within the virtual environment
    pip_executable = os.path.join(venv_dir, 'bin', 'pip')
    if not os.path.exists(pip_executable):
        pip_executable = os.path.join(venv_dir, 'Scripts', 'pip.exe')

    if os.path.exists(pip_executable):
        freeze_command = f'"{pip_executable}" freeze --all'
        packages = os.popen(freeze_command).read().strip()
        return packages
    else:
        return "Pip executable not found."


def install_packages(venv_dir, packages):
    """Install packages in the virtual environment."""
    pip_executable = os.path.join(venv_dir, 'bin', 'pip')
    if not os.path.exists(pip_executable):
        pip_executable = os.path.join(venv_dir, 'Scripts', 'pip.exe')

    if os.path.exists(pip_executable):
        for package in packages:
            subprocess.check_call([pip_executable, 'install', package])
            print(f"Package '{package}' installed successfully.")
    else:
        print("Pip executable not found. Ensure the virtual environment was created correctly.")


def create_virtual_environment(venv_dir):
    """Create a virtual environment in the specified directory."""
    venv_builder = venv.EnvBuilder(with_pip=True)
    venv_builder.create(venv_dir)


def get_venv_details(directory):
    if not os.path.exists(directory):
        return ['Directory does not exist', None]
    version = get_python_version(directory)
    if len(version) == 0:
        return [f'No Python environment found in {directory}', None]
    packages = get_installed_packages(directory)
    return ['', VenvDetails(version, packages)]
