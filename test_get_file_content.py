from functions.get_file_content import get_file_content

def test() -> None:
    result = get_file_content("calculator", "lorem.txt")
    print(f"lorem.txt length: {len(result)}")
    print(f"lorem.txt truncated: {'truncated' in result}")

    result = get_file_content("calculator", "main.py")
    print("result for main.py:")
    print(result)

    result = get_file_content("calculator", "pkg/calculator.py")
    print("result for pkg/calculator.py file:")
    print(result)

    result = get_file_content("calculator", "/bin/cat")
    print("result for /bin/cat file:")
    print(result)
    print("Error: Cannot read \"/bin/cat\" as it is outside the permitted working directory")

    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print("result for pkg/does_not_exist.py file:")
    print(result)
    print("Error: File not found or is not a regular file: \"pkg/does_not_exist.py\"")

if __name__ == "__main__":
    test()


 