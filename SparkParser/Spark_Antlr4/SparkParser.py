from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass
from SparkLexer import SqlBaseLexer
# Assuming the SqlBaseLexer is in the same file or imported
# from lexer import SqlBaseLexer

@dataclass
class ASTNode:
    """Base class for AST nodes"""
    type: str
    value: Any = None
    children: List['ASTNode'] = None

    def __init__(self, type: str, value: Any = None, children: List['ASTNode'] = None):
        self.type = type
        self.value = value
        self.children = children or []

class SqlParser:
    def __init__(self, tokens: List[Tuple[int, str]]):
        self.tokens = tokens
        self.pos = 0
        self.lexer = SqlBaseLexer("")  # For token type constants

    def current_token(self) -> Optional[Tuple[int, str]]:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def advance(self):
        self.pos += 1
        # Skip whitespace tokens
        while self.pos < len(self.tokens) and self.current_token()[0] == self.lexer.WS:
            self.pos += 1

    def expect(self, token_type: int) -> str:
        self.skip_whitespace()
        token = self.current_token()
        if not token or token[0] != token_type:
            raise SyntaxError(f"Expected token type {token_type}, got {token}")
        value = token[1]
        self.advance()
        return value

    def skip_whitespace(self):
        while self.pos < len(self.tokens) and self.current_token()[0] == self.lexer.WS:
            self.pos += 1

    def parse_identifier(self) -> ASTNode:
        self.skip_whitespace()
        token = self.current_token()
        if not token:
            raise SyntaxError("Expected identifier, got EOF")
        
        if token[0] in (self.lexer.IDENTIFIER, self.lexer.BACKQUOTED_IDENTIFIER):
            value = self.expect(token[0])
            return ASTNode("IDENTIFIER", value)
        raise SyntaxError(f"Expected identifier, got {token}")

    def parse_expression(self) -> ASTNode:
        self.skip_whitespace()
        left = self.parse_term()
        
        token = self.current_token()
        if token and token[0] in (self.lexer.EQ, self.lexer.NEQ, self.lexer.LT, 
                                self.lexer.LTE, self.lexer.GT, self.lexer.GTE):
            operator = self.expect(token[0])
            right = self.parse_term()
            return ASTNode("BINARY_OP", operator, [left, right])
        
        return left

    def parse_term(self) -> ASTNode:
        self.skip_whitespace()
        token = self.current_token()
        if not token:
            raise SyntaxError("Expected term, got EOF")

        if token[0] == self.lexer.STRING:
            value = self.expect(self.lexer.STRING)
            return ASTNode("STRING", value)
        elif token[0] in (self.lexer.INTEGER_VALUE, self.lexer.DECIMAL_VALUE, 
                         self.lexer.BIGINT_LITERAL, self.lexer.FLOAT_LITERAL):
            value = self.expect(token[0])
            return ASTNode("NUMBER", value)
        elif token[0] in (self.lexer.IDENTIFIER, self.lexer.BACKQUOTED_IDENTIFIER):
            return self.parse_identifier()
        raise SyntaxError(f"Unexpected token in term: {token}")

    def parse_where_clause(self) -> Optional[ASTNode]:
        self.skip_whitespace()
        token = self.current_token()
        if token and token[0] == self.lexer.IDENTIFIER and token[1].upper() == "WHERE":
            self.advance()
            condition = self.parse_expression()
            return ASTNode("WHERE", children=[condition])
        return None

    def parse_from_clause(self) -> ASTNode:
        self.expect(self.lexer.IDENTIFIER)  # Expect "FROM"
        table = self.parse_identifier()
        return ASTNode("FROM", children=[table])

    def parse_select_list(self) -> List[ASTNode]:
        self.skip_whitespace()
        items = []
        token = self.current_token()
        
        if token[0] == self.lexer.ASTERISK:
            items.append(ASTNode("ALL_COLUMNS", "*"))
            self.advance()
        else:
            while True:
                items.append(self.parse_identifier())
                token = self.current_token()
                if not token or token[0] == self.lexer.IDENTIFIER and token[1].upper() == "FROM":
                    break
                if token and token[0] == self.lexer.COMMA:
                    self.advance()
                else:
                    break
        return items

    def parse_select(self) -> ASTNode:
        self.expect(self.lexer.IDENTIFIER)  # Expect "SELECT"
        select_items = self.parse_select_list()
        
        from_clause = None
        where_clause = None
        
        token = self.current_token()
        if token and token[0] == self.lexer.IDENTIFIER and token[1].upper() == "FROM":
            from_clause = self.parse_from_clause()
        
        where_clause = self.parse_where_clause()
        
        token = self.current_token()
        if token and token[0] == self.lexer.SEMICOLON:
            self.advance()

        children = select_items
        if from_clause:
            children.append(from_clause)
        if where_clause:
            children.append(where_clause)
            
        return ASTNode("SELECT", children=children)

    def parse(self) -> ASTNode:
        self.skip_whitespace()
        if not self.tokens:
            raise SyntaxError("Empty input")
        
        token = self.current_token()
        if token and token[0] == self.lexer.IDENTIFIER and token[1].upper() == "SELECT":
            return self.parse_select()
        raise SyntaxError(f"Unsupported statement type starting with {token}")

def pretty_print_ast(node: ASTNode, level: int = 0):
    """Helper function to print AST"""
    indent = "  " * level
    print(f"{indent}{node.type}: {node.value if node.value else ''}")
    for child in node.children:
        pretty_print_ast(child, level + 1)

# Test it
if __name__ == "__main__":
    sql = "SELECT id, name FROM users WHERE age > 18 ORDER BY name"
    lexer = SqlBaseLexer(sql)
    tokens = lexer.tokenize()
    
    parser = SqlParser(tokens)
    ast = parser.parse()
    
    print("AST Structure:")
    pretty_print_ast(ast)
    