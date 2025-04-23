from openai import OpenAI
from pathlib import Path
import json
from tqdm import tqdm
from compilerFeedback import compile_or_run
def get_completion(prompt):
    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    temperature=0.0,
    messages=[
        {"role": "developer", "content": "You are a assistant specializing in computer science, particularly evaluation of code. Whenever you are given a task you reason clearly and unambiguously to arrive at an answer. Instead of rushing to an answer you think the problem through even if it takes more time than usual. You are not too verbose. Your answers are short with all the necessary information included. If you do not know the answer of a particular question reply with nothing."},
        {"role": "user", "content": prompt}
    ]
    )
    return (completion.choices[0].message.content)
def get_feedback(problemStatement,referenceSolution,studentSolution,rubric,codeDir,language):
    code=r''''''
    code=code+studentSolution
    compilerFeedback = compile_or_run(code, language)
    prompt=f"""You are an expert code evaluator and grader, evaluating code submissions for a Data Structures and Algorithm test at a university level. You are given a problem statement, reference solution and a student code and compiler feedback . You have to evaluate the student code according to the rubric provided. The problem statement, reference solution, student solution, compiler feedback and rubrick are all delimited by triple backticks. DO NOT GIVE MARKS IN THE FEEDBACK. Problem statement: ```{problemStatement}``` Reference solution: ```{referenceSolution}``` Student solution: ```{studentSolution}``` Rubric: ```{rubric}``` Compiler Feedback: ```{compilerFeedback} The code should not contain any pre or post text like good job or well done. Do not include a score anywhere in your output. No numeric based values should be present anywhere in the feeback."""
    feedback=get_completion(prompt)
    feedback_file = codeDir / "feedback.txt"
    with open(feedback_file, 'w') as f:
        f.write(feedback)

def main():
    rootDir=Path("DSA")
    for folder in rootDir.iterdir():
        quesDir=Path(folder)
        problem_statement_file = quesDir / f"{folder.name}.txt"
        rubric_file = quesDir / "rubric.yaml"
        with open(problem_statement_file, 'r', encoding="utf-8", errors="replace") as f:
            problemStatement=f.read()
        with open(rubric_file, 'r',encoding="utf-8", errors="replace") as f:
            rubric=f.read()
        for langFolder in quesDir.iterdir():
            if langFolder.is_dir():
                langDir=Path(langFolder)
                correct_solution_file=langDir / "Correct_1/Correct_1.txt" 
                language = ""
                if langFolder.name.lower() == "c_plus_plus":
                    language = "c++"
                elif langFolder.name == "Java":
                    language = "java"
                elif langFolder.name == "Python":
                    language = "python"
                with open(correct_solution_file, 'r') as f:
                    referenceSolution=f.read()
                for codeFolder in langDir.iterdir():
                    codeDir=Path(codeFolder)
                    for file in tqdm(list(codeDir.iterdir()), desc=f"Processing files in {codeDir.name}"):
                        if file.name != "feedback.txt":
                            with open(file, 'r', encoding="utf-8", errors="replace") as f:
                                code=f.read()                            
                            get_feedback(problemStatement,referenceSolution,code,rubric,codeDir,language)
                            
                            
main()
