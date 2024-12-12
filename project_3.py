# Symbol Table and Assembly Code Generator for Simplified Rat24F

# Initialize memory address
memory_address = 9000

# Symbol Table as a dictionary
symbol_table = {}

# Assembly code instruction list
assembly_code = []
instruction_index = 1

# Functions for Symbol Table Handling
def insert_identifier(lexeme):
    global memory_address
    if lexeme in symbol_table:
        raise ValueError(f"Error: Identifier '{lexeme}' already declared.")
    symbol_table[lexeme] = memory_address
    memory_address += 1

def lookup_identifier(lexeme):
    if lexeme not in symbol_table:
        raise ValueError(f"Error: Identifier '{lexeme}' undeclared.")
    return symbol_table[lexeme]

def print_symbol_table(output_stream):
    output_stream.write("\nSymbol Table:\n")
    output_stream.write("Identifier MemoryLocation Type\n")
    for lexeme, address in symbol_table.items():
        output_stream.write(f"{lexeme} {address} integer\n")

# Functions for Assembly Code Generation
def add_instruction(instruction, argument=None):
    global instruction_index
    if argument is not None:
        assembly_code.append(f"{instruction_index} {instruction} {argument}")
    else:
        assembly_code.append(f"{instruction_index} {instruction}")
    instruction_index += 1

def print_assembly_code(output_stream):
    output_stream.write("\nAssembly Code:\n")
    for line in assembly_code:
        output_stream.write(line + "\n")

# Lexer Class
class Lexer:
    def __init__(self, input_code, output):
        self.input_code = input_code
        self.tokens = []
        self.current_pos = 0
        self.output = output
        self.tokenize()

    def write_output(self, text):
        self.output.write(text + "\n")

    def tokenize(self):
        keywords = {'function', 'integer', 'if', 'else', 'while', 'put'}
        operators = {'+', '-', '=', '<', '>', '*', '/'}
        separators = {'(', ')', '{', '}', ';'}

        while self.current_pos < len(self.input_code):
            char = self.input_code[self.current_pos]
            if char in [' ', '\t', '\n']:
                self.current_pos += 1
                continue
            if char.isalpha():
                start_pos = self.current_pos
                while self.current_pos < len(self.input_code) and self.input_code[self.current_pos].isalnum():
                    self.current_pos += 1
                lexeme = self.input_code[start_pos:self.current_pos]
                token_type = 'KEYWORD' if lexeme in keywords else 'IDENTIFIER'
                self.tokens.append((token_type, lexeme))
                continue
            if char.isdigit():
                start_pos = self.current_pos
                while self.current_pos < len(self.input_code) and self.input_code[self.current_pos].isdigit():
                    self.current_pos += 1
                lexeme = self.input_code[start_pos:self.current_pos]
                self.tokens.append(('NUMBER', lexeme))
                continue
            if char in operators:
                self.tokens.append(('OPERATOR', char))
                self.current_pos += 1
                continue
            if char in separators:
                self.tokens.append(('SEPARATOR', char))
                self.current_pos += 1
                continue
            self.tokens.append(('MISMATCH', char))
            self.current_pos += 1

    def get_next_token(self):
        if self.tokens:
            return self.tokens.pop(0)
        return None

# Parser Class
class Parser:
    def __init__(self, lexer, output):
        self.lexer = lexer
        self.current_token = None
        self.output = output
        self.advance()

    def advance(self):
        self.current_token = self.lexer.get_next_token()

    def syntax_error(self, message):
        self.output.write(f"Syntax Error: {message}\n")
        raise ValueError(message)

    def parse_assignment(self):
        identifier = self.current_token[1]
        insert_identifier(identifier)
        self.advance()
        if self.current_token == ('OPERATOR', '='):
            self.advance()
            if self.current_token[0] == 'NUMBER':
                value = int(self.current_token[1])
                add_instruction("PUSHI", value)
                add_instruction("POPM", lookup_identifier(identifier))
                self.advance()
            else:
                self.syntax_error("Expected a number after '='")
        else:
            self.syntax_error("Expected '=' after identifier")

    def parse_print(self):
        if self.current_token[0] == 'IDENTIFIER':
            lexeme = self.current_token[1]
            add_instruction("PUSHM", lookup_identifier(lexeme))
            add_instruction("STDOUT")
            self.advance()
        else:
            self.syntax_error("Expected an identifier to print")

# Main Program
for i in range(1, 4):
    input_file = f"input{i}.txt"
    output_file = f"output{i}.txt"
    with open(input_file, "r") as f, open(output_file, "w") as output_stream:
        input_code = f.read()
        lexer = Lexer(input_code, output_stream)
        parser = Parser(lexer, output_stream)
        try:
            while parser.current_token:
                if parser.current_token[0] == 'IDENTIFIER':
                    parser.parse_assignment()
                elif parser.current_token == ('KEYWORD', 'put'):
                    parser.advance()
                    parser.parse_print()
                elif parser.current_token == ('SEPARATOR', ';'):
                    parser.advance()
                else:
                    parser.syntax_error(f"Unexpected token {parser.current_token}")
            print_assembly_code(output_stream)
            print_symbol_table(output_stream)
        except ValueError as e:
            output_stream.write(str(e) + "\n")
