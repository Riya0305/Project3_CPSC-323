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
                self.write_output(f"Token: {token_type} Lexeme: {lexeme}")
                continue

            if char.isdigit():
                start_pos = self.current_pos
                while self.current_pos < len(self.input_code) and self.input_code[self.current_pos].isdigit():
                    self.current_pos += 1
                lexeme = self.input_code[start_pos:self.current_pos]
                self.tokens.append(('NUMBER', lexeme))
                self.write_output(f"Token: NUMBER Lexeme: {lexeme}")
                continue

            if char in operators:
                self.tokens.append(('OPERATOR', char))
                self.write_output(f"Token: OPERATOR Lexeme: {char}")
                self.current_pos += 1
                continue

            if char in separators:
                self.tokens.append(('SEPARATOR', char))
                self.write_output(f"Token: SEPARATOR Lexeme: {char}")
                self.current_pos += 1
                continue

            self.tokens.append(('MISMATCH', char))
            self.write_output(f"Token: MISMATCH Lexeme: {char}")
            self.current_pos += 1

    def get_next_token(self):
        if self.tokens:
            return self.tokens.pop(0)
        return None
