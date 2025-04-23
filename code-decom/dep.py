from openai import OpenAI
import json
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

def getDepth(code):
    # get the depth of the code
    # return the depth
    prompt=f"get the depth of the code delimited by triple backticks. Depth of the code is defined as nesting level of predefined constructs. The constructs that are considered as a new level are as follows:- a loop, assignment of a variable, defining a class, defining a function/method, a conditional using if-else or a switch call. Return a single number - the depth of the given code. Do not attach any pre or post text like depth is etc.  ```{code}```"
    ans = get_completion(prompt)
    return int(ans)

def codeDecomposition(code):
    # break code into subcodes using AST. ast in python can only be used for python files. 
    # suggested by chatGPT
    # return a list of the subcodes
    prompt=f""" You are given a code snippet. You need to break this code into subcodes. 
    A subcode starts if there is a loop or defining a class or defining a function/method or
    a conditional using if-else or a switch call and ends when that construct's definition has finished. 
    Only decompose codes on the initial level of the code's AST. 
    Whatever is nested inside the first level is part of the subcode. 
    The decomposition must be exhaustive, ensuring that every line, symbol, and punctuation mark in the original 
    code is explicitly included in one of the defined subcodes, leaving no element unaccounted for. 
    Return the subcodes in a JSON format with the key 'subcodes' and the corresonding value to be array of the subcodes. 
    Do not attach any pre or post text like subcodes are etc. DO NOT alter the code in any way,shape or form.
    Just return the exact sub code snippet in the array.    {code}
    """    
    json_string = get_completion(prompt)
    data=json.loads(json_string)
    ans=data['subcodes']
    if len(ans)==1:
        prompt2=f"""You are given a code snippet. Remove the outermost construct from the code snippet and return the remaining code. The outermost construct is defined as the first construct that is encountered in the code snippet. The code snippet is delimited by triple backticks. Do not attach any pre or post text like code is etc.  {code}"""
        code=get_completion(prompt2)
        return codeDecomposition(code)
    return ans

def getDependencies(code):
    # get the dependencies of the code
    # return a list of dependencies
    prompt=f""" You are given a code snippet. You need to find the dependencies of the code. Dependencies are the variables,methods, classes or any other user defined constructs that are used in the code but are not defined in the code and are not part of the standard library of the programming language. Return the dependencies in a comma separated format. Do not attach any pre or post text like dependencies are etc.  ```{code}```"""
    ans = get_completion(prompt)
    return ans.split(',')

def retrieveSemantics(dependencies,storage):
    # get the semantics of the dependencies
    # return a dictionary of the dependencies and their semantics
    # If the code is semantically correct, each external dependency should have been previously analyzed and exist in the Semantic Dependency Decoupling Storage unit. We simply need to search and retrieve the semantics associated with each external dependency variable. The semantic descriptions (DPsemantics) of these external dependencies, retrieved from the Semantic Dependency Decoupling Storage unit, is then combined with the SC and inputted into the LLM for analysis.
    dependencySemantics={}
    for DP in dependencies:
        if DP in storage:
            dependencySemantics[DP]=storage[DP]
        else :
            print(f"Dependency not found in storage for {DP}")            
    return dependencySemantics

def LLM(code,dependencySemantics,subCodesSemantics=None):    
    # use the LLM to get the semantics of the code
    # return the semantics of the code
    prompt = f""" The aim is to get the semantics of the code delimited by triple backticks
    given the semantics of user defined dependencies and the semantics of subcodes if there are any.
    You are required to refer to {dependencySemantics} for meaning of user defined dependencies in the code. It is a a dictionary of the dependencies and their semantics.
    You are required to refer to {subCodesSemantics}  for the meaning of subcodes present in the code. It is a list of the semantics of the subcodes of the given code.
    Keeping the above meanings in mind, find the semantics of {code}. 
    The output should strictly be in a string format that contains the meaning of the code. Do not make up any answers and if 
    you are confused just say you don't know. Do not return the semantics of user-defined dependencies and subCode smeantics.
    """
    ans = get_completion(prompt)
    return ans

def updateSemantic(dependency,subCodesSemantic):
    # update the semantic of the dependency using the semantic of the subcodes
    # return the updated semantic
    prompt=f"""You are given the semantic of a dependency and the semantic of the subcode. Using these semantics, update the semantic of the dependency. The semantic of the dependency is delimited by triple backticks. The semantic of the subcode is delimited by double backticks. Return the updated semantic of the dependency. Do not attach any pre or post text like semantics are etc. Semantics of the dependency: ```{dependency}``` Semantics of the subcode: ``{subCodesSemantic}``  """
    ans = get_completion(prompt)
    return ans


