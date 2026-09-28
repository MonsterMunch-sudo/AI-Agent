import os, subprocess
from abc import ABC, abstractmethod
from config import MAX_CHARS


class subprocess_result(ABC):
    @property
    @abstractmethod
    def returncode(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def stdout(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def stderr(self) -> str:
        raise NotImplementedError

    @property
    def has_output(self) -> bool:
        return bool(self.stdout or self.stderr)

    def as_text(self) -> str:
        outputs = []
        if self.stdout:
            outputs.append(f"STDOUT: {self.stdout}")
        if self.stderr:
            outputs.append(f"STDERR: {self.stderr}")
        return "\n".join(outputs) if outputs else "No output produced"

    def __bool__(self) -> bool:
        return self.returncode == 0


class CompletedProcessResult(subprocess_result):
    def __init__(self, completed_process: subprocess.CompletedProcess[str]):
        self._completed_process = completed_process

    @property
    def returncode(self) -> int:
        return self._completed_process.returncode

    @property
    def stdout(self) -> str:
        return self._completed_process.stdout or ""

    @property
    def stderr(self) -> str:
        return self._completed_process.stderr or ""

    #get_file_content reads and returns the text content of a specific file, safely.
def get_file_content(working_directory: str, file_path: str) -> str:
    working_dir = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_dir, file_path))
    valid_target_file = os.path.commonpath([working_dir, target_file_path]) == working_dir


    try:
        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file_path, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content
    except Exception as e:
        return f'Error: reading file "{file_path}": "{e}"'


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "reads and returns the text content of a specific file, safely.",
        "parameters": {
            "required": ["file_path"],
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "is the relative path to the target file, as given by the LLM",
                },
            },
        },
    },
}

