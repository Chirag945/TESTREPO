import subprocess
import sys
import os
import tempfile

def compile_or_run(code, language):
    # Determine the correct file extension
    if language.lower() in ["c++", "cpp"]:
        suffix = ".cpp"
    elif language.lower() == "jav
        elif language.lower() == "java":
            # Compile Java and show all errors
            compile_command = ["javac", tmp_source]
            result = subprocess.run(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
  
            # pylint
            pylint_command = ["python", "-m", "pylint", "--errors-only", tmp_source]
            pylint_result = subprocess.run(pylint_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if pylint_result.stdout :
                return ("Errors:\n", pylint_result.stdout)
            else:
                return ("No errors found.")

    finally:
        os.remove(tmp_source)  # Cleanup temporary file