def summarizeSemantic(subCodesSemantics):
    # summarize the semantics of the subcodes
    # return the summarized semantic
    prompt=f"""You are given semantics of various subcodes. Using these semantics, summarize the semantics of the entire code. The semantics of the subcodes are delimited by triple backticks and are given as a list. Return the summarized semantics of the entire code. Do not attach any pre or post text like semantics are etc. ```{subCodesSemantics}```  """
    ans = get_completion(prompt)
    return ans

    
def getSemantic(code):
    storage={}
    subCodes=codeDecomposition(code)
    subCodesSemantics=[]
    for SC in subCodes:
        print(f"Processing subcode {SC}")
        SCDepth=getDepth(SC)
        print(f"Depth of subcode is {SCDepth}")
        dependencies=getDependencies(SC)
        print(f"Dependencies of subcode are {dependencies}")
        dependencySemantics=retrieveSemantics(dependencies,storage)
        print(f"Semantics of dependencies are {dependencySemantics}")
        if SCDepth<2:
            subCodesSemantic=LLM(SC,dependencySemantics)
            print(f"SCDepth is less than 3. Semantics of subcode is {subCodesSemantic}")
        else:
            SSCSemantics=getSemantic(SC)
            subCodesSemantic=LLM(SC,dependencySemantics,SSCSemantics)
            print(f"SCDepth is greater than 3. Semantics of subcode is {subCodesSemantic}")
        subCodesSemantics.append(subCodesSemantic)
        for DP in dependencySemantics:
            newDependency=updateSemantic(DP,subCodesSemantic)
            print(f"Updated semantic of dependency {DP} is {newDependency}")
            storage.update(newDependency)
    codeSemantic=summarizeSemantic(subCodesSemantics)
    print(f"Summarized Semantics of the code is {codeSemantic}")
    return codeSemantic   

solution="""import java.io.*;
import java.util.*;
import java.util.Comparator;

class Player {
    private String playerName;
    private Role role;
    private int runsScored;
    private int wicketsTaken;
    private String teamName;

    public Player(String playerName, Role role, int runsScored, int wicketsTaken, String teamName) {
        this.playerName = playerName;
        this.role = role;
        this.runsScored = runsScored;
        this.wicketsTaken = wicketsTaken;
        this.teamName = teamName;
    }

    public String getPlayerName() {
        return playerName;
    }

    public void setPlayerName(String playerName) {
        this.playerName = playerName;
    }

    public Role getRole() {
        return role;
    }

    public void setRole(Role role) {
        this.role = role;
    }

    public int getRunsScored() {
        return runsScored;
    }

    public void setRunsScored(int runsScored) {
        this.runsScored = runsScored;
    }

    public int getWicketsTaken() {
        return wicketsTaken;
    }

    public void setWicketsTaken(int wicketsTaken) {
        this.wicketsTaken = wicketsTaken;
    }

    public String getTeamName() {
        return teamName;
    }

    public void setTeamName(String teamName) {
        this.teamName = teamName;
    }

    @Override
    public String toString() {
        return "Player{" +
               "playerName='" + playerName + '\'' +
               ", role=" + role +
               ", runsScored=" + runsScored +
               ", wicketsTaken=" + wicketsTaken +
               ", teamName='" + teamName + '\'' +
               '}';
    }

    public String toCsvFormat() {
        return String.format("%s,%s,%d,%d,%s",
                playerName, role, runsScored, wicketsTaken, teamName);
    }
}

enum Role {
    BATSMAN, BOWLER, ALL_ROUNDER;

    public static Role fromString(String role) {
        switch (role.toUpperCase().replace("-", "_")) {
            case "BATSMAN":
                return BATSMAN;
            case "BOWLER":
                return BOWLER;
            case "ALL_ROUNDER":
                return ALL_ROUNDER;
            default:
                throw new IllegalArgumentException("Unknown role: " + role);
        }
    }
}

class RunsComparator implements Comparator<Player> {
    @Override
    public int compare(Player p1, Player p2) {
        // Question 1: Write code for comparing/sorting runs in descending order [Total: 2 marks]
        // Return a negative value if the first player has more runs, 
        // a positive value if the second player has more runs, or zero if they have the same number of runs.
        return Integer.compare(p2.getRunsScored(), p1.getRunsScored());
    }
}
"""
semantics = codeDecomposition(solution)
for s in semantics:
    print(s)
    print("*****END******")
