from langchain_groq import ChatGroq
import json
from java3 import code
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
        Analyze the following Java code and extract its components in a structured format with their dependencies. 
        Do not truncate body of classes, interfaces and methods.
        Return ONLY the JSON object with no additional text, comments, or explanations.
        Identify all syntax errors and do not fix any syntax errors.
        
        For each component, provide the following details including dependencies:

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
        - Dependencies:
          - Inherited methods (list methods inherited from superclass)
          - Overridden methods (list methods that override superclass)
          - Interface implementations (list methods implementing interfaces)
          - Field dependencies (fields used by which methods)
          - Method dependencies (methods called by other methods)
        - Brief description

        Interfaces:
        - Name
        - Enclosing class (name only)
        - Modifiers (e.g., public, private, abstract, static)
        - Methods (name only)
        - Default methods (name only)
        - Implementation (Body of the interface)
        - Dependencies:
          - Implementing classes (list of classes implementing this interface)
          - Extended interfaces (list of interfaces this interface extends)
        - Brief description

        Methods:
        - Name
        - Enclosing class/interface (name only)
        - Modifiers (e.g., public, private, static, final, synchronized, native, abstract)
        - Return type
        - Parameters (with types)
        - Throws declarations
        - Implementation (Body of the method)
        - Dependencies:
          - Called methods (list of methods this method calls)
          - Used fields (list of fields this method uses)
          - Overridden method (if this method overrides a superclass method)
          - Interface implementation (if this method implements an interface method)
        - Brief description

        Constructors:
        - Name
        - Enclosing class (name only)
        - Modifiers (e.g., public, private, protected)
        - Parameters (with types)
        - Throws declarations
        - Implementation (Body of the constructor)
        - Dependencies:
          - Constructor chaining (this() calls)
          - Super constructor calls
          - Field initializations
          - Method calls
        - Brief description

        Fields:
        - Name
        - Enclosing class
        - Type
        - Modifiers (e.g., public, private, static, final, volatile, transient)
        - Initial value
        - Implementation (Field declaration line)
        - Dependencies:
          - Methods using this field
          - Shadowed fields (if this field shadows a superclass field)
          - Initialization dependencies (other fields/methods used in initialization)
        - Usage context

        Imports:
        - Package name
        - Static imports
        - Dependencies:
          - Used by which classes/methods

        If any item of the JSON is not present, the corresponding output should be an empty string or list as applicable, strictly do NOT give null output in those cases under any circumstances.
        Java Code:
        {java_code}
        Return this JSON structure with dependencies included in each component:
        {{
            "classes": [{{
                "class_name": "",
                "modifiers": ["modifier"],
                "fields": ["field_name"],
                "methods": ["method_name"],
                "constructors": ["constructor_name"],
                "enclosing_class": ["enclosing_class_name"],
                "nested_classes_or_interfaces": ["nested_name"],
                "super_class": ["super_class_name"],
                "implemented_interfaces": ["interface_name"],
                "sub_class": ["sub_class_name"],
                "implementation": "",
                "dependencies": {{
                    "inherited_methods": ["method_name"],
                    "overridden_methods": ["method_name"],
                    "interface_implementations": ["method_name"],
                    "field_dependencies": [{{"field": "field_name", "used_by": ["method_name"]}}],
                    "method_dependencies": [{{"method": "method_name", "calls": ["method_name"]}}]
                }},
                "description": ""
            }}],
            "interfaces": [{{
                "interface_name": "",
                "modifiers": ["modifier"],
                "methods": ["method_name"],
                "default_methods": ["default_method_name"],
                "enclosing_class": ["enclosing_class_name"],
                "implementation": "",
                "dependencies": {{
                    "implementing_classes": ["class_name"],
                    "extended_interfaces": ["interface_name"]
                }},
                "description": ""
            }}],
            "methods": [{{
                "method_name": "",
                "modifiers": ["modifier"],
                "return_type": "",
                "parameters": [{{"name": "", "type": ""}}],
                "throws": ["exception_type"],
                "enclosing_class": ["enclosing_class_name"],
                "implementation": "",
                "dependencies": {{
                    "called_methods": ["method_name"],
                    "used_fields": ["field_name"],
                    "overrides": "superclass_method_name",
                    "implements": "interface_method_name"
                }},
                "description": ""
            }}],
            "constructors": [{{
                "constructor_name": "",
                "modifiers": ["modifier"],
                "parameters": [{{"name": "", "type": ""}}],
                "throws": ["exception_type"],
                "enclosing_class": ["enclosing_class_name"],
                "implementation": "",
                "dependencies": {{
                    "constructor_chaining": "constructor_name",
                    "super_constructor": true,
                    "initialized_fields": ["field_name"],
                    "called_methods": ["method_name"]
                }},
                "description": ""
            }}],
            "fields": [{{
                "field_name": "",
                "type": "",
                "modifiers": ["modifier"],
                "enclosing_class": ["enclosing_class_name"],
                "initial_value": "",
                "implementation": "",
                "dependencies": {{
                    "used_by_methods": ["method_name"],
                    "shadows_field": "superclass_field_name",
                    "initialization_dependencies": ["field_or_method_name"]
                }},
                "description": ""
            }}],
            "imports": [{{
                "standard_imports": ["package_name"],
                "static_imports": ["static_import"],
                "dependencies": {{
                    "used_by": ["class_or_method_name"]
                }}
            }}]
        }}"""
        
        response = self.chatgroq.invoke(prompt)
        cleaned_response = response.content.strip("```")  # Remove surrounding triple backticks
        cleaned_response = cleaned_response.replace("json", "", 1).strip()  # Remove "json" specifier
        print(cleaned_response)
        try:
            print("sending json")
            return json.loads(cleaned_response)
        except json.JSONDecodeError:
            print("json failed")
            return cleaned_response

    def first_pass_analyze_component(self, component: dict, component_type: str):
        """First pass."""
        details = self.prepare_analysis_prompt(component, component_type)
        
        prompt = f"""
        {details['name']}, {component_type}: Analyze this Java component.

        Component Details:
        {details['component_details']}
        
        Implementation:
        {details['implementation']}

        Original Description:
        {details['description']}
        
        Provide a brief technical analysis in less than 50 words.
        """
        response = self.chatgroq.invoke(prompt)
        try:
            analysis = response.content.strip()
        except Exception:
            analysis = "Analysis could not be generated."
        
        component["first_Pass_Analysis"] = analysis
        # print(analysis)
        return component
    
    def second_pass_analyze_component(self, component: dict, component_type: str):
        """Second pass"""
        details = self.prepare_analysis_prompt(component, component_type)
        
        prompt = f"""
        {details['name']}, {component_type}: Give a detailed analysis of this Java component given the following.

        Component Details:
        {details['component_details']}
        
        Implementation:
        {details['implementation']}

        Original Description:
        {details['description']}

        Dependencies:
        {details['dependencies']}

        initial_analysis:
        {details['first_Pass_Analysis']}


        Cover the following points in your analysis:
        1. Component Overview: Provide a high-level description of the component, including its purpose, role in an application, and key use cases.
        2. Functionality: Describe the primary functions and capabilities of the component. Highlight any specific logic it implements.
        3. Implementation Details: Discuss the design of the component. Explain how it interacts with other components. Explain key data structures or algorithms used (if any), only if the component was a method.
        Do NOT provide any sample implementation. Focus on the design and functionality of the component.
        """
        
        response = self.chatgroq.invoke(prompt)
        try:
            analysis = response.content.strip()
        except Exception:
            analysis = "Analysis could not be generated."
        
        component["second_Pass_Analysis"] = analysis
        # print(analysis)
        return component



    def prepare_analysis_prompt(self, component: dict, component_type: str):
        """Prepares the structured analysis details for a Java component."""
        details = {}

        if component_type == "classes":
            details["name"]=component.get('class_name', 'Not specified')
            details["component_details"] = f"""
            Class Name: {component.get('class_name', 'Not specified')}
            Modifiers: {', '.join(component.get('modifiers', []))}
            Fields: {', '.join(component.get('fields', []))}
            Methods: {', '.join(component.get('methods', []))}
            Constructors: {', '.join(component.get('constructors', []))}
            Enclosing Class: {', '.join(component.get('enclosing_class', []))}
            Nested Classes/Interfaces: {', '.join(component.get('nested_classes_or_interfaces', []))}
            Super Class: {', '.join(component.get('super_class', []))}
            Implemented Interfaces: {', '.join(component.get('implemented_interfaces', []))}
            Sub Class: {', '.join(component.get('sub_class', []))}
            """

        elif component_type == "methods":
            details["name"]=component.get('method_name', 'Not specified')
            details["component_details"] = f"""
            Method Name: {component.get('method_name', 'Not specified')}
            Modifiers: {', '.join(component.get('modifiers', []))}
            Return Type: {component.get('return_type', 'Not specified')}
            Parameters: {', '.join(f"{p.get('name')}: {p.get('type')}" for p in component.get('parameters', []))}
            Throws: {', '.join(component.get('throws', []))}
            Enclosing Class: {', '.join(component.get('enclosing_class', []))}
            """

        elif component_type == "interfaces":
            details["name"]=component.get('interface_name', 'Not specified')
            details["component_details"] = f"""
            Interface Name: {component.get('interface_name', 'Not specified')}
            Modifiers: {', '.join(component.get('modifiers', []))}
            Methods: {', '.join(component.get('methods', []))}
            Default Methods: {', '.join(component.get('default_methods', []))}
            Enclosing Class: {', '.join(component.get('enclosing_class', []))}
            """

        elif component_type == "constructors":
            details["name"]=component.get('constructor_name', 'Not specified')
            details["component_details"] = f"""
            Constructor Name: {component.get('constructor_name', 'Not specified')}
            Modifiers: {', '.join(component.get('modifiers', []))}
            Parameters: {', '.join(f"{p.get('name')}: {p.get('type')}" for p in component.get('parameters', []))}
            Throws: {', '.join(component.get('throws', []))}
            Enclosing Class: {', '.join(component.get('enclosing_class', []))}
            """

        elif component_type == "fields":
            details["name"]=component.get('field_name', 'Not specified')
            details["component_details"] = f"""
            Field Name: {component.get('field_name', 'Not specified')}
            Type: {component.get('type', 'Not specified')}
            Modifiers: {', '.join(component.get('modifiers', []))}
            Initial Value: {component.get('initial_value', 'Not specified')}
            Enclosing Class: {', '.join(component.get('enclosing_class', []))}
            """
        details['dependencies']=component.get('dependencies', 'Not provided')
        details["implementation"] = component.get('se', 'Not provided')
        details["description"] = component.get('description', 'Not provided')
        details["first_Pass_Analysis"] = component.get('first_Pass_Analysis', 'Not provided')
        return details

    def remove_implementation(self, components_dict):
        """Removes the implementation field from all components in the dictionary."""
        for component_type in components_dict:
            if isinstance(components_dict[component_type], list):
                for component in components_dict[component_type]:
                    if isinstance(component, dict) and 'implementation' in component:
                        del component['implementation']
        return components_dict

    def process_and_analyze(self, java_code: str):
        """
        Process and analyze Java code with dependencies included in initial extraction.
        """
        # Extract components with dependencies
        '''extracted_components = {
    "classes": [
        {
            "class_name": "BubbleSort",
            "modifiers": ["public"],
            "fields": [],
            "methods": ["bubbleSort", "printArray", "main"],
            "constructors": [],
            "enclosing_class": [],
            "nested_classes_or_interfaces": [],
            "super_class": ["Object"],
            "implemented_interfaces": [],
            "sub_class": [],
            "implementation": "public class BubbleSort {\n    public static void bubbleSort(int[] arr) {\n        int n = arr.length;\n        \n        // Outer loop - number of passes\n        for (int i = 0; i < n - 1; i++) {\n            // Flag to optimize - if no swaps occur, array is sorted\n            boolean swapped = false;\n            \n            // Inner loop - comparing adjacent elements\n            for (int j = 0; j < n - i - 1; j++) {\n                // Compare adjacent elements\n                if (arr[j] > arr[j + 1]) {\n                    // Swap arr[j] and arr[j + 1]\n                    int temp = arr[j];\n                    arr[j] = arr[j + 1];\n                    arr[j + 1] = temp;\n                    swapped = true;\n                }\n            }\n            \n            // If no swapping occurred, array is sorted\n            if (!swapped) {\n                break;\n            }\n        }\n    }\n\n    // Utility method to print array\n    public static void printArray(int[] arr) {\n        for (int i = 0; i < arr.length; i++) {\n            System.out.print(arr[i] + \" \");\n        }\n        System.out.println();\n    }\n\n    // Main method with example usage\n    public static void main(String[] args) {\n        int[] arr = {64, 34, 25, 12, 22, 11, 90};\n        \n        System.out.println(\"Original array:\");\n        printArray(arr);\n        \n        bubbleSort(arr);\n        \n        System.out.println(\"Sorted array:\");\n        printArray(arr);\n    }\n}",
            "dependencies": {
                "inherited_methods": ["toString", "equals", "hashCode", "getClass", "wait", "notify", "notifyAll"],
                "overridden_methods": [],
                "interface_implementations": [],
                "field_dependencies": [],
                "method_dependencies": [
                    {"method": "bubbleSort", "calls": ["printArray"]},
                    {"method": "printArray", "calls": []},
                    {"method": "main", "calls": ["printArray", "bubbleSort"]}
                ]
            },
            "description": "This class implements the Bubble Sort algorithm to sort an array of integers in ascending order."
        }
    ],
    "interfaces": [],
    "methods": [
        {
            "method_name": "bubbleSort",
            "modifiers": ["public", "static"],
            "return_type": "void",
            "parameters": [{"name": "arr", "type": "int[]"}],
            "throws": [],
            "enclosing_class": ["BubbleSort"],
            "implementation": "public static void bubbleSort(int[] arr) {\n        int n = arr.length;\n        \n        // Outer loop - number of passes\n        for (int i = 0; i < n - 1; i++) {\n            // Flag to optimize - if no swaps occur, array is sorted\n            boolean swapped = false;\n            \n            // Inner loop - comparing adjacent elements\n            for (int j = 0; j < n - i - 1; j++) {\n                // Compare adjacent elements\n                if (arr[j] > arr[j + 1]) {\n                    // Swap arr[j] and arr[j + 1]\n                    int temp = arr[j];\n                    arr[j] = arr[j + 1];\n                    arr[j + 1] = temp;\n                    swapped = true;\n                }\n            }\n            \n            // If no swapping occurred, array is sorted\n            if (!swapped) {\n                break;\n            }\n        }\n    }",
            "dependencies": {
                "called_methods": [],
                "used_fields": [],
                "overrides": "",
                "implements": ""
            },
            "description": "This method sorts an array of integers in ascending order using the Bubble Sort algorithm."
        },
        {
            "method_name": "printArray",
            "modifiers": ["public", "static"],
            "return_type": "void",
            "parameters": [{"name": "arr", "type": "int[]"}],
            "throws": [],
            "enclosing_class": ["BubbleSort"],
            "implementation": "public static void printArray(int[] arr) {\n        for (int i = 0; i < arr.length; i++) {\n            System.out.print(arr[i] + \" \");\n        }\n        System.out.println();\n    }",
            "dependencies": {
                "called_methods": [],
                "used_fields": [],
                "overrides": "",
                "implements": ""
            },
            "description": "This method prints the elements of an array to the console."
        },
        {
            "method_name": "main",
            "modifiers": ["public", "static"],
            "return_type": "void",
            "parameters": [{"name": "args", "type": "String[]"}],
            "throws": [],
            "enclosing_class": ["BubbleSort"],
            "implementation": "public static void main(String[] args) {\n        int[] arr = {64, 34, 25, 12, 22, 11, 90};\n        \n        System.out.println(\"Original array:\");\n        printArray(arr);\n        \n        bubbleSort(arr);\n        \n        System.out.println(\"Sorted array:\");\n        printArray(arr);\n    }",
            "dependencies": {
                "called_methods": ["printArray", "bubbleSort"],
                "used_fields": [],
                "overrides": "",
                "implements": ""
            },
            "description": "This is the main method that demonstrates the usage of the Bubble Sort algorithm."
        }
    ],
    "constructors": [],
    "fields": [],
    "imports": [
        {
            "standard_imports": ["java.lang"],
            "static_imports": [],
            "dependencies": {
                "used_by": ["BubbleSort"]
            }
        }
    ]
}'''
        extracted_components = self.extract_components(java_code)
        print(type(extracted_components))

        analyzed_components = {
            "classes": [],
            "interfaces": [],
            "methods": [],
            "constructors": [],
            "fields": []
        }
        
        for comp_type in analyzed_components.keys():
            for comp in extracted_components.get(comp_type, []):
                analyzed_components[comp_type].append(
                    self.first_pass_analyze_component(comp, comp_type)
                )
        for comp_type in analyzed_components.keys():
            for comp in extracted_components.get(comp_type, []):
                analyzed_components[comp_type].append(
                    self.second_pass_analyze_component(comp, comp_type)
                )
        
        return analyzed_components


if __name__ == "__main__":
    extractor = JavaCodeExtractor(
        model_name="llama-3.3-70b-versatile",
        #api_key="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"
        api_key="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"
    )
    analyzed_result = extractor.process_and_analyze(code)
    cleaned_result = extractor.remove_implementation(analyzed_result)
    print(json.dumps(cleaned_result, indent=2))