import re
from typing import List, Tuple

class SqlBaseLexer:
    # Token types as constants
    (
        SEMICOLON, LEFT_PAREN, RIGHT_PAREN, COMMA, DOT, LEFT_BRACKET, RIGHT_BRACKET,
        EQ, NSEQ, NEQ, NEQJ, LT, LTE, GT, GTE, PLUS, MINUS, ASTERISK, SLASH, PERCENT,
        TILDE, AMPERSAND, PIPE, CONCAT_PIPE, HAT, COLON, ARROW, HENT_START, HENT_END,
        STRING, DOUBLEQUOTED_STRING, BIGINT_LITERAL, SMALLINT_LITERAL, TINYINT_LITERAL,
        INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, FLOAT_LITERAL, DOUBLE_LITERAL,
        BIGDECIMAL_LITERAL, IDENTIFIER, BACKQUOTED_IDENTIFIER, SIMPLE_COMMENT,
        BRACKETED_COMMENT, WS, UNRECOGNIZED
    ) = range(46)

    # Keyword map
    KEYWORDS = {
        'ADD': 'ADD', 'AFTER': 'AFTER', 'ALL': 'ALL', 'ALTER': 'ALTER', 'ALWAYS': 'ALWAYS',
        'ANALYZE': 'ANALYZE', 'AND': 'AND', 'ANTI': 'ANTI', 'ANY': 'ANY', 'ANY_VALUE': 'ANY_VALUE',
        'ARCHIVE': 'ARCHIVE', 'ARRAY': 'ARRAY', 'AS': 'AS', 'ASC': 'ASC', 'AT': 'AT',
        'AUTHORIZATION': 'AUTHORIZATION', 'BETWEEN': 'BETWEEN', 'BOTH': 'BOTH', 'BUCKET': 'BUCKET',
        'BUCKETS': 'BUCKETS', 'BY': 'BY', 'CACHE': 'CACHE', 'CASCADE': 'CASCADE', 'CASE': 'CASE',
        'CAST': 'CAST', 'CATALOG': 'CATALOG', 'CATALOGS': 'CATALOGS', 'CHANGE': 'CHANGE',
        'CHECK': 'CHECK', 'CLEAR': 'CLEAR', 'CLUSTER': 'CLUSTER', 'CLUSTERED': 'CLUSTERED',
        'CODEGEN': 'CODEGEN', 'COLLATE': 'COLLATE', 'COLLECTION': 'COLLECTION', 'COLUMN': 'COLUMN',
        'COLUMNS': 'COLUMNS', 'COMMENT': 'COMMENT', 'COMMIT': 'COMMIT', 'COMPACT': 'COMPACT',
        'COMPACTIONS': 'COMPACTIONS', 'COMPUTE': 'COMPUTE', 'CONCATENATE': 'CONCATENATE',
        'CONSTRAINT': 'CONSTRAINT', 'COST': 'COST', 'CREATE': 'CREATE', 'CROSS': 'CROSS',
        'CUBE': 'CUBE', 'CURRENT': 'CURRENT', 'CURRENT_DATE': 'CURRENT_DATE',
        'CURRENT_TIME': 'CURRENT_TIME', 'CURRENT_TIMESTAMP': 'CURRENT_TIMESTAMP',
        'CURRENT_USER': 'CURRENT_USER', 'DAY': 'DAY', 'DAYS': 'DAYS', 'DAYOFYEAR': 'DAYOFYEAR',
        'DATA': 'DATA', 'DATABASE': 'DATABASE', 'DATABASES': 'DATABASES', 'DATEADD': 'DATEADD',
        'DATEDIFF': 'DATEDIFF', 'DBPROPERTIES': 'DBPROPERTIES', 'DEFAULT': 'DEFAULT',
        'DEFINED': 'DEFINED', 'DELETE': 'DELETE', 'DELIMITED': 'DELIMITED', 'DESC': 'DESC',
        'DESCRIBE': 'DESCRIBE', 'DFS': 'DFS', 'DIRECTORIES': 'DIRECTORIES', 'DIRECTORY': 'DIRECTORY',
        'DISTINCT': 'DISTINCT', 'DISTRIBUTE': 'DISTRIBUTE', 'DIV': 'DIV', 'DROP': 'DROP',
        'ELSE': 'ELSE', 'END': 'END', 'ESCAPE': 'ESCAPE', 'ESCAPED': 'ESCAPED', 'EXCEPT': 'EXCEPT',
        'EXCHANGE': 'EXCHANGE', 'EXCLUDE': 'EXCLUDE', 'EXISTS': 'EXISTS', 'EXPLAIN': 'EXPLAIN',
        'EXPORT': 'EXPORT', 'EXTENDED': 'EXTENDED', 'EXTERNAL': 'EXTERNAL', 'EXTRACT': 'EXTRACT',
        'FALSE': 'FALSE', 'FETCH': 'FETCH', 'FIELDS': 'FIELDS', 'FILTER': 'FILTER',
        'FILEFORMAT': 'FILEFORMAT', 'FIRST': 'FIRST', 'FOLLOWING': 'FOLLOWING', 'FOR': 'FOR',
        'FOREIGN': 'FOREIGN', 'FORMAT': 'FORMAT', 'FORMATTED': 'FORMATTED', 'FROM': 'FROM',
        'FULL': 'FULL', 'FUNCTION': 'FUNCTION', 'FUNCTIONS': 'FUNCTIONS', 'GENERATED': 'GENERATED',
        'GLOBAL': 'GLOBAL', 'GRANT': 'GRANT', 'GROUP': 'GROUP', 'GROUPING': 'GROUPING',
        'HAVING': 'HAVING', 'HOUR': 'HOUR', 'HOURS': 'HOURS', 'IF': 'IF', 'IGNORE': 'IGNORE',
        'IMPORT': 'IMPORT', 'IN': 'IN', 'INCLUDE': 'INCLUDE', 'INDEX': 'INDEX', 'INDEXES': 'INDEXES',
        'INNER': 'INNER', 'INPATH': 'INPATH', 'INPUTFORMAT': 'INPUTFORMAT', 'INSERT': 'INSERT',
        'INTERSECT': 'INTERSECT', 'INTERVAL': 'INTERVAL', 'INTO': 'INTO', 'IS': 'IS',
        'ITEMS': 'ITEMS', 'JOIN': 'JOIN', 'KEYS': 'KEYS', 'LAST': 'LAST', 'LATERAL': 'LATERAL',
        'LAZY': 'LAZY', 'LEADING': 'LEADING', 'LEFT': 'LEFT', 'LIKE': 'LIKE', 'ILIKE': 'ILIKE',
        'LIMIT': 'LIMIT', 'LINES': 'LINES', 'LIST': 'LIST', 'LOAD': 'LOAD', 'LOCAL': 'LOCAL',
        'LOCATION': 'LOCATION', 'LOCK': 'LOCK', 'LOCKS': 'LOCKS', 'LOGICAL': 'LOGICAL',
        'MACRO': 'MACRO', 'MAP': 'MAP', 'MATCHED': 'MATCHED', 'MERGE': 'MERGE',
        'MICROSECOND': 'MICROSECOND', 'MICROSECONDS': 'MICROSECONDS', 'MILLISECOND': 'MILLISECOND',
        'MILLISECONDS': 'MILLISECONDS', 'MINUTE': 'MINUTE', 'MINUTES': 'MINUTES', 'MONTH': 'MONTH',
        'MONTHS': 'MONTHS', 'MSCK': 'MSCK', 'NAMESPACE': 'NAMESPACE', 'NAMESPACES': 'NAMESPACES',
        'NANOSECOND': 'NANOSECOND', 'NANOSECONDS': 'NANOSECONDS', 'NATURAL': 'NATURAL', 'NO': 'NO',
        'NOT': 'NOT', 'NULL': 'NULL', 'NULLS': 'NULLS', 'OF': 'OF', 'OFFSET': 'OFFSET', 'ON': 'ON',
        'ONLY': 'ONLY', 'OPTION': 'OPTION', 'OPTIONS': 'OPTIONS', 'OR': 'OR', 'ORDER': 'ORDER',
        'OUT': 'OUT', 'OUTER': 'OUTER', 'OUTPUTFORMAT': 'OUTPUTFORMAT', 'OVER': 'OVER',
        'OVERLAPS': 'OVERLAPS', 'OVERLAY': 'OVERLAY', 'OVERWRITE': 'OVERWRITE',
        'PARTITION': 'PARTITION', 'PARTITIONED': 'PARTITIONED', 'PARTITIONS': 'PARTITIONS',
        'PERCENTILE_CONT': 'PERCENTILE_CONT', 'PERCENTILE_DISC': 'PERCENTILE_DISC',
        'PERCENT': 'PERCENTLIT', 'PIVOT': 'PIVOT', 'PLACING': 'PLACING', 'POSITION': 'POSITION',
        'PRECEDING': 'PRECEDING', 'PRIMARY': 'PRIMARY', 'PRINCIPALS': 'PRINCIPALS',
        'PROPERTIES': 'PROPERTIES', 'PURGE': 'PURGE', 'QUARTER': 'QUARTER', 'QUERY': 'QUERY',
        'RANGE': 'RANGE', 'RECORDREADER': 'RECORDREADER', 'RECORDWRITER': 'RECORDWRITER',
        'RECOVER': 'RECOVER', 'REDUCE': 'REDUCE', 'REFERENCES': 'REFERENCES', 'REFRESH': 'REFRESH',
        'RENAME': 'RENAME', 'REPAIR': 'REPAIR', 'REPEATABLE': 'REPEATABLE', 'REPLACE': 'REPLACE',
        'RESET': 'RESET', 'RESPECT': 'RESPECT', 'RESTRICT': 'RESTRICT', 'REVOKE': 'REVOKE',
        'RIGHT': 'RIGHT', 'RLIKE': 'RLIKE', 'ROLE': 'ROLE', 'ROLES': 'ROLES', 'ROLLBACK': 'ROLLBACK',
        'ROLLUP': 'ROLLUP', 'ROW': 'ROW', 'ROWS': 'ROWS', 'SECOND': 'SECOND', 'SECONDS': 'SECONDS',
        'SCHEMA': 'SCHEMA', 'SCHEMAS': 'SCHEMAS', 'SELECT': 'SELECT', 'SEMI': 'SEMI',
        'SEPARATED': 'SEPARATED', 'SERDE': 'SERDE', 'SERDEPROPERTIES': 'SERDEPROPERTIES',
        'SESSION_USER': 'SESSION_USER', 'SET': 'SET', 'MINUS': 'SETMINUS', 'SETS': 'SETS',
        'SHOW': 'SHOW', 'SKEWED': 'SKEWED', 'SOME': 'SOME', 'SORT': 'SORT', 'SORTED': 'SORTED',
        'SOURCE': 'SOURCE', 'START': 'START', 'STATISTICS': 'STATISTICS', 'STORED': 'STORED',
        'STRATIFY': 'STRATIFY', 'STRUCT': 'STRUCT', 'SUBSTR': 'SUBSTR', 'SUBSTRING': 'SUBSTRING',
        'SYNC': 'SYNC', 'SYSTEM_TIME': 'SYSTEM_TIME', 'SYSTEM_VERSION': 'SYSTEM_VERSION',
        'TABLE': 'TABLE', 'TABLES': 'TABLES', 'TABLESAMPLE': 'TABLESAMPLE', 'TARGET': 'TARGET',
        'TBLPROPERTIES': 'TBLPROPERTIES', 'TEMPORARY': 'TEMPORARY', 'TEMP': 'TEMPORARY',
        'TERMINATED': 'TERMINATED', 'THEN': 'THEN', 'TIME': 'TIME', 'TIMESTAMP': 'TIMESTAMP',
        'TIMESTAMPADD': 'TIMESTAMPADD', 'TIMESTAMPDIFF': 'TIMESTAMPDIFF', 'TO': 'TO',
        'TOUCH': 'TOUCH', 'TRAILING': 'TRAILING', 'TRANSACTION': 'TRANSACTION',
        'TRANSACTIONS': 'TRANSACTIONS', 'TRANSFORM': 'TRANSFORM', 'TRIM': 'TRIM', 'TRUE': 'TRUE',
        'TRUNCATE': 'TRUNCATE', 'TRY_CAST': 'TRY_CAST', 'TYPE': 'TYPE', 'UNARCHIVE': 'UNARCHIVE',
        'UNBOUNDED': 'UNBOUNDED', 'UNCACHE': 'UNCACHE', 'UNION': 'UNION', 'UNIQUE': 'UNIQUE',
        'UNKNOWN': 'UNKNOWN', 'UNLOCK': 'UNLOCK', 'UNPIVOT': 'UNPIVOT', 'UNSET': 'UNSET',
        'UPDATE': 'UPDATE', 'USE': 'USE', 'USER': 'USER', 'USING': 'USING', 'VALUES': 'VALUES',
        'VERSION': 'VERSION', 'VIEW': 'VIEW', 'VIEWS': 'VIEWS', 'WEEK': 'WEEK', 'WEEKS': 'WEEKS',
        'WHEN': 'WHEN', 'WHERE': 'WHERE', 'WINDOW': 'WINDOW', 'WITH': 'WITH', 'WITHIN': 'WITHIN',
        'YEAR': 'YEAR', 'YEARS': 'YEARS', 'ZONE': 'ZONE'
    }

    def __init__(self, input_str: str):
        self.input = input_str
        self.pos = 0
        self.length = len(input_str)
        self.has_unclosed_bracketed_comment = False

    def isValidDecimal(self, token: str, next_pos: int) -> bool:
        """Check if a decimal token is valid (not followed by digit, letter, or underscore)."""
        if next_pos >= self.length:
            return True
        next_char = self.input[next_pos]
        return not (next_char.isalnum() or next_char == '_')

    def isHint(self, pos: int) -> bool:
        """Check if the next character after '/*' is '+' (indicating a hint)."""
        if pos + 1 < self.length:
            return self.input[pos + 1] == '+'
        return False

    def markUnclosedComment(self):
        """Mark that an unclosed bracketed comment was encountered."""
        self.has_unclosed_bracketed_comment = True

    def tokenize(self) -> List[Tuple[int, str]]:
        tokens = []
        while self.pos < self.length:
            char = self.input[self.pos]

            # Whitespace
            if char.isspace():
                start = self.pos
                while self.pos < self.length and self.input[self.pos].isspace():
                    self.pos += 1
                tokens.append((self.WS, self.input[start:self.pos]))
                continue

            # Single-character tokens
            if char == ';':
                tokens.append((self.SEMICOLON, char))
                self.pos += 1
            elif char == '(':
                tokens.append((self.LEFT_PAREN, char))
                self.pos += 1
            elif char == ')':
                tokens.append((self.RIGHT_PAREN, char))
                self.pos += 1
            elif char == ',':
                tokens.append((self.COMMA, char))
                self.pos += 1
            elif char == '.':
                tokens.append((self.DOT, char))
                self.pos += 1
            elif char == '[':
                tokens.append((self.LEFT_BRACKET, char))
                self.pos += 1
            elif char == ']':
                tokens.append((self.RIGHT_BRACKET, char))
                self.pos += 1
            elif char == '=':
                if self.pos + 1 < self.length and self.input[self.pos + 1] == '=':
                    tokens.append((self.EQ, '=='))
                    self.pos += 2
                elif self.pos + 1 < self.length and self.input[self.pos + 1] == '>':
                    tokens.append((self.NSEQ, '<=>'))
                    self.pos += 3
                else:
                    tokens.append((self.EQ, '='))
                    self.pos += 1
            elif char == '<':
                if self.pos + 1 < self.length and self.input[self.pos + 1] == '=':
                    tokens.append((self.LTE, '<='))
                    self.pos += 2
                elif self.pos + 1 < self.length and self.input[self.pos + 1] == '>':
                    tokens.append((self.NEQ, '<>'))
                    self.pos += 2
                else:
                    tokens.append((self.LT, '<'))
                    self.pos += 1
            elif char == '>':
                if self.pos + 1 < self.length and self.input[self.pos + 1] == '=':
                    tokens.append((self.GTE, '>='))
                    self.pos += 2
                else:
                    tokens.append((self.GT, '>'))
                    self.pos += 1
            elif char == '!':
                if self.pos + 1 < self.length and self.input[self.pos + 1] == '=':
                    tokens.append((self.NEQJ, '!='))
                    self.pos += 2
                elif self.pos + 1 < self.length and self.input[self.pos + 1] == '>':
                    tokens.append((self.LTE, '!>'))
                    self.pos += 2
                elif self.pos + 1 < self.length and self.input[self.pos + 1] == '<':
                    tokens.append((self.GTE, '!<'))
                    self.pos += 2
                else:
                    tokens.append((self.NOT, '!'))
                    self.pos += 1
            elif char == '+':
                tokens.append((self.PLUS, '+'))
                self.pos += 1
            elif char == '-':
                if self.pos + 1 < self.length and self.input[self.pos + 1] == '-':
                    # Simple comment
                    start = self.pos
                    self.pos += 2
                    while self.pos < self.length and self.input[self.pos] != '\n':
                        self.pos += 1
                    if self.pos < self.length:
                        self.pos += 1  # Skip newline
                    tokens.append((self.SIMPLE_COMMENT, self.input[start:self.pos]))
                elif self.pos + 1 < self.length and self.input[self.pos + 1] == '>':
                    tokens.append((self.ARROW, '->'))
                    self.pos += 2
                else:
                    tokens.append((self.MINUS, '-'))
                    self.pos += 1
            elif char == '*':
                tokens.append((self.ASTERISK, '*'))
                self.pos += 1
            elif char == '/':
                if self.pos + 1 < self.length and self.input[self.pos + 1] == '*':
                    # Bracketed comment or hint
                    start = self.pos
                    self.pos += 2
                    if self.isHint(start + 2):
                        tokens.append((self.HENT_START, '/*+'))
                        self.pos += 1
                        while self.pos < self.length and self.input[self.pos:self.pos + 2] != '*/':
                            self.pos += 1
                        if self.pos + 1 < self.length:
                            tokens.append((self.HENT_END, '*/'))
                            self.pos += 2
                    else:
                        while self.pos < self.length and self.input[self.pos:self.pos + 2] != '*/':
                            self.pos += 1
                        if self.pos + 1 < self.length:
                            tokens.append((self.BRACKETED_COMMENT, self.input[start:self.pos + 2]))
                            self.pos += 2
                        else:
                            self.markUnclosedComment()
                            tokens.append((self.BRACKETED_COMMENT, self.input[start:]))
                            self.pos = self.length
                else:
                    tokens.append((self.SLASH, '/'))
                    self.pos += 1
            elif char == '%':
                tokens.append((self.PERCENT, '%'))
                self.pos += 1
            elif char == '~':
                tokens.append((self.TILDE, '~'))
                self.pos += 1
            elif char == '&':
                tokens.append((self.AMPERSAND, '&'))
                self.pos += 1
            elif char == '|':
                if self.pos + 1 < self.length and self.input[self.pos + 1] == '|':
                    tokens.append((self.CONCAT_PIPE, '||'))
                    self.pos += 2
                else:
                    tokens.append((self.PIPE, '|'))
                    self.pos += 1
            elif char == '^':
                tokens.append((self.HAT, '^'))
                self.pos += 1
            elif char == ':':
                tokens.append((self.COLON, ':'))
                self.pos += 1

            # String literals
            elif char == '\'':
                start = self.pos
                self.pos += 1
                while self.pos < self.length and self.input[self.pos] != '\'':
                    if self.input[self.pos] == '\\':
                        self.pos += 2  # Skip escaped character
                    else:
                        self.pos += 1
                if self.pos < self.length:
                    self.pos += 1  # Skip closing quote
                    tokens.append((self.STRING, self.input[start:self.pos]))
                else:
                    tokens.append((self.UNRECOGNIZED, self.input[start:]))
                    self.pos = self.length
            elif char == '"':
                start = self.pos
                self.pos += 1
                while self.pos < self.length and self.input[self.pos] != '"':
                    if self.input[self.pos] == '\\':
                        self.pos += 2  # Skip escaped character
                    else:
                        self.pos += 1
                if self.pos < self.length:
                    self.pos += 1  # Skip closing quote
                    tokens.append((self.DOUBLEQUOTED_STRING, self.input[start:self.pos]))
                else:
                    tokens.append((self.UNRECOGNIZED, self.input[start:]))
                    self.pos = self.length

            # Backquoted identifier
            elif char == '`':
                start = self.pos
                self.pos += 1
                while self.pos < self.length and self.input[self.pos] != '`':
                    if self.pos + 1 < self.length and self.input[self.pos:self.pos + 2] == '``':
                        self.pos += 2  # Skip escaped backquote
                    else:
                        self.pos += 1
                if self.pos < self.length:
                    self.pos += 1  # Skip closing backquote
                    tokens.append((self.BACKQUOTED_IDENTIFIER, self.input[start:self.pos]))
                else:
                    tokens.append((self.UNRECOGNIZED, self.input[start:]))
                    self.pos = self.length

            # Numeric literals and identifiers
            elif char.isalpha() or char == '_':
                start = self.pos
                while self.pos < self.length and (self.input[self.pos].isalnum() or self.input[self.pos] == '_'):
                    self.pos += 1
                token = self.input[start:self.pos]
                if token in self.KEYWORDS:
                    tokens.append((getattr(self, token, self.IDENTIFIER), token))
                else:
                    tokens.append((self.IDENTIFIER, token))
            elif char.isdigit():
                start = self.pos
                while self.pos < self.length and self.input[self.pos].isdigit():
                    self.pos += 1
                token = self.input[start:self.pos]
                if self.pos < self.length:
                    next_char = self.input[self.pos]
                    if next_char == '.':
                        self.pos += 1
                        while self.pos < self.length and self.input[self.pos].isdigit():
                            self.pos += 1
                        token = self.input[start:self.pos]
                        if self.isValidDecimal(token, self.pos):
                            tokens.append((self.DECIMAL_VALUE, token))
                        else:
                            tokens.append((self.UNRECOGNIZED, token))
                    elif next_char == 'E' or next_char == 'e':
                        self.pos += 1
                        if self.pos < self.length and self.input[self.pos] in ['+', '-']:
                            self.pos += 1
                        while self.pos < self.length and self.input[self.pos].isdigit():
                            self.pos += 1
                        token = self.input[start:self.pos]
                        tokens.append((self.EXPONENT_VALUE, token))
                    elif next_char == 'L':
                        tokens.append((self.BIGINT_LITERAL, token + 'L'))
                        self.pos += 1
                    elif next_char == 'S':
                        tokens.append((self.SMALLINT_LITERAL, token + 'S'))
                        self.pos += 1
                    elif next_char == 'Y':
                        tokens.append((self.TINYINT_LITERAL, token + 'Y'))
                        self.pos += 1
                    elif next_char == 'F':
                        tokens.append((self.FLOAT_LITERAL, token + 'F'))
                        self.pos += 1
                    elif next_char == 'D':
                        tokens.append((self.DOUBLE_LITERAL, token + 'D'))
                        self.pos += 1
                    elif next_char == 'B' and self.pos + 1 < self.length and self.input[self.pos + 1] == 'D':
                        tokens.append((self.BIGDECIMAL_LITERAL, token + 'BD'))
                        self.pos += 2
                    else:
                        tokens.append((self.INTEGER_VALUE, token))
                else:
                    tokens.append((self.INTEGER_VALUE, token))

            else:
                tokens.append((self.UNRECOGNIZED, char))
                self.pos += 1

        return tokens

# Example usage
if __name__ == "__main__":
    sql = "SELECT id, name FROM users WHERE age > 18 ORDER BY name"
    lexer = SqlBaseLexer(sql)
    tokens = lexer.tokenize()
    for token_type, value in tokens:
        print(f"Type: {token_type}, Value: {value}")