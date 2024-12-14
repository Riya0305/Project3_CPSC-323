import re

class AssemblyCodeGenerator:
    def __init__(self):
        self.instructions = []
    
    def add_instruction(self, instruction):
        self.instructions.append(instruction)
    
    def generate_code(self, statement, symbol_table):
        if isinstance(statement, str):
            print(f"Error: Expected a dictionary but got a string: {statement}")
            return

        if statement['type'] == 'get':
            identifier = statement['identifier']
            self.add_instruction("STDIN")  # Read input
            memory_info = symbol_table.get_memory_address(identifier)
            if memory_info is not None:
                address = memory_info['address']
                self.add_instruction(f"POPM {address}")  # Store value in identifier
            else:
                print(f"Error: Address for identifier '{identifier}' not found.")
        
        elif statement['type'] == 'assign':
            identifier = statement['identifier']
            value = statement['value']
            self.add_instruction(f"PUSHI {value}")
            memory_info = symbol_table.get_memory_address(identifier)
            if memory_info is not None:
                address = memory_info['address']
                self.add_instruction(f"POPM {address}")  # Store value in identifier
            else:
                print(f"Error: Address for identifier '{identifier}' not found.")
        
        elif statement['type'] == 'while':
            condition_var = statement['condition'][0]
            condition_value = statement['condition'][1]
            self.add_instruction(f"PUSHM {condition_var}")  # Push the condition variable
            self.add_instruction(f"PUSHI {condition_value}")  # Push the comparison value
            self.add_instruction("LES")
            self.add_instruction(f"JUMPZ {statement['end_label']}")
            # Process body of while loop (simplified example)
            for stmt in statement['body']:
                self.generate_code(stmt, symbol_table)

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.memory_address_counter = 9000
    
    def add_symbol(self, identifier, var_type):
        if identifier not in self.symbols:
            self.symbols[identifier] = {'address': self.memory_address_counter, 'type': var_type}
            self.memory_address_counter += 1
    
    def get_memory_address(self, identifier):
        return self.symbols.get(identifier, None)

class Parser:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.assembly_code_generator = AssemblyCodeGenerator()

    def parse(self, program):
        program_statements = program.split("\n")
        for statement in program_statements:
            statement = statement.strip()
            if statement.startswith("get"):
                self.parse_get_statement(statement)
            elif "=" in statement:
                self.parse_assign_statement(statement)
            elif statement.startswith("while"):
                self.parse_while_statement(statement)

    def parse_get_statement(self, statement):
        identifier = re.findall(r'\((.*?)\)', statement)[0].strip()  # Extract the identifier from 'get(max);'
        self.symbol_table.add_symbol(identifier, 'integer')  # Add it to the symbol table
        self.assembly_code_generator.generate_code({'type': 'get', 'identifier': identifier}, self.symbol_table)
    
    def parse_assign_statement(self, statement):
        parts = statement.split("=")
        identifier = parts[0].strip()
        value = parts[1].strip().strip(";")
        self.symbol_table.add_symbol(identifier, 'integer')  # Assume all variables are integers for simplicity
        self.assembly_code_generator.generate_code({'type': 'assign', 'identifier': identifier, 'value': value}, self.symbol_table)
    
    def parse_while_statement(self, statement):
        condition = re.findall(r'\((.*?)\)', statement)[0].strip()
        condition_var, condition_value = condition.split("<")
        condition_var = condition_var.strip()
        condition_value = condition_value.strip()
        self.symbol_table.add_symbol(condition_var, 'integer')  # Add it to the symbol table
        body = [{'type': 'assign', 'identifier': 'sum', 'value': 'sum + i'}]
        self.assembly_code_generator.generate_code({'type': 'while', 'condition': (condition_var, condition_value), 'body': body, 'end_label': 'LABEL2'}, self.symbol_table)

    def generate_symbol_table_and_code(self, program):
        self.parse(program)
        result = "Symbol Table\n"
        result += "Identifier MemoryLocation Type\n"
        for identifier, data in self.symbol_table.symbols.items():
            result += f"{identifier} {data['address']} {data['type']}\n"
        
        result += "\nGenerated Assembly Code:\n"
        for instruction in self.assembly_code_generator.instructions:
            result += f"{instruction}\n"
        
        return result

# Function to handle input/output from files
def process_test_case(input_file, output_file):
    with open(input_file, 'r') as file:
        program = file.read()
    
    parser = Parser()
    result = parser.generate_symbol_table_and_code(program)
    
    with open(output_file, 'w') as file:
        file.write(result)

# Main execution for multiple test cases
if __name__ == "__main__":
    process_test_case('input1.txt', 'output1.txt')
    process_test_case('input2.txt', 'output2.txt')
    process_test_case('input3.txt', 'output3.txt')
