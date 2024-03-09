import os
import io
import time
import docker
import tarfile
import tempfile

from pathlib import Path
from docker.errors import ImageNotFound, BuildError, APIError, ContainerError

# how should a tool look?

"""
A tool is used by an agent.
The tool is given text and returns text, really just like an agent
So a tool is just another transformer, except it might throw errors
So a tool should:

1: Take some text
2: Do something with it
3: Reply with what happened
4: If the input text was wrong, the tool should say why (if it can)

Agents
When we talk of agents, we mean again of boxes that input text and then and output text.
Agents normally have a memory and also some leader text


Tasks
A task is something we would like to do.
What we mean by *do* is very important.
An llm by default can only ever convert text to text.
It's response may be right, or it may be wrong, and the for the interesting cases the latter is usual.
You can use a tool to determine if something is correct, however a tool must be defined in Python.
In theory you can let an llm determine if something it correct, however it could always be wrong.
A task does the usual thing; ultimately it takes in some text, and it returns some text.

A simple task would just be one agent. It would read in your text and then return some text.
Then:
    * Some more text is put in, i.e. a conversation is started
    * It decides it has finished (which is always after the first response with no tool)
    * It has some way of testing correctness, in which it may try to fix itself and therefore try many times.
    
A more complex example could be 3 or 4 llms.
For this task you need a manger who has the ability to tell other agents to do the work.
"""


DEFAULT_PYTHON_VERSION = '3.11'
DEFAULT_DOCKER_TAG = 'crew-python-runner'
DOCKER_FOLDER = '/app'


docker_file = """
FROM python:{version}

WORKDIR /app
COPY . /app
CMD ["tail", "-f", "/dev/null"]
"""


class RunnerError(Exception):
    pass


def get_code_temp_file(code: str):
    temp_file = tempfile.NamedTemporaryFile(mode='w+t', delete=False, suffix='.py')
    temp_file.write(code)
    temp_file.flush()
    # as delete is false, closing will not remove the file
    temp_file.close()
    return Path(temp_file.name)


def create_tar_from_code(code: str):
    """Create a tar archive containing the specified file."""
    code_file = get_code_temp_file(code)
    with open(code_file, 'rb') as f:
        file_data = f.read()
    tar_stream = io.BytesIO()
    with tarfile.open(fileobj=tar_stream, mode='w') as tar:
        tarinfo = tarfile.TarInfo(name=code_file.name)
        tarinfo.size = len(file_data)
        tarinfo.mtime = time.time()
        tar.addfile(tarinfo, io.BytesIO(file_data))
    tar_stream.seek(0)
    return [tar_stream, code_file]


class PythonResult:
    def __init__(self, error: int, result):
        self.error_code = error
        # convert to string from bytecode if required
        try:
            result = result.decode()
        except (UnicodeError, AttributeError):
            pass
        # strip ending \n if it exists
        self.output = result.rstrip()


class DockerRunner:
    def __init__(self, version=DEFAULT_PYTHON_VERSION):
        self.version = version
        self.client = docker.from_env()
        self.runner = self.start_runner()

    def create_docker_image(self):
        # init the python version. this may involve a download
        # Convert to "file like object" for the docker setup
        formatted_docker_file = io.BytesIO(str.encode(docker_file.format(version=self.version)))
        # from docs: The first item is the Image object for the image that was built.
        return self.client.images.build(fileobj=formatted_docker_file, tag=DEFAULT_DOCKER_TAG)[0]

    def get_image(self):
        try:
            return self.client.images.get(DEFAULT_DOCKER_TAG)
        except ImageNotFound:
            pass
        return self.create_docker_image()

    def start_runner(self):
        try:
            image = self.get_image()
            return self.client.containers.run(image, detach=True, auto_remove=True)
        except (BuildError, APIError, ContainerError) as ex:
            raise RunnerError(ex)

    def run_python(self, code: str) -> PythonResult:
        # copy the file to the docker image
        tar, filepath = create_tar_from_code(code)
        self.runner.put_archive(DOCKER_FOLDER, tar)
        # run the code in python
        docker_filepath = f'{DOCKER_FOLDER}/{filepath.name}'
        exit_code, output = self.runner.exec_run(f'python {docker_filepath}')
        # delete the file in the container
        self.runner.exec_run(f'rm {docker_filepath}')
        # delete the file here
        os.remove(filepath)
        return PythonResult(exit_code, output)


# need to get rid of this somehow
# maybe make a singleton that shares some data?
# the runner should likely not try to pull in the docker image, at least not by default
runner = DockerRunner()


"""
A tool is again, something that consumes text and returns text.
The simplest tool is an agent! it consumes text and returns some. It's got leader text as well.
Sounds trivial, but important; if there are more than 2 agents on a task then code-wise they are just other tools.
But that could be seen as the null tool.
The real use of a tool is to connect with the real world in some way.
Read a webpage, lookup some meaning, run some code, etc etc
We should say that a tool is "invisible", "safe" or "open"
Invisible means that the tool is a function that does not connect with the real world, i.e. files, the web
Safe means that the tool will read things, or ask for things, but it will not do anything
    It might read files, scour the web, check a files size
Open means the tool could control something in some way. It might write to a DB, create a file or similar.

Here's our tool to call python code
"""

