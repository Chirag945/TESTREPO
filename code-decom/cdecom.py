from langchain_groq import ChatGroq
import json

class CCodeExtractor:
    def __init__(self, model_name: str, api_key: str, temperature: float = 0.7):
        self.chatgroq = ChatGroq(
            model_name=model_name,
            api_key=api_key,
            temperature=temperature
        )
    
    def extract_components(self, c_code: str):
        prompt = f"""
        Analyze the following C code and extract its components in a structured format.
        Return ONLY the JSON object with no additional text, comments, or explanations.
        
        For each component, provide the following details:
        
        Functions:
        - Name
        - Return type
        - Parameters (with types)
        - Implementation
        - Brief description
        
        Structs:
        - Name
        - Fields (with types and descriptions)
        - Typedef names
        - Usage context
        
        Enums:
        - Name
        - Values (with implicit values calculated)
        - Typedef names
        - Usage context
        
        Global Variables:
        - Name
        - Type
        - Initial value
        - Usage context
        
        C Code:
        {c_code}
        
        Return ONLY this JSON structure:
        {{
            "functions": {{
                "function_name": {{
                    "return_type": "",
                    "parameters": [{{"name": "", "type": ""}}],
                    "implementation": "",
                    "description": ""
                }}
            }},
            "structs": {{
                "struct_name": {{
                    "typedef_name": "",
                    "fields": [{{
                        "name": "",
                        "type": "",
                        "description": ""
                    }}],
                    "usage": ""
                }}
            }},
            "enums": {{
                "enum_name": {{
                    "typedef_name": "",
                    "values": [{{
                        "name": "",
                        "value": 0
                    }}],
                    "usage": ""
                }}
            }},
            "globals": {{
                "variable_name": {{
                    "type": "",
                    "value": "",
                    "usage": ""
                }}
            }}
        }}"""
        response = self.chatgroq.invoke(prompt)
        # Convert string response to JSON
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            # If response is not valid JSON, return raw content
            return response.content

if __name__ == "__main__":
    # Example C code
    c_code = """
// C program to pairwise swap elements
// in a given linked list

#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node* next;
};

// Recursive function to swap data of nodes in pairs
void pairwiseSwap(struct Node* head) {
    
    // Base case: if the list is empty or has
      // only one node, no swap
    if (head == NULL || head->next == NULL) {
        return;
    }

    // Swap the data of the current node with the next node
    int temp = head->data;
    head->data = head->next->data;
    head->next->data = temp;

    // Recursion for the next pair
    pairwiseSwap(head->next->next);
}

void printList(struct Node* head) {
    struct Node* curr = head;
    while (curr != NULL) {
        printf("%d ", curr->data);
        curr = curr->next;
    }
    printf("\n");
}

struct Node* createNode(int val) {
    struct Node* newNode = 
      (struct Node*)malloc(sizeof(struct Node));
    newNode->data = val;
    newNode->next = NULL;
    return newNode;
}

int main() {
    
    // Creating the linked list: 
      // 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> NULL
    struct Node* head = createNode(1);
    head->next = createNode(2);
    head->next->next = createNode(3);
    head->next->next->next = createNode(4);
    head->next->next->next->next = createNode(5);
    head->next->next->next->next->next = createNode(6);

    pairwiseSwap(head);
    
    printList(head);

    return 0;
}
    """

  

    extractor = CCodeExtractor(model_name="llama-3.3-70b-versatile", api_key="api_key")
    result = extractor.extract_components(c_code)
    print("Extracted Components:")
    print(result)
