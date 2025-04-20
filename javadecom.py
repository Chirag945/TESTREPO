from langchain_groq import ChatGroq
import json
from oopsol import solution
from java1 import code
from java2 import sort
class JavaCodeExtractor:
    def __init__(self, model_name: str, api_key: str, temperature: float = 0.2):
        self.chatgroq = ChatGroq(
            model_name=model_name,
            api_key=api_key,
            temperature=temperature
        )

    def extract_components(self, java_code: str):
        prompt = f"""
        Analyze the following Java code and extract its components in a structured format. Do not truncate body of classes, interfaces and methods.
        Return ONLY the JSON object with no additional text, comments, or explanations.]
        
        For each component, provide the following details:

        Classes(including nested classes):
        - Name
        - Modifiers (e.g., public, private, abstract, final, strictfp)
        - Fields (name only)
        - Methods (name only)
        - Constructors (name only)
        - Enclosing Class (name only)
        - Nested Classes or Interfaces (name only)
        - Super Class (name only)
        - Implemented Interfaces (name only)
        - Sub Class (name only)
        - Implementation (Body of the Class)
        - Brief description
        - Annotations

        Interfaces:
        - Name
        - Enclosing class (name only)
        - Modifiers (e.g., public, private, abstract, static)
        - Methods (name only)
        - Default methods (name only)
        - Implementation (Body of the interface)
        - Brief description
        - Annotations

        Methods:
        - Name
        - Enclosing class/interface (name only)
        - Modifiers (e.g., public, private, static, final, synchronized, native, abstract)
        - Return type
        - Parameters (with types)
        - Throws declarations
        - Implementation (Body of the method)
        - Brief description
        - Annotations

        Constructors:
        - Name
        - Enclosing class (name only)
        - Modifiers (e.g., public, private, protected)
        - Parameters (with types)
        - Throws declarations
        - Implementation (Body of the constructor)
        - Brief description
        - Annotations

        Fields:
        - Name
        -Enclosing class
        - Type
        - Modifiers (e.g., public, private, static, final, volatile, transient)
        - Initial value
        - Implementation (Field declaration line)
        - Usage context
        - Annotations

        Imports:
        - Package name
        - Static imports

        Java Code:
        {java_code}

        Return ONLY this JSON structure:
        {{
            "classes": [{{
                "class_name": "",
                "modifiers": ["modifier"],
                "fields": ["field_name"],
                "methods": ["method_name"],
                "constructors": ["constructor_name"],
                "enclosing_class": ["enclosing_class_name"]
                "nested_classes_or_interfaces": ["nested_name"],
                "sub_class": ["sub_class_name"],
                "super_class": ["super_class_name"],
                "implemented_interfaces": ["interface_name"],
                "implementation": "",
                "description": "",
                "annotations": ["annotation"]    
            }}],
            "interfaces": [{{
                "interface_name": "",
                "modifiers": ["modifier"],
                "methods": ["method_name"],
                "default_methods": ["default_method_name"],
                "enclosing_class": ["enclosing_class_name"],
                "implementation": "",
                "description": "",
                "annotations": ["annotation"]
            }}],
            "methods": [{{
                "method_name": "",
                "modifiers": ["modifier"],
                "return_type": "",
                "parameters": [{{"name": "", "type": ""}}],
                "throws": ["exception_type"],
                "enclosing_class": ["enclosing/interface_class_name"],
                "implementation": "",
                "description": "",
                "annotations": ["annotation"]
            }}],
            "constructors": [{{
                "constructor_name": "",
                "modifiers": ["modifier"],
                "parameters": [{{"name": "", "type": ""}}],
                "throws": ["exception_type"],
                "enclosing_class": ["enclosing_class_name"]
                "implementation": "",
                "description": "",
                "annotations": ["annotation"]
            }}],
            "fields": [{{
                "field_name": "",
                "type": "",
                "modifiers": ["modifier"],
                "enclosing_class": ["enclosing_class_name"]
                "initial_value": "",
                "implementation": "",
                "usage": "",
                "annotations": ["annotation"]
            }}],
            "imports": [{{
                "standard_imports": ["package_name"],
                "static_imports": ["static_import"]
            }}]
        }}"""
        response = self.chatgroq.invoke(prompt)

        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            
            return response.content

if __name__ == "__main__":
    
    java_code = code
    # def create_component_extraction_prompt(json_response):
    #     prompt = f"""
    #     Convert the following JSON structure into a flat list of components. Each component should be represented as a dictionary with 'type', 'name', and 'details' keys. Include all classes, interfaces, methods, constructors, and fields.

    #     JSON Input:
    #     {json_response}

    #     Return ONLY a Python list of dictionaries containing the components.
    #     """
    #     return prompt


# class ComponentProcessor:
#     def __init__(self, model_name: str, api_key: str):
#         self.chatgroq = ChatGroq(model_name=model_name, api_key=api_key)
    
#     def process_components(self, json_response):
#         prompt = create_component_extraction_prompt(json_response)
#         response = self.chatgroq.invoke(prompt)
#         try:
#             return json.loads(response.content)
#         except json.JSONDecodeError:
#             return response.content


if __name__ == "__main__":
    extractor = JavaCodeExtractor(model_name="llama-3.3-70b-versatile", api_key="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")
    json_result = extractor.extract_components(java_code)
    # editedreult=json_result.strip("json`")
    
    print (json_result)
    # print("\n\n")
    # print(editedreult)
    
    