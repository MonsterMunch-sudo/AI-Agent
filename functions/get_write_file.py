import os



    #write_file creates or overwrites a file with given content, safely.
def write_file(working_directory: str, file_path: str, content: str) -> str:
    working_dir = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_dir, file_path))
    valid_target_file = os.path.commonpath([working_dir, target_file_path]) == working_dir

    try:
        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        if target_file_path:
            os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

        with open(target_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: writing to file "{file_path}": "{e}"'



schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "creates or overwrites a file with given content, safely.",
        "parameters": {
            "required": ["file_path", "content"],
            "type": "object",
            "properties": {
                "file_path":{
                    "type": "string",
                    "description": "is the relative path to the target file, as given by the LLM",
                },
                "content": {
                    "type": "string",
                    "description": "is simply the string of text you want written into the file.",
                },
            },
        },
    },
}