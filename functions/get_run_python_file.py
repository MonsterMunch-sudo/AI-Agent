import os, subprocess


    #run_python_file actually executes a Python script and reports its output.
def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    working_dir = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_dir, file_path))
    valid_target_file = os.path.commonpath([working_dir, target_file_path]) == working_dir

    try:
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file_path]
        if args:
            command.extend(args)
        result = subprocess.run(
            command,
            cwd=working_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output: list[str] = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"



schema_run = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "actually executes a Python script and reports its output.",
        "parameters": {
            "required": ["file_path"],
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "is the relative path to the target file, as given by the LLM",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of arguments to pass to the Python script",
                },
            },
        },
    },
}