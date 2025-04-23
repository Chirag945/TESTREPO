import subprocess
import sys
import os
import tempfile

def compile_or_run(code, language):
    # Determine the correct file extension
    if language.lower() in ["c++", "cpp"]:
        suffix = ".cpp"
    elif language.lower() == "java":
        suffix = ".java"
    elif language.lower() == "python":
        suffix = ".py"
    else:
        print("Unsupported language. Please choose C++, Java, or Python.")
        return

    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, mode='w') as tmp_file:
        tmp_file.write(code)
        tmp_source = tmp_file.name

    try:
        if language.lower() in ["c++", "cpp"]:
            # Compile C++ and show all errors
            output_executable = "a.out" if os.name != "nt" else "a.exe"
            compile_command = ["g++", tmp_source, "-o", output_executable]
            result = subprocess.run(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                return result.stderr
            else:
                return ("C++ Compilation succeeded!")
        elif language.lower() == "java":
            # Compile Java and show all errors
            compile_command = ["javac", tmp_source]
            result = subprocess.run(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                return result.stderr
            else:
                return ("Java Compilation succeeded!")
        elif language.lower() == "python":
            # Run Python static analysis using pylint, flake8, and mypy

            # pylint
            pylint_command = ["python", "-m", "pylint", "--errors-only", tmp_source]
            pylint_result = subprocess.run(pylint_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if pylint_result.stdout :
                return ("Errors:\n", pylint_result.stdout)
            else:
                return ("No errors found.")

    finally:
        os.remove(tmp_source)  # Cleanup temporary file


