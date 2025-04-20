def extract_component_names_with_counts(json_response):
    """
    Extracts component names from the JSON response of JavaCodeExtractor
    and returns them in a structured format along with counts.
    
    Args:
        json_response (dict): JSON response from JavaCodeExtractor
        
    Returns:
        tuple: (List of components, Dictionary of component counts)
    """
    components = []
    component_counts = {
        "classes": 0,
        "interfaces": 0,
        "methods": 0,
        "constructors": 0,
        "fields": 0
    }
    
    # Process Classes
    for class_info in json_response.get('classes', []):
        components.append({'type': 'class', 'name': class_info.get('class_name', '')})
        component_counts["classes"] += 1

    # Process Interfaces
    for interface in json_response.get('interfaces', []):
        components.append({'type': 'interface', 'name': interface.get('interface_name', '')})
        component_counts["interfaces"] += 1

    # Process Methods
    for method in json_response.get('methods', []):
        components.append({'type': 'method', 'name': method.get('method_name', '')})
        component_counts["methods"] += 1

    # Process Constructors
    for constructor in json_response.get('constructors', []):
        components.append({'type': 'constructor', 'name': constructor.get('constructor_name', '')})
        component_counts["constructors"] += 1

    # Process Fields
    for field in json_response.get('fields', []):
        components.append({'type': 'field', 'name': field.get('field_name', '')})
        component_counts["fields"] += 1

    return components, component_counts

# Example usage:
if __name__ == "__main__":
    # Example JSON response
    json_result = {
    "classes": [
        {
            "class_name": "AbstractVehicle",
            "modifiers": ["public", "abstract"],
            "fields": ["manufacturer", "running", "VALID_TYPES"],
            "methods": ["start", "stop", "getValidTypes"],
            "constructors": ["AbstractVehicle"],
            "enclosing_class": [],
            "nested_classes_or_interfaces": [],
            "sub_class": ["ElectricCar"],
            "super_class": ["Object"],
            "implemented_interfaces": ["Vehicle", "Maintainable"],
            "implementation": "public abstract class AbstractVehicle implements Vehicle, Maintainable {\n    protected final String manufacturer;\n    private volatile boolean running;\n    private static final List<String> VALID_TYPES;\n    \n    static {\n        List<String> types = new ArrayList<>();\n        types.add(\"Land\");\n        types.add(\"Air\");\n        types.add(\"Water\");\n        VALID_TYPES = unmodifiableList(types);\n    }\n    \n    protected AbstractVehicle(String manufacturer) {\n        this.manufacturer = manufacturer;\n    }\n    \n    @Override\n    public synchronized void start() {\n        running = true;\n        System.out.println(\"Vehicle starting\");\n    }\n    \n    @Override\n    public void stop() {\n        running = false;\n        System.out.println(\"Vehicle stopping\");\n    }\n    \n    public static List<String> getValidTypes() {\n        return VALID_TYPES;\n    }\n}",
            "description": "Abstract class representing a vehicle",
            "annotations": ["@Component"]
        },
        {
            "class_name": "ElectricCar",
            "modifiers": ["public"],
            "fields": ["batteryLevel", "oldField", "battery"],
            "methods": ["getType", "performMaintenance", "getBatteryLevel", "oldMethod"],
            "constructors": ["ElectricCar"],
            "enclosing_class": [],
            "nested_classes_or_interfaces": ["Battery"],
            "sub_class": [],
            "super_class": ["AbstractVehicle"],
            "implemented_interfaces": [],
            "implementation": "public class ElectricCar extends AbstractVehicle {\n    private transient int batteryLevel;\n    @Deprecated\n    private String oldField;\n    \n    public static class Battery {\n        private final int capacity;\n        \n        public Battery(int capacity) {\n            this.capacity = capacity;\n        }\n        \n        public int getCapacity() {\n            return capacity;\n        }\n    }\n    \n    private final Battery battery;\n    \n    public ElectricCar(String manufacturer, int batteryCapacity) {\n        super(manufacturer);\n        this.battery = new Battery(batteryCapacity);\n        this.batteryLevel = 100;\n    }\n    \n    @Override\n    public String getType() {\n        return \"Land\";\n    }\n    \n    @Override\n    public void performMaintenance() {\n        System.out.println(\"Performing electric car maintenance\");\n        batteryLevel = 100;\n    }\n    \n    public synchronized int getBatteryLevel() {\n        return batteryLevel;\n    }\n    \n    @Deprecated\n    public void oldMethod() throws IllegalStateException {\n        throw new IllegalStateException(\"This method is deprecated\");\n    }\n}",
            "description": "Class representing an electric car",
            "annotations": ["@Component"]
        },
        {
            "class_name": "Battery",
            "modifiers": ["public", "static"],
            "fields": ["capacity"],
            "methods": ["getCapacity"],
            "constructors": ["Battery"],
            "enclosing_class": ["ElectricCar"],
            "nested_classes_or_interfaces": [],
            "sub_class": [],
            "super_class": ["Object"],
            "implemented_interfaces": [],
            "implementation": "public static class Battery {\n        private final int capacity;\n        \n        public Battery(int capacity) {\n            this.capacity = capacity;\n        }\n        \n        public int getCapacity() {\n            return capacity;\n        }\n    }",
            "description": "Nested class representing a battery",
            "annotations": []
        }
    ],
    "interfaces": [
        {
            "interface_name": "Maintainable",
            "modifiers": ["public"],
            "methods": ["performMaintenance"],
            "default_methods": ["logMaintenance"],
            "enclosing_class": [],
            "implementation": "@FunctionalInterface\npublic interface Maintainable {\n    void performMaintenance();\n    \n    default void logMaintenance() {\n        System.out.println(\"Maintenance performed at: \" + System.currentTimeMillis());\n    }\n}",
            "description": "Interface representing a maintainable entity",
            "annotations": ["@FunctionalInterface"]
        },
        {
            "interface_name": "Vehicle",
            "modifiers": ["public"],
            "methods": ["start", "stop", "getType"],
            "default_methods": [],
            "enclosing_class": [],
            "implementation": "public interface Vehicle {\n    void start();\n    void stop();\n    String getType();\n}",    
            "description": "Interface representing a vehicle",
            "annotations": []
        }
    ],
    "methods": [
        {
            "method_name": "start",
            "modifiers": ["public", "synchronized"],
            "return_type": "void",
            "parameters": [],
            "throws": [],
            "enclosing_class": ["AbstractVehicle"],
            "implementation": "@Override\npublic synchronized void start() {\n    running = true;\n    System.out.println(\"Vehicle starting\");\n}",
            "description": "Method to start the vehicle",
            "annotations": []
        },
        {
            "method_name": "stop",
            "modifiers": ["public"],
            "return_type": "void",
            "parameters": [],
            "throws": [],
            "enclosing_class": ["AbstractVehicle"],
            "implementation": "@Override\npublic void stop() {\n    running = false;\n    System.out.println(\"Vehicle stopping\");\n}",
            "description": "Method to stop the vehicle",
            "annotations": []
        },
        {
            "method_name": "getValidTypes",
            "modifiers": ["public", "static"],
            "return_type": "List<String>",
            "parameters": [],
            "throws": [],
            "enclosing_class": ["AbstractVehicle"],
            "implementation": "public static List<String> getValidTypes() {\n    return VALID_TYPES;\n}",
            "description": "Method to get valid vehicle types",
            "annotations": []
        },
        {
            "method_name": "getType",
            "modifiers": ["public"],
            "return_type": "String",
            "parameters": [],
            "throws": [],
            "enclosing_class": ["ElectricCar"],
            "implementation": "@Override\npublic String getType() {\n    return \"Land\";\n}",
            "description": "Method to get the type of electric car",
            "annotations": []
        },
        {
            "method_name": "performMaintenance",
            "modifiers": ["public"],
            "return_type": "void",
            "parameters": [],
            "throws": [],
            "enclosing_class": ["ElectricCar"],
            "implementation": "@Override\npublic void performMaintenance() {\n    System.out.println(\"Performing electric car maintenance\");\n    batteryLevel = 100;\n}",
            "description": "Method to perform maintenance on electric car",
            "annotations": []
        },
        {
            "method_name": "getBatteryLevel",
            "modifiers": ["public", "synchronized"],
            "return_type": "int",
            "parameters": [],
            "throws": [],
            "enclosing_class": ["ElectricCar"],
            "implementation": "public synchronized int getBatteryLevel() {\n    return batteryLevel;\n}",
            "description": "Method to get the battery level of electric car",
            "annotations": []
        },
        {
            "method_name": "oldMethod",
            "modifiers": ["public"],
            "return_type": "void",
            "parameters": [],
            "throws": ["IllegalStateException"],
            "enclosing_class": ["ElectricCar"],
            "implementation": "@Deprecated\npublic void oldMethod() throws IllegalStateException {\n    throw new IllegalStateException(\"This method is deprecated\");\n}",
            "description": "Deprecated method",
            "annotations": ["@Deprecated"]
        },
        {
            "method_name": "getCapacity",
            "modifiers": ["public"],
            "return_type": "int",
            "parameters": [],
            "throws": [],
            "enclosing_class": ["Battery"],
            "implementation": "public int getCapacity() {\n    return capacity;\n}",
            "description": "Method to get the capacity of battery",
            "annotations": []
        },
        {
            "method_name": "logMaintenance",
            "modifiers": ["default"],
            "return_type": "void",
            "parameters": [],
            "throws": [],
            "enclosing_class": ["Maintainable"],
            "implementation": "default void logMaintenance() {\n    System.out.println(\"Maintenance performed at: \" + System.currentTimeMillis());\n}",
            "description": "Default method to log maintenance",
            "annotations": []
        }
    ],
    "constructors": [
        {
            "constructor_name": "AbstractVehicle",
            "modifiers": ["protected"],
            "parameters": [{"name": "manufacturer", "type": "String"}],
            "throws": [],
            "enclosing_class": ["AbstractVehicle"],
            "implementation": "protected AbstractVehicle(String manufacturer) {\n    this.manufacturer = manufacturer;\n}",   
            "description": "Constructor for abstract vehicle",
            "annotations": []
        },
        {
            "constructor_name": "ElectricCar",
            "modifiers": ["public"],
            "parameters": [{"name": "manufacturer", "type": "String"}, {"name": "batteryCapacity", "type": "int"}],
            "throws": [],
            "enclosing_class": ["ElectricCar"],
            "implementation": "public ElectricCar(String manufacturer, int batteryCapacity) {\n    super(manufacturer);\n    this.battery = new Battery(batteryCapacity);\n    this.batteryLevel = 100;\n}",
            "description": "Constructor for electric car",
            "annotations": []
        },
        {
            "constructor_name": "Battery",
            "modifiers": ["public"],
            "parameters": [{"name": "capacity", "type": "int"}],
            "throws": [],
            "enclosing_class": ["Battery"],
            "implementation": "public Battery(int capacity) {\n    this.capacity = capacity;\n}",
            "description": "Constructor for battery",
            "annotations": []
        }
    ],
    "fields": [
        {
            "field_name": "manufacturer",
            "type": "String",
            "modifiers": ["protected", "final"],
            "enclosing_class": ["AbstractVehicle"],
            "initial_value": "",
            "implementation": "protected final String manufacturer;",
            "usage": "Used to store the manufacturer of the vehicle",
            "annotations": []
        },
        {
            "field_name": "running",
            "type": "boolean",
            "modifiers": ["private", "volatile"],
            "enclosing_class": ["AbstractVehicle"],
            "initial_value": "",
            "implementation": "private volatile boolean running;",
            "usage": "Used to store the running state of the vehicle",
            "annotations": []
        },
        {
            "field_name": "VALID_TYPES",
            "type": "List<String>",
            "modifiers": ["private", "static", "final"],
            "enclosing_class": ["AbstractVehicle"],
            "initial_value": "",
            "implementation": "private static final List<String> VALID_TYPES;",
            "usage": "Used to store valid vehicle types",
            "annotations": []
        },
        {
            "field_name": "batteryLevel",
            "type": "int",
            "modifiers": ["private", "transient"],
            "enclosing_class": ["ElectricCar"],
            "initial_value": "",
            "implementation": "private transient int batteryLevel;",
            "usage": "Used to store the battery level of electric car",
            "annotations": []
        },
        {
            "field_name": "oldField",
            "type": "String",
            "modifiers": ["private", "deprecated"],
            "enclosing_class": ["ElectricCar"],
            "initial_value": "",
            "implementation": "@Deprecated\nprivate String oldField;",
            "usage": "Deprecated field",
            "annotations": ["@Deprecated"]
        },
        {
            "field_name": "battery",
            "type": "Battery",
            "modifiers": ["private", "final"],
            "enclosing_class": ["ElectricCar"],
            "initial_value": "",
            "implementation": "private final Battery battery;",
            "usage": "Used to store the battery of electric car",
            "annotations": []
        },
        {
            "field_name": "capacity",
            "type": "int",
            "modifiers": ["private", "final"],
            "enclosing_class": ["Battery"],
            "initial_value": "",
            "implementation": "private final int capacity;",
            "usage": "Used to store the capacity of battery",
            "annotations": []
        }
    ],
    "imports": {
        "standard_imports": ["java.util.List", "java.util.ArrayList", "org.springframework.stereotype.Component"],
        "static_imports": ["java.util.Collections.unmodifiableList"]
    }
}
    
    # Example usage:
if __name__ == "__main__":
    components, counts = extract_component_names_with_counts(json_result)
    print("Extracted Components:", components)
    print("Component Counts:", counts)
    # for component in components:
    #     print(f"\nType: {component['type']}")
    #     print(f"Name: {component['name']}")
    #     print("Details:", component['details'])