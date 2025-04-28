import re
from typing import List, Tuple, Dict, Any, Optional, Union

class SqlBaseParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = []
        self.current_token_index = 0
        
        # Configuration options from the grammar
        self.legacy_setops_precedence_enabled = False
        self.legacy_exponent_literal_as_decimal_enabled = False
        self.SQL_standard_keyword_behavior = False
        self.double_quoted_identifiers = False
    
    def parse(self):
        """Parse the input SQL statement."""
        self.tokens = self.lexer.tokenize()
        self.current_token_index = 0
        
        # Start with the top-level rule
        return self.singleStatement()
    
    # Token handling methods
    def current_token(self) -> Optional[Tuple[int, str]]:
        """Get the current token."""
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None
    
    def next_token(self) -> Optional[Tuple[int, str]]:
        """Move to the next token and return it."""
        self.current_token_index += 1
        return self.current_token()
    
    def peek_token(self, lookahead=1) -> Optional[Tuple[int, str]]:
        """Look ahead at a future token without consuming it."""
        peek_index = self.current_token_index + lookahead
        if peek_index < len(self.tokens):
            return self.tokens[peek_index]
        return None
    
    def match(self, token_type: int) -> bool:
        """Check if the current token matches the expected type, consume it if it does."""
        token = self.current_token()
        if token and token[0] == token_type:
            self.next_token()
            return True
        return False
    
    def expect(self, token_type: int) -> str:
        """Expect a token of a specific type, consume it, and return its value."""
        token = self.current_token()
        if token and token[0] == token_type:
            result = token[1]
            self.next_token()
            return result
        raise SyntaxError(f"Expected token type {token_type}, got {token[0] if token else 'None'} at position {self.current_token_index}")
    
    def check_keyword(self, keyword: str) -> bool:
        """Check if the current token is a specific keyword."""
        token = self.current_token()
        if token and token[1].upper() == keyword:
            return True
        return False
    
    def match_keyword(self, keyword: str) -> bool:
        """Check if the current token is a specific keyword, consume it if it is."""
        if self.check_keyword(keyword):
            self.next_token()
            return True
        return False
    
    def is_at_end(self) -> bool:
        """Check if we've reached the end of the tokens."""
        return self.current_token_index >= len(self.tokens)
    
    # Grammar rule methods
    def singleStatement(self):
        """
        singleStatement
            : statement SEMICOLON* EOF
        """
        stmt = self.statement()
        
        # Skip any semicolons
        while self.current_token() and self.current_token()[0] == self.lexer.SEMICOLON:
            self.next_token()
        
        # Ensure we've consumed all tokens
        if not self.is_at_end():
            raise SyntaxError(f"Expected end of input, got {self.current_token()[1]} at position {self.current_token_index}")
        
        return stmt
    
    def singleExpression(self):
        """
        singleExpression
            : namedExpression EOF
        """
        expr = self.namedExpression()
        
        if not self.is_at_end():
            raise SyntaxError(f"Expected end of input, got {self.current_token()[1]} at position {self.current_token_index}")
        
        return expr
    
    def singleTableIdentifier(self):
        """
        singleTableIdentifier
            : tableIdentifier EOF
        """
        table_id = self.tableIdentifier()
        
        if not self.is_at_end():
            raise SyntaxError(f"Expected end of input, got {self.current_token()[1]} at position {self.current_token_index}")
        
        return table_id
    
    def singleMultipartIdentifier(self):
        """
        singleMultipartIdentifier
            : multipartIdentifier EOF
        """
        multipart_id = self.multipartIdentifier()
        
        if not self.is_at_end():
            raise SyntaxError(f"Expected end of input, got {self.current_token()[1]} at position {self.current_token_index}")
        
        return multipart_id
    
    def singleFunctionIdentifier(self):
        """
        singleFunctionIdentifier
            : functionIdentifier EOF
        """
        function_id = self.functionIdentifier()
        
        if not self.is_at_end():
            raise SyntaxError(f"Expected end of input, got {self.current_token()[1]} at position {self.current_token_index}")
        
        return function_id
    
    def singleDataType(self):
        """
        singleDataType
            : dataType EOF
        """
        data_type = self.dataType()
        
        if not self.is_at_end():
            raise SyntaxError(f"Expected end of input, got {self.current_token()[1]} at position {self.current_token_index}")
        
        return data_type
    
    def singleTableSchema(self):
        """
        singleTableSchema
            : colTypeList EOF
        """
        col_type_list = self.colTypeList()
        
        if not self.is_at_end():
            raise SyntaxError(f"Expected end of input, got {self.current_token()[1]} at position {self.current_token_index}")
        
        return col_type_list
    
    def statement(self):
        """Implementation of the statement rule from the grammar."""
        # Check for query (statementDefault)
        if self.check_keyword("SELECT") or self.check_keyword("FROM") or self.check_keyword("VALUES") or (self.check_keyword("WITH") and not self.dmlStatementCheck()):
            return {"type": "statementDefault", "query": self.query()}
        
        # Check for DML statements
        if self.dmlStatementCheck():
            ctes = None
            if self.check_keyword("WITH"):
                ctes = self.ctes()
            
            dml = self.dmlStatementNoWith()
            return {"type": "dmlStatement", "ctes": ctes, "statement": dml}
        
        # Check for USE
        if self.check_keyword("USE"):
            self.next_token()
            
            # Check for namespace
            if self.check_keyword("NAMESPACE"):
                self.next_token()
                return {"type": "useNamespace", "namespace": self.multipartIdentifier()}
            
            return {"type": "use", "database": self.multipartIdentifier()}
        
        # Check for SET CATALOG
        if self.check_keyword("SET") and self.peek_token() and self.check_keyword("CATALOG", self.peek_token()[1]):
            self.next_token()  # Consume SET
            self.next_token()  # Consume CATALOG
            
            if self.current_token()[0] == self.lexer.IDENTIFIER:
                return {"type": "setCatalog", "catalog": self.identifier()}
            else:
                return {"type": "setCatalog", "catalog": self.stringLit()}
        
        # Implement other statement types as needed
        raise NotImplementedError(f"Statement type not implemented: {self.current_token()[1] if self.current_token() else 'EOF'}")
    
    def dmlStatementCheck(self):
        """Helper method to check if the current tokens indicate a DML statement."""
        if self.check_keyword("INSERT") or self.check_keyword("UPDATE") or self.check_keyword("DELETE") or self.check_keyword("MERGE"):
            return True
        
        if self.check_keyword("WITH"):
            # Look ahead to see if this is a WITH followed by a DML statement
            saved_index = self.current_token_index
            try:
                self.next_token()  # Skip WITH
                
                # Skip named query definitions
                while not self.is_at_end():
                    self.errorCapturingIdentifier()  # name
                    
                    # Optional column aliases
                    if self.current_token() and self.current_token()[0] == self.lexer.LEFT_PAREN:
                        self.identifierList()
                    
                    # Optional AS
                    if self.check_keyword("AS"):
                        self.next_token()
                    
                    # Skip the subquery
                    if self.current_token() and self.current_token()[0] == self.lexer.LEFT_PAREN:
                        self.next_token()
                        nesting = 1
                        while nesting > 0 and not self.is_at_end():
                            if self.current_token()[0] == self.lexer.LEFT_PAREN:
                                nesting += 1
                            elif self.current_token()[0] == self.lexer.RIGHT_PAREN:
                                nesting -= 1
                            self.next_token()
                    
                    # If we've reached a DML keyword, this is a DML statement
                    if self.check_keyword("INSERT") or self.check_keyword("UPDATE") or self.check_keyword("DELETE") or self.check_keyword("MERGE"):
                        return True
                    
                    # If there's no comma, we've reached the end of the WITH clause
                    if not self.current_token() or self.current_token()[0] != self.lexer.COMMA:
                        break
                    
                    self.next_token()  # Skip comma
            finally:
                # Restore the token index
                self.current_token_index = saved_index
        
        return False
    
    def query(self):
        """
        query
            : ctes? queryTerm queryOrganization
        """
        ctes = None
        if self.check_keyword("WITH"):
            ctes = self.ctes()
        
        query_term = self.queryTerm()
        query_org = self.queryOrganization()
        
        return {"type": "query", "ctes": ctes, "queryTerm": query_term, "queryOrganization": query_org}
    
    def ctes(self):
        """
        ctes
            : WITH namedQuery (COMMA namedQuery)*
        """
        self.match_keyword("WITH")
        named_queries = [self.namedQuery()]
        
        while self.current_token() and self.current_token()[0] == self.lexer.COMMA:
            self.next_token()
            named_queries.append(self.namedQuery())
        
        return {"type": "ctes", "namedQueries": named_queries}
    
    def namedQuery(self):
        """
        namedQuery
            : name=errorCapturingIdentifier (columnAliases=identifierList)? AS? LEFT_PAREN query RIGHT_PAREN
        """
        name = self.errorCapturingIdentifier()
        
        column_aliases = None
        if self.current_token() and self.current_token()[0] == self.lexer.LEFT_PAREN:
            column_aliases = self.identifierList()
        
        if self.check_keyword("AS"):
            self.next_token()
        
        self.expect(self.lexer.LEFT_PAREN)
        query = self.query()
        self.expect(self.lexer.RIGHT_PAREN)
        
        return {"type": "namedQuery", "name": name, "columnAliases": column_aliases, "query": query}
    
    def queryTerm(self):
        """
        queryTerm
            : queryPrimary                                                                       #queryTermDefault
            | left=queryTerm {legacy_setops_precedence_enabled}?
                operator=(INTERSECT | UNION | EXCEPT | SETMINUS) setQuantifier? right=queryTerm  #setOperation
            | left=queryTerm {!legacy_setops_precedence_enabled}?
                operator=INTERSECT setQuantifier? right=queryTerm                                #setOperation
            | left=queryTerm {!legacy_setops_precedence_enabled}?
                operator=(UNION | EXCEPT | SETMINUS) setQuantifier? right=queryTerm              #setOperation
        """
        left = self.queryPrimary()
        
        while True:
            if not self.current_token():
                break
                
            if self.check_keyword("INTERSECT"):
                operator = "INTERSECT"
                self.next_token()
                set_quantifier = self.setQuantifier() if self.check_keyword("ALL") or self.check_keyword("DISTINCT") else None
                
                right = self.queryPrimary() if self.legacy_setops_precedence_enabled else self.queryTerm()
                left = {"type": "setOperation", "left": left, "operator": operator, "setQuantifier": set_quantifier, "right": right}
                
            elif self.check_keyword("UNION") or self.check_keyword("EXCEPT") or self.check_keyword("MINUS"):
                operator = self.current_token()[1]
                self.next_token()
                
                set_quantifier = self.setQuantifier() if self.check_keyword("ALL") or self.check_keyword("DISTINCT") else None
                
                right = self.queryPrimary()
                if not self.legacy_setops_precedence_enabled and operator != "INTERSECT":
                    right = self.queryTerm()
                    
                left = {"type": "setOperation", "left": left, "operator": operator, "setQuantifier": set_quantifier, "right": right}
            else:
                break
                
        return left
    
    def queryPrimary(self):
        """
        queryPrimary
            : querySpecification                                                    #queryPrimaryDefault
            | fromStatement                                                         #fromStmt
            | TABLE multipartIdentifier                                             #table
            | inlineTable                                                           #inlineTableDefault1
            | LEFT_PAREN query RIGHT_PAREN                                          #subquery
        """
        if self.check_keyword("SELECT"):
            return {"type": "queryPrimaryDefault", "querySpecification": self.querySpecification()}
        elif self.check_keyword("FROM"):
            return {"type": "fromStmt", "fromStatement": self.fromStatement()}
        elif self.check_keyword("TABLE"):
            self.next_token()
            return {"type": "table", "multipartIdentifier": self.multipartIdentifier()}
        elif self.check_keyword("VALUES"):
            return {"type": "inlineTableDefault1", "inlineTable": self.inlineTable()}
        elif self.current_token() and self.current_token()[0] == self.lexer.LEFT_PAREN:
            self.next_token()
            query = self.query()
            self.expect(self.lexer.RIGHT_PAREN)
            return {"type": "subquery", "query": query}
        else:
            raise SyntaxError(f"Expected query primary, got {self.current_token()[1] if self.current_token() else 'EOF'}")
    
    def selectClause(self):
        """
        selectClause
            : SELECT (hints+=hint)* setQuantifier? namedExpressionSeq
        """
        self.match_keyword("SELECT")
        
        hints = []
        while self.current_token() and self.current_token()[0] == self.lexer.HENT_START:
            hints.append(self.hint())
        
        set_quantifier = None
        if self.check_keyword("ALL") or self.check_keyword("DISTINCT"):
            set_quantifier = self.setQuantifier()
        
        named_expressions = self.namedExpressionSeq()
        
        return {"type": "selectClause", "hints": hints, "setQuantifier": set_quantifier, "namedExpressions": named_expressions}
    
    def setQuantifier(self):
        """
        setQuantifier
            : DISTINCT
            | ALL
        """
        if self.check_keyword("DISTINCT"):
            self.next_token()
            return "DISTINCT"
        elif self.check_keyword("ALL"):
            self.next_token()
            return "ALL"
        return None
    
    def fromClause(self):
        """
        fromClause
            : FROM relation (COMMA relation)* lateralView* pivotClause? unpivotClause?
        """
        self.match_keyword("FROM")
        
        relations = [self.relation()]
        
        while self.current_token() and self.current_token()[0] == self.lexer.COMMA:
            self.next_token()
            relations.append(self.relation())
        
        lateral_views = []
        while self.check_keyword("LATERAL") and self.peek_token() and self.check_keyword("VIEW", self.peek_token()[1]):
            lateral_views.append(self.lateralView())
        
        pivot_clause = None
        if self.check_keyword("PIVOT"):
            pivot_clause = self.pivotClause()
        
        unpivot_clause = None
        if self.check_keyword("UNPIVOT"):
            unpivot_clause = self.unpivotClause()
        
        return {
            "type": "fromClause",
            "relations": relations,
            "lateralViews": lateral_views,
            "pivotClause": pivot_clause,
            "unpivotClause": unpivot_clause
        }
    
    def relation(self):
        """
        relation
            : LATERAL? relationPrimary relationExtension*
        """
        is_lateral = False
        if self.check_keyword("LATERAL"):
            is_lateral = True
            self.next_token()
        
        relation_primary = self.relationPrimary()
        
        extensions = []
        while (self.current_token() and 
               (self.check_keyword("JOIN") or 
                self.check_keyword("CROSS") or 
                self.check_keyword("INNER") or 
                self.check_keyword("LEFT") or 
                self.check_keyword("RIGHT") or 
                self.check_keyword("FULL") or 
                self.check_keyword("NATURAL") or
                self.check_keyword("PIVOT") or
                self.check_keyword("UNPIVOT"))):
            if self.check_keyword("PIVOT"):
                extensions.append(self.pivotClause())
            elif self.check_keyword("UNPIVOT"):
                extensions.append(self.unpivotClause())
            else:
                extensions.append(self.joinRelation())
        
        return {"type": "relation", "isLateral": is_lateral, "relationPrimary": relation_primary, "extensions": extensions}
    
    def relationPrimary(self):
        """
        relationPrimary
            : multipartIdentifier temporalClause?
              sample? tableAlias                                    #tableName
            | LEFT_PAREN query RIGHT_PAREN sample? tableAlias       #aliasedQuery
            | LEFT_PAREN relation RIGHT_PAREN sample? tableAlias    #aliasedRelation
            | inlineTable                                           #inlineTableDefault2
            | functionTable                                         #tableValuedFunction
        """
        if self.check_keyword("VALUES"):
            return {"type": "inlineTableDefault2", "inlineTable": self.inlineTable()}
        elif (self.current_token() and 
              self.current_token()[0] == self.lexer.IDENTIFIER and 
              self.peek_token() and 
              self.peek_token()[0] == self.lexer.LEFT_PAREN):
            return {"type": "tableValuedFunction", "functionTable": self.functionTable()}
        elif self.current_token() and self.current_token()[0] == self.lexer.LEFT_PAREN:
            self.next_token()
            
            # Determine if this is a query or a relation
            saved_index = self.current_token_index
            is_relation = False
            
            try:
                if (self.check_keyword("SELECT") or 
                    self.check_keyword("FROM") or 
                    self.check_keyword("VALUES") or 
                    self.check_keyword("TABLE") or
                    (self.current_token() and self.current_token()[0] == self.lexer.LEFT_PAREN)):
                    is_relation = False
                else:
                    is_relation = True
            finally:
                self.current_token_index = saved_index
            
            if is_relation:
                relation = self.relation()
                self.expect(self.lexer.RIGHT_PAREN)
                
                sample = None
                if self.check_keyword("TABLESAMPLE"):
                    sample = self.sample()
                
                table_alias = self.tableAlias()
                
                return {"type": "aliasedRelation", "relation": relation, "sample": sample, "tableAlias": table_alias}
            else:
                query = self.query()
                self.expect(self.lexer.RIGHT_PAREN)
                
                sample = None
                if self.check_keyword("TABLESAMPLE"):
                    sample = self.sample()
                
                table_alias = self.tableAlias()
                
                return {"type": "aliasedQuery", "query": query, "sample": sample, "tableAlias": table_alias}
        else:
            multipart_id = self.multipartIdentifier()
            
            temporal_clause = None
            if self.check_keyword("FOR") or (self.check_keyword("SYSTEM_VERSION") or self.check_keyword("VERSION") or self.check_keyword("SYSTEM_TIME") or self.check_keyword("TIMESTAMP")):
                temporal_clause = self.temporalClause()
            
            sample = None
            if self.check_keyword("TABLESAMPLE"):
                sample = self.sample()
            
            table_alias = self.tableAlias()
            
            return {"type": "tableName", "multipartIdentifier": multipart_id, "temporalClause": temporal_clause, "sample": sample, "tableAlias": table_alias}
    
    def tableAlias(self):
        """
        tableAlias
            : (AS? strictIdentifier identifierList?)?
        """
        if not self.current_token() or (not self.check_keyword("AS") and self.current_token()[0] != self.lexer.IDENTIFIER):
            return None
        
        as_keyword = False
        if self.check_keyword("AS"):
            as_keyword = True
            self.next_token()
        
        identifier = self.strictIdentifier()
        
        columns = None
        if self.current_token() and self.current_token()[0] == self.lexer.LEFT_PAREN:
            columns = self.identifierList()
        
        return {"type": "tableAlias", "as": as_keyword, "identifier": identifier, "columns": columns}
    
    def joinRelation(self):
        """
        joinRelation
            : (joinType) JOIN LATERAL? right=relationPrimary joinCriteria?
            | NATURAL joinType JOIN LATERAL? right=relationPrimary
        """
        is_natural = False
        if self.check_keyword("NATURAL"):
            is_natural = True
            self.next_token()
        
        join_type = self.joinType()
        
        self.match_keyword("JOIN")
        
        is_lateral = False
        if self.check_keyword("LATERAL"):
            is_lateral = True
            self.next_token()
        
        right = self.relationPrimary()
        
        criteria = None
        if not is_natural and (self.check_keyword("ON") or self.check_keyword("USING")):
            criteria = self.joinCriteria()
        
        return {
            "type": "joinRelation",
            "isNatural": is_natural,
            "joinType": join_type,
            "isLateral": is_lateral,
            "right": right,
            "criteria": criteria
        }
    
    def joinType(self):
        """
        joinType
            : INNER?
            | CROSS
            | LEFT OUTER?
            | LEFT? SEMI
            | RIGHT OUTER?
            | FULL OUTER?
            | LEFT? ANTI
        """
        if self.check_keyword("INNER"):
            self.next_token()
            return "INNER"
        elif self.check_keyword("CROSS"):
            self.next_token()
            return "CROSS"
        elif self.check_keyword("LEFT"):
            self.next_token()
            if self.check_keyword("OUTER"):
                self.next_token()
                return "LEFT OUTER"
            elif self.check_keyword("SEMI"):
                self.next_token()
                return "LEFT SEMI"
            elif self.check_keyword("ANTI"):
                self.next_token()
                return "LEFT ANTI"
            return "LEFT"
        elif self.check_keyword("RIGHT"):
            self.next_token()
            if self.check_keyword("OUTER"):
                self.next_token()
                return "RIGHT OUTER"
            return "RIGHT"
        elif self.check_keyword("FULL"):
            self.next_token()
            if self.check_keyword("OUTER"):
                self.next_token()
                return "FULL OUTER"
            return "FULL"
        elif self.check_keyword("SEMI"):
            self.next_token()
            return "SEMI"
        elif self.check_keyword("ANTI"):
            self.next_token()
            return "ANTI"
        return ""  # INNER JOIN with 'INNER' omitted
    
    def joinCriteria(self):
        """
        joinCriteria
            : ON booleanExpression
            | USING identifierList
        """
        if self.check_keyword("ON"):
            self.next_token()
            return {"type": "ON", "expression": self.booleanExpression()}
        elif self.check_keyword("USING"):
            self.next_token()
            return {"type": "USING", "columns": self.identifierList()}
        else:
            raise SyntaxError(f"Expected ON or USING, got {self.current_token()[1] if self.current_token() else 'EOF'}")
    
    def identifierList(self):
        """
        identifierList
            : LEFT_PAREN identifierSeq RIGHT_PAREN
        """
        self.expect(self.lexer.LEFT_PAREN)
        seq = self.identifierSeq()
        self.expect(self.lexer.RIGHT_PAREN)
        return seq
    
    def identifierSeq(self):
        """
        identifierSeq
            : ident+=errorCapturingIdentifier (COMMA ident+=errorCapturingIdentifier)*
        """
        identifiers = [self.errorCapturingIdentifier()]
        
        while self.current_token() and self.current_token()[0] == self.lexer.COMMA:
            self.next_token()
            identifiers.append(self.errorCapturingIdentifier())
        
        return identifiers
    
    def errorCapturingIdentifier(self):
        """
        errorCapturingIdentifier
            : identifier errorCapturingIdentifierExtra
        """
        base_identifier = self.identifier()
        extra = self.errorCapturingIdentifierExtra()
        
        if extra:
            return {"type": "errorCapturingIdentifier", "baseIdentifier": base_identifier, "extraIdentifiers": extra}
        
        return base_identifier
    
    def errorCapturingIdentifierExtra(self):
        """
        errorCapturingIdentifierExtra
            : (MINUS identifier)+    #errorIdent
            |                        #realIdent
        """
        extra_identifiers = []
        
        while self.current_token() and self.current_token()[0] == self.lexer.MINUS:
            self.next_token()
            if self.current_token() and (self.current_token()[0] == self.lexer.IDENTIFIER or self.isKeyword(self.current_token()[1])):
                extra_identifiers.append(self.identifier())
            else:
                break
        
        return extra_identifiers if extra_identifiers else None
    
    def isKeyword(self, token_value):
        """Check if a token value is a keyword."""
        return token_value.upper() in self.lexer.KEYWORDS
    
    def identifier(self):
        """
        identifier
            : strictIdentifier
            | {!SQL_standard_keyword_behavior}? strictNonReserved
        """
        if not self.SQL_standard_keyword_behavior and self.isStrictNonReserved():
            return {"type": "identifier", "value": self.current_token()[1]}
        
        return self.strictIdentifier()
    
    def isStrictNonReserved(self):
        """Check if the current token is a strict non-reserved keyword."""
        if not self.current_token():
            return False
        
        strict_non_reserved = [
            "ANTI", "CROSS", "EXCEPT", "FULL", "INNER", "INTERSECT", 
            "JOIN", "LATERAL", "LEFT", "NATURAL", "ON", "RIGHT", 
            "SEMI", "SETMINUS", "UNION", "USING"
        ]
        
        return self.current_token()[1].upper() in strict_non_reserved
    
    def strictIdentifier(self):
        """
        strictIdentifier
            : IDENTIFIER              #unquotedIdentifier
            | quotedIdentifier        #quotedIdentifierAlternative
            | {SQL_standard_keyword_behavior}? ansiNonReserved #unquotedIdentifier
            | {!SQL_standard_keyword_behavior}? nonReserved    #unquotedIdentifier
        """
        if self.current_token() and self.current_token()[0] == self.lexer.IDENTIFIER:
            identifier = self.current_token()[1]
            self.next_token()
            return {"type": "unquotedIdentifier", "value": identifier}
        elif self.current_token() and (self.current_token()[0] == self.lexer.BACKQUOTED_IDENTIFIER or 
              (self.double_quoted_identifiers and self.current_token()[0] == self.lexer.DOUBLEQUOTED_STRING)):
            return self.quotedIdentifier()
        elif self.SQL_standard_keyword_behavior and self.isAnsiNonReserved():
            identifier = self.current_token()[1]
            self.next_token()
            return {"type": "unquotedIdentifier", "value": identifier}
        elif not self.SQL_standard_keyword_behavior and self.isNonReserved():
            identifier = self.current_token()[1]
            self.next_token()
            return {"type": "unquotedIdentifier", "value": identifier}
        else:
            raise SyntaxError(f"Expected identifier, got {self.current_token()[1] if self.current_token() else 'EOF'}")
    
    def isAnsiNonReserved(self):
        """Check if the current token is an ANSI non-reserved keyword."""
        if not self.current_token():
            return False
        
        # This is the list - the full list is quite long
        ansi_non_reserved = [
            "ADD", "AFTER", "ALTER", "ALWAYS", "ANALYZE", "ANTI", "ANY_VALUE", "ARCHIVE", "ARRAY", 
            "ASC", "AT", "BETWEEN", "BUCKET", "BUCKETS", "BY", "CACHE", "CASCADE", "CATALOG", 
            "CATALOGS", "CHANGE", "CLEAR", "CLUSTER", "CLUSTERED", "CODEGEN", "COLLECTION", 
            "COLUMNS", "COMMENT", "COMMIT", "COMPACT", "COMPACTIONS", "COMPUTE", "CONCATENATE", 
            "COST", "CUBE", "CURRENT", "DATA", "DATABASE", "DATABASES", "DATEADD", "DATEDIFF", 
            "DAY", "DAYS", "DAYOFYEAR", "DBPROPERTIES", "DEFAULT", "DEFINED", "DELETE", "DELIMITED", 
            "DESC", "DESCRIBE", "DFS", "DIRECTORIES", "DIRECTORY", "DISTRIBUTE", "DIV", "DROP", 
            "ESCAPED", "EXCHANGE", "EXCLUDE", "EXISTS", "EXPLAIN", "EXPORT", "EXTENDED", "EXTERNAL", 
            "EXTRACT", "FIELDS", "FILEFORMAT", "FIRST", "FOLLOWING", "FORMAT", "FORMATTED", 
            "FUNCTION", "FUNCTIONS", "GENERATED", "GLOBAL", "GROUPING", "HOUR", "HOURS", "IF", 
            "IGNORE", "IMPORT", "INCLUDE", "INDEX", "INDEXES", "INPATH", "INPUTFORMAT", "INSERT", 
            "INTERVAL", "ITEMS", "KEYS", "LAST", "LAZY", "LIKE", "ILIKE", "LIMIT", "LINES", "LIST", 
            "LOAD", "LOCAL", "LOCATION", "LOCK", "LOCKS", "LOGICAL", "MACRO", "MAP", "MATCHED", 
            "MERGE", "MICROSECOND", "MICROSECONDS", "MILLISECOND", "MILLISECONDS", "MINUTE", 
            "MINUTES", "MONTH", "MONTHS", "MSCK", "NAMESPACE", "NAMESPACES", "NANOSECOND", 
            "NANOSECONDS", "NO", "NULLS", "OF", "OPTION", "OPTIONS", "OUT", "OUTPUTFORMAT", "OVER", 
            "OVERLAY", "OVERWRITE", "PARTITION", "PARTITIONED", "PARTITIONS", "PERCENTLIT", "PIVOT", 
            "PLACING", "POSITION", "PRECEDING", "PRINCIPALS", "PROPERTIES", "PURGE", "QUARTER", 
            "QUERY", "RANGE", "RECORDREADER", "RECORDWRITER", "RECOVER", "REDUCE", "REFRESH", 
            "RENAME", "REPAIR", "REPEATABLE", "REPLACE", "RESET", "RESPECT", "RESTRICT", "REVOKE", 
            "RLIKE", "ROLE", "ROLES", "ROLLBACK", "ROLLUP", "ROW", "ROWS", "SCHEMA", "SCHEMAS", 
            "SECOND", "SECONDS", "SEMI", "SEPARATED", "SERDE", "SERDEPROPERTIES", "SET", "SETMINUS", 
            "SETS", "SHOW", "SKEWED", "SORT", "SORTED", "SOURCE", "START", "STATISTICS", "STORED", 
            "STRATIFY", "STRUCT", "SUBSTR", "SUBSTRING", "SYNC", "SYSTEM_TIME", "SYSTEM_VERSION", 
            "TABLES", "TABLESAMPLE", "TARGET", "TBLPROPERTIES", "TEMPORARY", "TERMINATED", 
            "TIMESTAMP", "TIMESTAMPADD", "TIMESTAMPDIFF", "TOUCH", "TRANSACTION", "TRANSACTIONS", 
            "TRANSFORM", "TRIM", "TRUE", "TRUNCATE", "TRY_CAST", "TYPE", "UNARCHIVE", "UNBOUNDED", 
            "UNCACHE", "UNLOCK", "UNPIVOT", "UNSET", "UPDATE", "USE", "VALUES", "VERSION", "VIEW", 
            "VIEWS", "WEEK", "WEEKS", "WINDOW", "YEAR", "YEARS", "ZONE"
        ]
        
        return self.current_token()[1].upper() in ansi_non_reserved
    
    def isNonReserved(self):
        """Check if the current token is a non-reserved keyword."""
        if not self.current_token():
            return False
        
        # This is the list - the full list is quite long
        non_reserved = [
            "ADD", "AFTER", "ALL", "ALTER", "ALWAYS", "ANALYZE", "AND", "ANY", "ANY_VALUE", "ARCHIVE", 
            "ARRAY", "AS", "ASC", "AT", "AUTHORIZATION", "BETWEEN", "BOTH", "BUCKET", "BUCKETS", "BY", 
            "CACHE", "CASCADE", "CASE", "CAST", "CATALOG", "CATALOGS", "CHANGE", "CHECK", "CLEAR", 
            "CLUSTER", "CLUSTERED", "CODEGEN", "COLLATE", "COLLECTION", "COLUMN", "COLUMNS", "COMMENT", 
            "COMMIT", "COMPACT", "COMPACTIONS", "COMPUTE", "CONCATENATE", "CONSTRAINT", "COST", "CREATE", 
            "CUBE", "CURRENT", "CURRENT_DATE", "CURRENT_TIME", "CURRENT_TIMESTAMP", "CURRENT_USER", "DATA", 
            "DATABASE", "DATABASES", "DATEADD", "DATEDIFF", "DAY", "DAYS", "DAYOFYEAR", "DBPROPERTIES", 
            "DEFAULT", "DEFINED", "DELETE", "DELIMITED", "DESC", "DESCRIBE", "DFS", "DIRECTORIES", 
            "DIRECTORY", "DISTINCT", "DISTRIBUTE", "DIV", "DROP", "ELSE", "END", "ESCAPE", "ESCAPED", 
            "EXCHANGE", "EXCLUDE", "EXISTS", "EXPLAIN", "EXPORT", "EXTENDED", "EXTERNAL", "EXTRACT", 
            "FALSE", "FETCH", "FILTER", "FIELDS", "FILEFORMAT", "FIRST", "FOLLOWING", "FOR", "FOREIGN", 
            "FORMAT", "FORMATTED", "FROM", "FUNCTION", "FUNCTIONS", "GENERATED", "GLOBAL", "GRANT", 
            "GROUP", "GROUPING", "HAVING", "HOUR", "HOURS", "IF", "IGNORE", "IMPORT", "IN", "INCLUDE", 
            "INDEX", "INDEXES", "INPATH", "INPUTFORMAT", "INSERT", "INTERVAL", "INTO", "IS", "ITEMS", 
            "KEYS", "LAST", "LAZY", "LEADING", "LIKE", "ILIKE", "LIMIT", "LINES", "LIST", "LOAD", 
            "LOCAL", "LOCATION", "LOCK", "LOCKS", "LOGICAL", "MACRO", "MAP", "MATCHED", "MERGE", 
            "MICROSECOND", "MICROSECONDS", "MILLISECOND", "MILLISECONDS", "MINUTE", "MINUTES", "MONTH", 
            "MONTHS", "MSCK", "NAMESPACE", "NAMESPACES", "NANOSECOND", "NANOSECONDS", "NO", "NOT", 
            "NULL", "NULLS", "OF", "OFFSET", "ONLY", "OPTION", "OPTIONS", "OR", "ORDER", "OUT", "OUTER", 
            "OUTPUTFORMAT", "OVER", "OVERLAPS", "OVERLAY", "OVERWRITE", "PARTITION", "PARTITIONED", 
            "PARTITIONS", "PERCENTILE_CONT", "PERCENTILE_DISC", "PERCENTLIT", "PIVOT", "PLACING", 
            "POSITION", "PRECEDING", "PRIMARY", "PRINCIPALS", "PROPERTIES", "PURGE", "QUARTER", "QUERY", 
            "RANGE", "RECORDREADER", "RECORDWRITER", "RECOVER", "REDUCE", "REFERENCES", "REFRESH", 
            "RENAME", "REPAIR", "REPEATABLE", "REPLACE", "RESET", "RESPECT", "RESTRICT", "REVOKE", 
            "RLIKE", "ROLE", "ROLES", "ROLLBACK", "ROLLUP", "ROW", "ROWS", "SCHEMA", "SCHEMAS", "SECOND", 
            "SECONDS", "SELECT", "SEPARATED", "SERDE", "SERDEPROPERTIES", "SESSION_USER", "SET", "SETS", 
            "SHOW", "SKEWED", "SOME", "SORT", "SORTED", "SOURCE", "START", "STATISTICS", "STORED", 
            "STRATIFY", "STRUCT", "SUBSTR", "SUBSTRING", "SYNC", "SYSTEM_TIME", "SYSTEM_VERSION", "TABLE", 
            "TABLES", "TABLESAMPLE", "TARGET", "TBLPROPERTIES", "TEMPORARY", "TERMINATED", "THEN", "TIME", 
            "TIMESTAMP", "TIMESTAMPADD", "TIMESTAMPDIFF", "TO", "TOUCH", "TRAILING", "TRANSACTION", 
            "TRANSACTIONS", "TRANSFORM", "TRIM", "TRUE", "TRUNCATE", "TRY_CAST", "TYPE", "UNARCHIVE", 
            "UNBOUNDED", "UNCACHE", "UNIQUE", "UNKNOWN", "UNLOCK", "UNPIVOT", "UNSET", "UPDATE", "USE", 
            "USER", "VALUES", "VERSION", "VIEW", "VIEWS", "WEEK", "WEEKS", "WHEN", "WHERE", "WINDOW", 
            "WITH", "WITHIN", "YEAR", "YEARS", "ZONE"
        ]
        
        return self.current_token()[1].upper() in non_reserved
    
    def quotedIdentifier(self):
        """
        quotedIdentifier
            : BACKQUOTED_IDENTIFIER
            | {double_quoted_identifiers}? DOUBLEQUOTED_STRING
        """
        if self.current_token() and self.current_token()[0] == self.lexer.BACKQUOTED_IDENTIFIER:
            identifier = self.current_token()[1]
            self.next_token()
            return {"type": "quotedIdentifier", "value": identifier}
        elif self.double_quoted_identifiers and self.current_token() and self.current_token()[0] == self.lexer.DOUBLEQUOTED_STRING:
            identifier = self.current_token()[1]
            self.next_token()
            return {"type": "quotedIdentifier", "value": identifier}
        else:
            raise SyntaxError(f"Expected quoted identifier, got {self.current_token()[1] if self.current_token() else 'EOF'}")
    
    def whereClause(self):
        """
        whereClause
            : WHERE booleanExpression
        """
        self.match_keyword("WHERE")
        return {"type": "whereClause", "expression": self.booleanExpression()}
    
    def havingClause(self):
        """
        havingClause
            : HAVING booleanExpression
        """
        self.match_keyword("HAVING")
        return {"type": "havingClause", "expression": self.booleanExpression()}
    
    def hint(self):
        """
        hint
            : HENT_START hintStatements+=hintStatement (COMMA? hintStatements+=hintStatement)* HENT_END
        """
        self.expect(self.lexer.HENT_START)
        
        statements = [self.hintStatement()]
        
        while self.current_token() and (self.current_token()[0] == self.lexer.COMMA or self.current_token()[0] != self.lexer.HENT_END):
            if self.current_token()[0] == self.lexer.COMMA:
                self.next_token()
            
            statements.append(self.hintStatement())
        
        self.expect(self.lexer.HENT_END)
        
        return {"type": "hint", "statements": statements}
    
    def hintStatement(self):
        """
        hintStatement
            : hintName=identifier
            | hintName=identifier LEFT_PAREN parameters+=primaryExpression (COMMA parameters+=primaryExpression)* RIGHT_PAREN
        """
        name = self.identifier()
        
        parameters = []
        if self.current_token() and self.current_token()[0] == self.lexer.LEFT_PAREN:
            self.next_token()
            
            parameters.append(self.primaryExpression())
            
            while self.current_token() and self.current_token()[0] == self.lexer.COMMA:
                self.next_token()
                parameters.append(self.primaryExpression())
            
            self.expect(self.lexer.RIGHT_PAREN)
        
        return {"type": "hintStatement", "name": name, "parameters": parameters}
    
    def booleanExpression(self):
        """
        booleanExpression
            : NOT booleanExpression                                        #logicalNot
            | EXISTS LEFT_PAREN query RIGHT_PAREN                          #exists
            | valueExpression predicate?                                   #predicated
            | left=booleanExpression operator=AND right=booleanExpression  #logicalBinary
            | left=booleanExpression operator=OR right=booleanExpression   #logicalBinary
        """
        if self.check_keyword("NOT") and not self.isPredicateKeyword(1):
            self.next_token()
            return {"type": "logicalNot", "expression": self.booleanExpression()}
        elif self.check_keyword("EXISTS"):
            self.next_token()
            self.expect(self.lexer.LEFT_PAREN)
            query = self.query()
            self.expect(self.lexer.RIGHT_PAREN)
            return {"type": "exists", "query": query}
        else:
            expr = self.valueExpression()
            
            # Check for a predicate
            if self.isPredicateStart():
                predicate = self.predicate()
                expr = {"type": "predicated", "expression": expr, "predicate": predicate}
            
            # Check for AND/OR operators
            while self.current_token() and (self.check_keyword("AND") or self.check_keyword("OR")):
                operator = self.current_token()[1]
                self.next_token()
                
                right = self.booleanExpression()
                
                expr = {"type": "logicalBinary", "left": expr, "operator": operator, "right": right}
            
            return expr
    
    def isPredicateKeyword(self, lookahead=0):
        """Check if the token at the given lookahead position is a predicate keyword."""
        token = self.peek_token(lookahead) if lookahead > 0 else self.current_token()
        if not token:
            return False
        
        predicate_keywords = ["IN", "BETWEEN", "LIKE", "ILIKE", "RLIKE", "IS", "NULL", "TRUE", "FALSE", "UNKNOWN", "DISTINCT"]
        
        return token[1].upper() in predicate_keywords
    
    def isPredicateStart(self):
        """Check if the current token can start a predicate."""
        if not self.current_token():
            return False
        
        if self.check_keyword("NOT") and self.isPredicateKeyword(1):
            return True
        
        return self.isPredicateKeyword()
    
    def predicate(self):
        """
        predicate
            : NOT? kind=BETWEEN lower=valueExpression AND upper=valueExpression
            : NOT? kind=IN LEFT_PAREN expression (COMMA expression)* RIGHT_PAREN
            : NOT? kind=IN LEFT_PAREN query RIGHT_PAREN
            : NOT? kind=RLIKE pattern=valueExpression
            : NOT? kind=(LIKE | ILIKE) quantifier=(ANY | SOME | ALL) (LEFT_PAREN RIGHT_PAREN | LEFT_PAREN expression (COMMA expression)* RIGHT_PAREN)
            : NOT? kind=(LIKE | ILIKE) pattern=valueExpression (ESCAPE escapeChar=stringLit)?
            : IS NOT? kind=NULL
            : IS NOT? kind=(TRUE | FALSE | UNKNOWN)
            : IS NOT? kind=DISTINCT FROM right=valueExpression
        """
        # Handle NOT prefix
        has_not = False
        if self.check_keyword("NOT"):
            has_not = True
            self.next_token()
        
        if self.check_keyword("BETWEEN"):
            self.next_token()
            lower = self.valueExpression()
            self.match_keyword("AND")
            upper = self.valueExpression()
            return {"type": "between", "not": has_not, "lower": lower, "upper": upper}
        elif self.check_keyword("IN"):
            self.next_token()
            self.expect(self.lexer.LEFT_PAREN)
            
            # Check if it's a query or a list of expressions
            saved_index = self.current_token_index
            is_query = False
            
            try:
                if (self.check_keyword("SELECT") or 
                    self.check_keyword("FROM") or 
                    self.check_keyword("VALUES") or 
                    self.check_keyword("TABLE") or
                    (self.current_token() and self.current_token()[0] == self.lexer.LEFT_PAREN)):
                    is_query = True
            finally:
                self.current_token_index = saved_index
            
            if is_query:
                query = self.query()
                self.expect(self.lexer.RIGHT_PAREN)
                return {"type": "inQuery", "not": has_not, "query": query}
            else:
                expressions = [self.expression()]
                
                while self.current_token() and self.current_token()[0] == self.lexer.COMMA:
                    self.next_token()
                    expressions.append(self.expression())
                
                self.expect(self.lexer.RIGHT_PAREN)
                return {"type": "inList", "not": has_not, "expressions": expressions}
        elif self.check_keyword("RLIKE"):
            self.next_token()
            pattern = self.valueExpression()
            return {"type": "rlike", "not": has_not, "pattern": pattern}
        elif self.check_keyword("LIKE") or self.check_keyword("ILIKE"):
            kind = self.current_token()[1]
            self.next_token()
            
            if self.check_keyword("ANY") or self.check_keyword("SOME") or self.check_keyword("ALL"):
                quantifier = self.current_token()[1]
                self.next_token()
                
                self.expect(self.lexer.LEFT_PAREN)
                
                if self.current_token() and self.current_token()[0] == self.lexer.RIGHT_PAREN:
                    self.next_token()
                    return {"type": "likeAny", "not": has_not, "kind": kind, "quantifier": quantifier, "expressions": []}
                else:
                    expressions = [self.expression()]
                    
                    while self.current_token() and self.current_token()[0] == self.lexer.COMMA:
                        self.next_token()
                        expressions.append(self.expression())
                    
                    self.expect(self.lexer.RIGHT_PAREN)
                    return {"type": "likeAny", "not": has_not, "kind": kind, "quantifier": quantifier, "expressions": expressions}
            else:
                pattern = self.valueExpression()
                
                escape = None
                if self.check_keyword("ESCAPE"):
                    self.next_token()
                    escape = self.stringLit()
                
                return {"type": "like", "not": has_not, "kind": kind, "pattern": pattern, "escape": escape}
        elif self.check_keyword("IS"):
            self.next_token()
            
            is_not = False
            if self.check_keyword("NOT"):
                is_not = True
                self.next_token()
            
            if self.check_keyword("NULL"):
                self.next_token()
                return {"type": "isNull", "not": is_not}
            elif self.check_keyword("TRUE"):
                self.next_token()
                return {"type": "isTrue", "not": is_not}
            elif self.check_keyword("FALSE"):
                self.next_token()
                return {"type": "isFalse", "not": is_not}
            elif self.check_keyword("UNKNOWN"):
                self.next_token()
                return {"type": "isUnknown", "not": is_not}
            elif self.check_keyword("DISTINCT"):
                self.next_token()
                self.match_keyword("FROM")
                right = self.valueExpression()
                return {"type": "isDistinct", "not": is_not, "right": right}
            else:
                raise SyntaxError(f"Expected NULL, TRUE, FALSE, UNKNOWN, or DISTINCT after IS NOT?, got {self.current_token()[1] if self.current_token() else 'EOF'}")
        else:
            raise SyntaxError(f"Expected predicate, got {self.current_token()[1] if self.current_token() else 'EOF'}")
    
    def valueExpression(self):
        """
        valueExpression
            : primaryExpression                                                                      #valueExpressionDefault
            | operator=(MINUS | PLUS | TILDE) valueExpression                                        #arithmeticUnary
            | left=valueExpression operator=(ASTERISK | SLASH | PERCENT | DIV) right=valueExpression #arithmeticBinary
            | left=valueExpression operator=(PLUS | MINUS | CONCAT_PIPE) right=valueExpression       #arithmeticBinary
            | left=valueExpression operator=AMPERSAND right=valueExpression                          #arithmeticBinary
            | left=valueExpression operator=HAT right=valueExpression                                #arithmeticBinary
            | left=valueExpression operator=PIPE right=valueExpression                               #arithmeticBinary
            | left=valueExpression comparisonOperator right=valueExpression                          #comparison
        """
        # Handle unary operators
        if self.current_token() and (self.current_token()[0] == self.lexer.MINUS or 
                                    self.current_token()[0] == self.lexer.PLUS or 
                                    self.current_token()[0] == self.lexer.TILDE):
            operator = self.current_token()[1]
            self.next_token()
            expr = self.valueExpression()
            return {"type": "arithmeticUnary", "operator": operator, "expression": expr}
        
        # Start with a primary expression
        expr = self.primaryExpression()
        
        # Handle binary operators with appropriate precedence
        while self.current_token() and self.isBinaryOperator():
            if self.isMultiplicativeOperator():
                operator = self.current_token()[1]
                self.next_token()
                right = self.primaryExpression()
                expr = {"type": "arithmeticBinary", "left": expr, "operator": operator, "right": right}
            elif self.isAdditiveOperator():
                operator = self.current_token()[1]
                self.next_token()
                right = self.primaryExpression()
                expr = {"type": "arithmeticBinary", "left": expr, "operator": operator, "right": right}
            elif self.isBitwiseOperator():
                operator = self.current_token()[1]
                self.next_token()
                right = self.primaryExpression()
                expr = {"type": "arithmeticBinary", "left": expr, "operator": operator, "right": right}
            elif self.isComparisonOperator():
                operator = self.current_token()[1]
                self.next_token()
                right = self.valueExpression()
                expr = {"type": "comparison", "left": expr, "operator": operator, "right": right}
                break  # Comparison has lower precedence, so stop after one
            else:
                break
        
        return expr
    
    def isBinaryOperator(self):
        """Check if the current token is a binary operator."""
        return (self.isMultiplicativeOperator() or 
                self.isAdditiveOperator() or 
                self.isBitwiseOperator() or 
                self.isComparisonOperator())
    
    def isMultiplicativeOperator(self):
        """Check if the current token is a multiplicative operator."""
        return (self.current_token() and 
                (self.current_token()[0] == self.lexer.ASTERISK or 
                 self.current_token()[0] == self.lexer.SLASH or 
                 self.current_token()[0] == self.lexer.PERCENT or 
                 self.check_keyword("DIV")))
    
    def isAdditiveOperator(self):
        """Check if the current token is an additive operator."""
        return (self.current_token() and 
                (self.current_token()[0] == self.lexer.PLUS or 
                 self.current_token()[0] == self.lexer.MINUS or 
                 self.current_token()[0] == self.lexer.CONCAT_PIPE))
    
    def isBitwiseOperator(self):
        """Check if the current token is a bitwise operator."""
        return (self.current_token() and 
                (self.current_token()[0] == self.lexer.AMPERSAND or 
                 self.current_token()[0] == self.lexer.HAT or 
                 self.current_token()[0] == self.lexer.PIPE))
    
    def isComparisonOperator(self):
        """Check if the current token is a comparison operator."""
        return (self.current_token() and 
                (self.current_token()[0] == self.lexer.EQ or 
                 self.current_token()[0] == self.lexer.NEQ or 
                 self.current_token()[0] == self.lexer.NEQJ or 
                 self.current_token()[0] == self.lexer.LT or 
                 self.current_token()[0] == self.lexer.LTE or 
                 self.current_token()[0] == self.lexer.GT or 
                 self.current_token()[0] == self.lexer.GTE or 
                 self.current_token()[0] == self.lexer.NSEQ))
    
    def primaryExpression(self):
        """Implementation of primaryExpression rule from the grammar."""
        if not self.current_token():
            raise SyntaxError("Unexpected end of input in primaryExpression")
        
        try:
            # Check for current-like expressions
            if self.check_keyword("CURRENT_DATE") or self.check_keyword("CURRENT_TIMESTAMP") or \
            self.check_keyword("CURRENT_USER") or self.check_keyword("USER"):
                function_name = self.current_token()[1]
                self.next_token()
                return {"type": "currentLike", "name": function_name}
            
            # Check for TIMESTAMPADD, DATEADD
            if self.check_keyword("TIMESTAMPADD") or self.check_keyword("DATEADD"):
                function_name = self.current_token()[1]
                self.next_token()
                self.expect(self.lexer.LEFT_PAREN)
                unit = self.datetimeUnit() if hasattr(self, 'datetimeUnit') else self.identifier()
                self.expect(self.lexer.COMMA)
                units_amount = self.valueExpression()
                self.expect(self.lexer.COMMA)
                timestamp = self.valueExpression()
                self.expect(self.lexer.RIGHT_PAREN)
                return {
                    "type": "timestampadd",
                    "name": function_name,
                    "unit": unit,
                    "unitsAmount": units_amount,
                    "timestamp": timestamp
                }
            
            # Check for TIMESTAMPDIFF, DATEDIFF
            if self.check_keyword("TIMESTAMPDIFF") or self.check_keyword("DATEDIFF"):
                function_name = self.current_token()[1]
                self.next_token()
                self.expect(self.lexer.LEFT_PAREN)
                unit = self.datetimeUnit() if hasattr(self, 'datetimeUnit') else self.identifier()
                self.expect(self.lexer.COMMA)
                start_timestamp = self.valueExpression()
                self.expect(self.lexer.COMMA)
                end_timestamp = self.valueExpression()
                self.expect(self.lexer.RIGHT_PAREN)
                return {
                    "type": "timestampdiff",
                    "name": function_name,
                    "unit": unit,
                    "startTimestamp": start_timestamp,
                    "endTimestamp": end_timestamp
                }
            
            # Check for CASE expressions
            if self.check_keyword("CASE"):
                self.next_token()
                
                # Check if it's a simple or searched CASE
                if not self.check_keyword("WHEN"):
                    # Simple CASE
                    value = self.expression()
                    when_clauses = []
                    
                    while self.check_keyword("WHEN"):
                        when_clauses.append(self.whenClause() if hasattr(self, 'whenClause') else self.parseWhenClause())
                    
                    else_expression = None
                    if self.check_keyword("ELSE"):
                        self.next_token()
                        else_expression = self.expression()
                    
                    if self.check_keyword("END"):
                        self.next_token()
                    else:
                        raise SyntaxError("Expected END keyword for CASE expression")
                    
                    return {
                        "type": "simpleCase",
                        "value": value,
                        "whenClauses": when_clauses,
                        "elseExpression": else_expression
                    }
                else:
                    # Searched CASE
                    when_clauses = []
                    
                    while self.check_keyword("WHEN"):
                        when_clauses.append(self.whenClause() if hasattr(self, 'whenClause') else self.parseWhenClause())
                    
                    else_expression = None
                    if self.check_keyword("ELSE"):
                        self.next_token()
                        else_expression = self.expression()
                    
                    if self.check_keyword("END"):
                        self.next_token()
                    else:
                        raise SyntaxError("Expected END keyword for CASE expression")
                    
                    return {
                        "type": "searchedCase",
                        "whenClauses": when_clauses,
                        "elseExpression": else_expression
                    }
            
            # Check for constants before checking functions/identifiers
            if (self.check_keyword("NULL") or 
                self.check_keyword("TRUE") or 
                self.check_keyword("FALSE") or
                self.current_token()[0] in [self.lexer.INTEGER_VALUE, 
                                        self.lexer.DECIMAL_VALUE,
                                        self.lexer.STRING]):
                return self.constant()
            
            # Check for parenthesized expression
            if self.current_token()[0] == self.lexer.LEFT_PAREN:
                self.next_token()
                expr = self.expression()
                self.expect(self.lexer.RIGHT_PAREN)
                return {"type": "parenthesizedExpression", "expression": expr}
            
            # Simple identifier reference (column reference) - fallback for most cases
            if self.current_token()[0] == self.lexer.IDENTIFIER:
                identifier = self.identifier()
                
                # Check for function calls immediately after a identifier
                if self.current_token() and self.current_token()[0] == self.lexer.LEFT_PAREN:
                    self.next_token()  # consume LEFT_PAREN
                    
                    arguments = []
                    if not self.check_token(self.lexer.RIGHT_PAREN):
                        arguments.append(self.expression())
                        
                        while self.current_token() and self.current_token()[0] == self.lexer.COMMA:
                            self.next_token()
                            arguments.append(self.expression())
                    
                    self.expect(self.lexer.RIGHT_PAREN)
                    
                    return {
                        "type": "functionCall",
                        "functionName": {"type": "qualifiedName", "identifiers": [identifier]},
                        "arguments": arguments
                    }
                
                # Check for field access (dereference)
                if self.current_token() and self.current_token()[0] == self.lexer.DOT:
                    base_expr = {"type": "columnReference", "identifier": identifier}
                    
                    # We support multiple levels of field access (a.b.c)
                    while self.current_token() and self.current_token()[0] == self.lexer.DOT:
                        self.next_token()  # consume DOT
                        
                        # Special case for star: a.*
                        if self.current_token() and self.current_token()[0] == self.lexer.ASTERISK:
                            self.next_token()  # consume *
                            return {"type": "star", "qualifiedName": base_expr}
                        
                        field_name = self.identifier()
                        base_expr = {
                            "type": "dereference",
                            "base": base_expr,
                            "fieldName": field_name
                        }
                    
                    return base_expr
                
                # Just a simple column reference
                return {"type": "columnReference", "identifier": identifier}
            
            # Star expression (SELECT *)
            if self.current_token()[0] == self.lexer.ASTERISK:
                self.next_token()
                return {"type": "star"}
            
            # If we reach here, we couldn't recognize the expression
            raise SyntaxError(f"Unexpected token in primaryExpression: {self.current_token()[1] if self.current_token() else 'None'}")
        
        except Exception as e:
            # Provide a more helpful error message that includes the token position
            if isinstance(e, SyntaxError):
                token_info = ""
                if self.current_token():
                    token_info = f" at position {self.current_token_index}, token: {self.current_token()[1]}"
                raise SyntaxError(f"{str(e)}{token_info}")
            raise
        
    def parseWhenClause(self):
        """Helper method for parsing WHEN clauses in CASE expressions."""
        self.expect_keyword("WHEN")
        condition = self.expression()
        self.expect_keyword("THEN")
        result = self.expression()
        
        return {
            "type": "whenClause",
            "condition": condition,
            "result": result
        }

    def expect_keyword(self, keyword):
        """Expect a specific keyword, consume it if found, otherwise raise an error."""
        if self.check_keyword(keyword):
            self.next_token()
            return True
        raise SyntaxError(f"Expected keyword {keyword}, got {self.current_token()[1] if self.current_token() else 'EOF'}")


    def expect_keyword(self, keyword):
        """Expect a specific keyword, consume it if found, otherwise raise an error."""
        if self.check_keyword(keyword):
            self.next_token()
            return True
        raise SyntaxError(f"Expected keyword {keyword}, got {self.current_token()[1] if self.current_token() else 'EOF'}")

    def datetimeUnit(self):
        """
        datetimeUnit
            : YEAR | QUARTER | MONTH
            | WEEK | DAY | DAYOFYEAR
            | HOUR | MINUTE | SECOND | MILLISECOND | MICROSECOND
        """
        datetime_units = [
            "YEAR", "QUARTER", "MONTH", "WEEK", "DAY", "DAYOFYEAR",
            "HOUR", "MINUTE", "SECOND", "MILLISECOND", "MICROSECOND"
        ]
        
        if self.check_keyword_in_list(datetime_units):
            unit = self.current_token()[1].upper()
            self.next_token()
            return unit
        
        raise SyntaxError(f"Expected datetime unit, got {self.current_token()[1] if self.current_token() else 'EOF'}")

    def check_keyword_in_list(self, keywords):
        """Check if the current token is a keyword in the provided list."""
        if not self.current_token():
            return False
        
        return self.current_token()[1].upper() in keywords

    def whenClause(self):
        """
        whenClause
            : WHEN condition=expression THEN result=expression
        """
        self.expect_keyword("WHEN")
        condition = self.expression()
        self.expect_keyword("THEN")
        result = self.expression()
        
        return {
            "type": "whenClause",
            "condition": condition,
            "result": result
        }

    def windowSpec(self):
        """
        windowSpec
            : name=errorCapturingIdentifier                         #windowRef
            | LEFT_PAREN name=errorCapturingIdentifier RIGHT_PAREN  #windowRef
            | LEFT_PAREN
            ( CLUSTER BY partition+=expression (COMMA partition+=expression)*
            | ((PARTITION | DISTRIBUTE) BY partition+=expression (COMMA partition+=expression)*)?
                ((ORDER | SORT) BY sortItem (COMMA sortItem)*)?)
            windowFrame?
            RIGHT_PAREN                                           #windowDef
        """
        if self.current_token()[0] == self.lexer.IDENTIFIER:
            name = self.errorCapturingIdentifier()
            return {"type": "windowRef", "name": name}
        elif self.current_token()[0] == self.lexer.LEFT_PAREN and self.peek_token()[0] == self.lexer.IDENTIFIER and self.peek_token(2) and self.peek_token(2)[0] == self.lexer.RIGHT_PAREN:
            self.next_token()
            name = self.errorCapturingIdentifier()
            self.expect(self.lexer.RIGHT_PAREN)
            return {"type": "windowRef", "name": name}
        else:
            self.expect(self.lexer.LEFT_PAREN)
            
            partition_by = []
            order_by = []
            
            # CLUSTER BY
            if self.check_keyword("CLUSTER"):
                self.next_token()
                self.expect_keyword("BY")
                
                partition_by.append(self.expression())
                
                while self.current_token()[0] == self.lexer.COMMA:
                    self.next_token()
                    partition_by.append(self.expression())
            else:
                # PARTITION BY or DISTRIBUTE BY
                if self.check_keyword("PARTITION") or self.check_keyword("DISTRIBUTE"):
                    self.next_token()
                    self.expect_keyword("BY")
                    
                    partition_by.append(self.expression())
                    
                    while self.current_token()[0] == self.lexer.COMMA:
                        self.next_token()
                        partition_by.append(self.expression())
                
                # ORDER BY or SORT BY
                if self.check_keyword("ORDER") or self.check_keyword("SORT"):
                    self.next_token()
                    self.expect_keyword("BY")
                    
                    order_by.append(self.sortItem())
                    
                    while self.current_token()[0] == self.lexer.COMMA:
                        self.next_token()
                        order_by.append(self.sortItem())
            
            # Window frame
            window_frame = None
            if self.check_keyword("RANGE") or self.check_keyword("ROWS"):
                window_frame = self.windowFrame()
            
            self.expect(self.lexer.RIGHT_PAREN)
            
            return {
                "type": "windowDef",
                "partitionBy": partition_by,
                "orderBy": order_by,
                "windowFrame": window_frame
            }
    def constant(self):
        """Implement a basic subset of the constant rule."""
        if self.check_keyword("NULL"):
            self.next_token()
            return {"type": "nullLiteral"}
        elif self.check_keyword("TRUE"):
            self.next_token()
            return {"type": "booleanLiteral", "value": True}
        elif self.check_keyword("FALSE"):
            self.next_token()
            return {"type": "booleanLiteral", "value": False}
        elif self.current_token()[0] in [self.lexer.INTEGER_VALUE, self.lexer.DECIMAL_VALUE, 
                                        self.lexer.EXPONENT_VALUE, self.lexer.BIGINT_LITERAL, 
                                        self.lexer.SMALLINT_LITERAL, self.lexer.TINYINT_LITERAL, 
                                        self.lexer.DOUBLE_LITERAL, self.lexer.FLOAT_LITERAL, 
                                        self.lexer.BIGDECIMAL_LITERAL]:
            value = self.current_token()[1]
            token_type = self.current_token()[0]
            self.next_token()
            return {"type": "numericLiteral", "value": value, "tokenType": token_type}
        elif self.current_token()[0] == self.lexer.STRING or self.current_token()[0] == self.lexer.DOUBLEQUOTED_STRING:
            value = self.current_token()[1]
            self.next_token()
            
            # Handle concatenated string literals like 'a' 'b' -> 'ab'
            strings = [value]
            while self.current_token() and (self.current_token()[0] == self.lexer.STRING or self.current_token()[0] == self.lexer.DOUBLEQUOTED_STRING):
                strings.append(self.current_token()[1])
                self.next_token()
            
            return {"type": "stringLiteral", "value": strings}
        else:
            raise SyntaxError(f"Expected constant, got {self.current_token()[1] if self.current_token() else 'EOF'}")
    
    def expression(self):
        """
        expression
            : booleanExpression
        """
        return self.booleanExpression()
    
    def stringLit(self):
        """
        stringLit
            : STRING
            | {!double_quoted_identifiers}? DOUBLEQUOTED_STRING
        """
        if self.current_token() and self.current_token()[0] == self.lexer.STRING:
            value = self.current_token()[1]
            self.next_token()
            return value
        elif not self.double_quoted_identifiers and self.current_token() and self.current_token()[0] == self.lexer.DOUBLEQUOTED_STRING:
            value = self.current_token()[1]
            self.next_token()
            return value
        else:
            raise SyntaxError(f"Expected string literal, got {self.current_token()[1] if self.current_token() else 'EOF'}")
    
    def namedExpression(self):
        """
        namedExpression
            : expression (AS? (name=errorCapturingIdentifier | identifierList))?
        """
        expr = self.expression()
        
        alias = None
        if (self.current_token() and 
            (self.check_keyword("AS") or 
             self.current_token()[0] == self.lexer.IDENTIFIER or 
             self.current_token()[0] == self.lexer.BACKQUOTED_IDENTIFIER or
             (self.double_quoted_identifiers and self.current_token()[0] == self.lexer.DOUBLEQUOTED_STRING) or
             self.current_token()[0] == self.lexer.LEFT_PAREN)):
            
            if self.check_keyword("AS"):
                self.next_token()
            
            if self.current_token() and self.current_token()[0] == self.lexer.LEFT_PAREN:
                alias = self.identifierList()
            else:
                alias = self.errorCapturingIdentifier()
        
        return {"type": "namedExpression", "expression": expr, "alias": alias}
    
    def namedExpressionSeq(self):
        """
        namedExpressionSeq
            : namedExpression (COMMA namedExpression)*
        """
        expressions = [self.namedExpression()]
        
        while self.current_token() and self.current_token()[0] == self.lexer.COMMA:
            self.next_token()
            expressions.append(self.namedExpression())
        
        return expressions
    
    def multipartIdentifier(self):
        """
        multipartIdentifier
            : parts+=errorCapturingIdentifier (DOT parts+=errorCapturingIdentifier)*
        """
        parts = [self.errorCapturingIdentifier()]
        
        while self.current_token() and self.current_token()[0] == self.lexer.DOT:
            self.next_token()
            parts.append(self.errorCapturingIdentifier())
        
        return {"type": "multipartIdentifier", "parts": parts}
    
    def tableIdentifier(self):
        """
        tableIdentifier
            : (db=errorCapturingIdentifier DOT)? table=errorCapturingIdentifier
        """
        db = None
        if (self.peek_token() and self.peek_token()[0] == self.lexer.DOT):
            db = self.errorCapturingIdentifier()
            self.expect(self.lexer.DOT)
        
        table = self.errorCapturingIdentifier()
        
        return {"type": "tableIdentifier", "db": db, "table": table}
    
    def functionIdentifier(self):
        """
        functionIdentifier
            : (db=errorCapturingIdentifier DOT)? function=errorCapturingIdentifier
        """
        db = None
        if (self.peek_token() and self.peek_token()[0] == self.lexer.DOT):
            db = self.errorCapturingIdentifier()
            self.expect(self.lexer.DOT)
        
        function = self.errorCapturingIdentifier()
        
        return {"type": "functionIdentifier", "db": db, "function": function}
    
    def lateralView(self):
        """
        lateralView
            : LATERAL VIEW (OUTER)? qualifiedName LEFT_PAREN (expression (COMMA expression)*)? RIGHT_PAREN tblName=identifier (AS? colName+=identifier (COMMA colName+=identifier)*)?
        """
        self.match_keyword("LATERAL")
        self.match_keyword("VIEW")
        
        is_outer = False
        if self.check_keyword("OUTER"):
            is_outer = True
            self.next_token()
        
        qualified_name = self.qualifiedName()
        
        self.expect(self.lexer.LEFT_PAREN)
        
        expressions = []
        if not self.check_token(self.lexer.RIGHT_PAREN):
            expressions.append(self.expression())
            
            while self.current_token() and self.current_token()[0] == self.lexer.COMMA:
                self.next_token()
                expressions.append(self.expression())
        
        self.expect(self.lexer.RIGHT_PAREN)
        
        table_name = self.identifier()
        
        column_names = []
        if self.check_keyword("AS"):
            self.next_token()
            column_names.append(self.identifier())
            
            while self.current_token() and self.current_token()[0] == self.lexer.COMMA:
                self.next_token()
                column_names.append(self.identifier())
        elif self.current_token() and self.current_token()[0] == self.lexer.IDENTIFIER:
            column_names.append(self.identifier())
            
            while self.current_token() and self.current_token()[0] == self.lexer.COMMA:
                self.next_token()
                column_names.append(self.identifier())
        
        return {
            "type": "lateralView",
            "isOuter": is_outer,
            "qualifiedName": qualified_name,
            "expressions": expressions,
            "tableName": table_name,
            "columnNames": column_names
        }

    def pivotClause(self):
        """
        pivotClause
            : PIVOT LEFT_PAREN aggregates=namedExpressionSeq FOR pivotColumn IN LEFT_PAREN pivotValues+=pivotValue (COMMA pivotValues+=pivotValue)* RIGHT_PAREN RIGHT_PAREN
        """
        self.match_keyword("PIVOT")
        self.expect(self.lexer.LEFT_PAREN)
        
        # Parse the aggregation expressions
        aggregates = self.namedExpressionSeq()
        
        self.match_keyword("FOR")
        
        # Parse pivot column
        pivot_column = self.pivotColumn()
        
        self.match_keyword("IN")
        self.expect(self.lexer.LEFT_PAREN)
        
        # Parse pivot values
        pivot_values = [self.pivotValue()]
        
        while self.current_token() and self.current_token()[0] == self.lexer.COMMA:
            self.next_token()
            pivot_values.append(self.pivotValue())
        
        self.expect(self.lexer.RIGHT_PAREN)
        self.expect(self.lexer.RIGHT_PAREN)
        
        return {
            "type": "pivotClause",
            "aggregates": aggregates,
            "pivotColumn": pivot_column,
            "pivotValues": pivot_values
        }

    def pivotColumn(self):
        """
        pivotColumn
            : identifiers+=identifier
            | LEFT_PAREN identifiers+=identifier (COMMA identifiers+=identifier)* RIGHT_PAREN
        """
        identifiers = []
        
        if self.current_token() and self.current_token()[0] == self.lexer.LEFT_PAREN:
            self.next_token()
            identifiers.append(self.identifier())
            
            while self.current_token() and self.current_token()[0] == self.lexer.COMMA:
                self.next_token()
                identifiers.append(self.identifier())
            
            self.expect(self.lexer.RIGHT_PAREN)
        else:
            identifiers.append(self.identifier())
        
        return {"type": "pivotColumn", "identifiers": identifiers}
    
    def pivotValue(self):
        """
        pivotValue
            : expression (AS? identifier)?
        """
        expression = self.expression()
        
        alias = None
        if self.check_keyword("AS"):
            self.next_token()
            alias = self.identifier()
        elif self.current_token() and self.current_token()[0] == self.lexer.IDENTIFIER:
            alias = self.identifier()
        
        return {"type": "pivotValue", "expression": expression, "alias": alias}


    def unpivotClause(self):
        """
        unpivotClause
            : UNPIVOT nullOperator=unpivotNullClause? LEFT_PAREN
                operator=unpivotOperator
            RIGHT_PAREN (AS? identifier)?
        """
        self.match_keyword("UNPIVOT")
        
        # Parse optional null operator
        null_operator = None
        if self.check_keyword("INCLUDE") or self.check_keyword("EXCLUDE"):
            null_operator = self.unpivotNullClause()
        
        self.expect(self.lexer.LEFT_PAREN)
        
        # Parse unpivot operator
        operator = self.unpivotOperator()
        
        self.expect(self.lexer.RIGHT_PAREN)
        
        # Parse optional alias
        alias = None
        if self.check_keyword("AS"):
            self.next_token()
            alias = self.identifier()
        elif self.current_token() and self.current_token()[0] == self.lexer.IDENTIFIER:
            alias = self.identifier()
        
        return {
            "type": "unpivotClause",
            "nullOperator": null_operator,
            "operator": operator,
            "alias": alias
        }

    def unpivotNullClause(self):
        """
        unpivotNullClause
            : (INCLUDE | EXCLUDE) NULLS
        """
        operator = None
        if self.check_keyword("INCLUDE"):
            operator = "INCLUDE"
            self.next_token()
        elif self.check_keyword("EXCLUDE"):
            operator = "EXCLUDE"
            self.next_token()
        else:
            raise SyntaxError(f"Expected INCLUDE or EXCLUDE, got {self.current_token()[1] if self.current_token() else 'EOF'}")
        
        self.match_keyword("NULLS")
        
        return {"type": "unpivotNullClause", "operator": operator}

    def unpivotOperator(self):
        """
        unpivotOperator
            : (unpivotSingleValueColumnClause | unpivotMultiValueColumnClause)
        """
        # Check which type of unpivot operation we have
        saved_index = self.current_token_index
        is_multi_value = False
        
        if self.current_token() and self.current_token()[0] == self.lexer.LEFT_PAREN:
            is_multi_value = True
        
        self.current_token_index = saved_index
        
        if is_multi_value:
            return self.unpivotMultiValueColumnClause()
        else:
            return self.unpivotSingleValueColumnClause()

    def unpivotSingleValueColumnClause(self):
        """
        unpivotSingleValueColumnClause
            : unpivotValueColumn FOR unpivotNameColumn IN LEFT_PAREN unpivotColumns+=unpivotColumnAndAlias (COMMA unpivotColumns+=unpivotColumnAndAlias)* RIGHT_PAREN
        """
        value_column = self.unpivotValueColumn()
        
        self.match_keyword("FOR")
        
        name_column = self.unpivotNameColumn()
        
        self.match_keyword("IN")
        self.expect(self.lexer.LEFT_PAREN)
        
        columns = [self.unpivotColumnAndAlias()]
        
        while self.current_token() and self.current_token()[0] == self.lexer.COMMA:
            self.next_token()
            columns.append(self.unpivotColumnAndAlias())
        
        self.expect(self.lexer.RIGHT_PAREN)
        
        return {
            "type": "unpivotSingleValueColumnClause",
            "valueColumn": value_column,
            "nameColumn": name_column,
            "columns": columns
        }

    def unpivotMultiValueColumnClause(self):
        """
        unpivotMultiValueColumnClause
            : LEFT_PAREN unpivotValueColumns+=unpivotValueColumn (COMMA unpivotValueColumns+=unpivotValueColumn)* RIGHT_PAREN
            FOR unpivotNameColumn
            IN LEFT_PAREN unpivotColumnSets+=unpivotColumnSet (COMMA unpivotColumnSets+=unpivotColumnSet)* RIGHT_PAREN
        """
        self.expect(self.lexer.LEFT_PAREN)
        
        value_columns = [self.unpivotValueColumn()]
        
        while self.current_token() and self.current_token()[0] == self.lexer.COMMA:
            self.next_token()
            value_columns.append(self.unpivotValueColumn())
        
        self.expect(self.lexer.RIGHT_PAREN)
        
        self.match_keyword("FOR")
        
        name_column = self.unpivotNameColumn()
        
        self.match_keyword("IN")
        self.expect(self.lexer.LEFT_PAREN)
        
        column_sets = [self.unpivotColumnSet()]
        
        while self.current_token() and self.current_token()[0] == self.lexer.COMMA:
            self.next_token()
            column_sets.append(self.unpivotColumnSet())
        
        self.expect(self.lexer.RIGHT_PAREN)
        
        return {
            "type": "unpivotMultiValueColumnClause",
            "valueColumns": value_columns,
            "nameColumn": name_column,
            "columnSets": column_sets
        }

    def unpivotColumnSet(self):
        """
        unpivotColumnSet
            : LEFT_PAREN unpivotColumns+=unpivotColumn (COMMA unpivotColumns+=unpivotColumn)* RIGHT_PAREN unpivotAlias?
        """
        self.expect(self.lexer.LEFT_PAREN)
        
        columns = [self.unpivotColumn()]
        
        while self.current_token() and self.current_token()[0] == self.lexer.COMMA:
            self.next_token()
            columns.append(self.unpivotColumn())
        
        self.expect(self.lexer.RIGHT_PAREN)
        
        alias = None
        if self.check_keyword("AS") or (self.current_token() and self.current_token()[0] == self.lexer.IDENTIFIER):
            alias = self.unpivotAlias()
        
        return {
            "type": "unpivotColumnSet",
            "columns": columns,
            "alias": alias
        }

    def unpivotValueColumn(self):
        """
        unpivotValueColumn
            : identifier
        """
        return {"type": "unpivotValueColumn", "identifier": self.identifier()}

    def unpivotNameColumn(self):
        """
        unpivotNameColumn
            : identifier
        """
        return {"type": "unpivotNameColumn", "identifier": self.identifier()}

    def unpivotColumnAndAlias(self):
        """
        unpivotColumnAndAlias
            : unpivotColumn unpivotAlias?
        """
        column = self.unpivotColumn()
        
        alias = None
        if self.check_keyword("AS") or (self.current_token() and self.current_token()[0] == self.lexer.IDENTIFIER):
            alias = self.unpivotAlias()
        
        return {
            "type": "unpivotColumnAndAlias",
            "column": column,
            "alias": alias
        }

    def unpivotColumn(self):
        """
        unpivotColumn
            : multipartIdentifier
        """
        return {"type": "unpivotColumn", "identifier": self.multipartIdentifier()}

    def unpivotAlias(self):
        """
        unpivotAlias
            : AS? identifier
        """
        if self.check_keyword("AS"):
            self.next_token()
        
        return {"type": "unpivotAlias", "identifier": self.identifier()}

    def check_token(self, token_type):
        """Check if the current token has a specific type without consuming it."""
        token = self.current_token()
        return token and token[0] == token_type

    def inlineTable(self):
        """
        inlineTable
            : VALUES expression (COMMA expression)* tableAlias
        """
        self.match_keyword("VALUES")
        
        expressions = [self.expression()]
        
        while self.current_token() and self.current_token()[0] == self.lexer.COMMA:
            self.next_token()
            expressions.append(self.expression())
        
        table_alias = self.tableAlias()
        
        return {
            "type": "inlineTable",
            "expressions": expressions,
            "tableAlias": table_alias
        }

    def functionTable(self):
        """
        functionTable
            : funcName=functionName LEFT_PAREN (expression (COMMA expression)*)? RIGHT_PAREN tableAlias
        """
        function_name = self.functionName()
        
        self.expect(self.lexer.LEFT_PAREN)
        
        expressions = []
        if not self.check_token(self.lexer.RIGHT_PAREN):
            expressions.append(self.expression())
            
            while self.current_token() and self.current_token()[0] == self.lexer.COMMA:
                self.next_token()
                expressions.append(self.expression())
        
        self.expect(self.lexer.RIGHT_PAREN)
        
        table_alias = self.tableAlias()
        
        return {
            "type": "functionTable",
            "functionName": function_name,
            "expressions": expressions,
            "tableAlias": table_alias
        }

    def functionName(self):
        """
        functionName
            : qualifiedName
            | FILTER
            | LEFT
            | RIGHT
        """
        if self.check_keyword("FILTER") or self.check_keyword("LEFT") or self.check_keyword("RIGHT"):
            keyword = self.current_token()[1]
            self.next_token()
            return {"type": "keyword", "value": keyword}
        else:
            return self.qualifiedName()

    def qualifiedName(self):
        """
        qualifiedName
            : identifier (DOT identifier)*
        """
        identifiers = [self.identifier()]
        
        while self.current_token() and self.current_token()[0] == self.lexer.DOT:
            self.next_token()
            identifiers.append(self.identifier())
        
        return {"type": "qualifiedName", "identifiers": identifiers}

    def temporalClause(self):
        """
        temporalClause
            : FOR? (SYSTEM_VERSION | VERSION) AS OF version
            | FOR? (SYSTEM_TIME | TIMESTAMP) AS OF timestamp=valueExpression
        """
        if self.check_keyword("FOR"):
            self.next_token()
        
        temporal_type = None
        if self.check_keyword("SYSTEM_VERSION"):
            temporal_type = "SYSTEM_VERSION"
            self.next_token()
        elif self.check_keyword("VERSION"):
            temporal_type = "VERSION"
            self.next_token()
        elif self.check_keyword("SYSTEM_TIME"):
            temporal_type = "SYSTEM_TIME"
            self.next_token()
        elif self.check_keyword("TIMESTAMP"):
            temporal_type = "TIMESTAMP"
            self.next_token()
        else:
            raise SyntaxError(f"Expected SYSTEM_VERSION, VERSION, SYSTEM_TIME, or TIMESTAMP, got {self.current_token()[1] if self.current_token() else 'EOF'}")
        
        self.match_keyword("AS")
        self.match_keyword("OF")
        
        value = None
        if temporal_type in ["SYSTEM_VERSION", "VERSION"]:
            value = self.version()
        else:  # SYSTEM_TIME or TIMESTAMP
            value = self.valueExpression()
        
        return {
            "type": "temporalClause",
            "temporalType": temporal_type,
            "value": value
        }

    def version(self):
        """
        version
            : INTEGER_VALUE
            | stringLit
        """
        if self.current_token() and self.current_token()[0] == self.lexer.INTEGER_VALUE:
            value = self.current_token()[1]
            self.next_token()
            return {"type": "integerVersion", "value": value}
        else:
            return {"type": "stringVersion", "value": self.stringLit()}

    def sample(self):
        """
        sample
            : TABLESAMPLE LEFT_PAREN sampleMethod? RIGHT_PAREN (REPEATABLE LEFT_PAREN seed=INTEGER_VALUE RIGHT_PAREN)?
        """
        self.match_keyword("TABLESAMPLE")
        self.expect(self.lexer.LEFT_PAREN)
        
        method = None
        if not self.check_token(self.lexer.RIGHT_PAREN):
            method = self.sampleMethod()
        
        self.expect(self.lexer.RIGHT_PAREN)
        
        seed = None
        if self.check_keyword("REPEATABLE"):
            self.next_token()
            self.expect(self.lexer.LEFT_PAREN)
            
            if self.current_token() and self.current_token()[0] == self.lexer.INTEGER_VALUE:
                seed = self.current_token()[1]
                self.next_token()
            else:
                raise SyntaxError(f"Expected INTEGER_VALUE, got {self.current_token()[1] if self.current_token() else 'EOF'}")
            
            self.expect(self.lexer.RIGHT_PAREN)
        
        return {
            "type": "sample",
            "method": method,
            "seed": seed
        }

    def sampleMethod(self):
        """
        sampleMethod
            : negativeSign=MINUS? percentage=(INTEGER_VALUE | DECIMAL_VALUE) PERCENTLIT   #sampleByPercentile
            | expression ROWS                                                             #sampleByRows
            | sampleType=BUCKET numerator=INTEGER_VALUE OUT OF denominator=INTEGER_VALUE
                (ON (identifier | qualifiedName LEFT_PAREN RIGHT_PAREN))?                 #sampleByBucket
            | bytes=expression                                                            #sampleByBytes
        """
        # Check for sample by percentile
        if self.check_token(self.lexer.MINUS) or self.current_token()[0] in [self.lexer.INTEGER_VALUE, self.lexer.DECIMAL_VALUE]:
            negative_sign = False
            if self.check_token(self.lexer.MINUS):
                negative_sign = True
                self.next_token()
            
            if self.current_token()[0] not in [self.lexer.INTEGER_VALUE, self.lexer.DECIMAL_VALUE]:
                raise SyntaxError(f"Expected INTEGER_VALUE or DECIMAL_VALUE, got {self.current_token()[1] if self.current_token() else 'EOF'}")
            
            percentage = self.current_token()[1]
            percentage_type = self.current_token()[0]
            self.next_token()
            
            if not self.check_keyword("PERCENT"):
                raise SyntaxError(f"Expected PERCENT, got {self.current_token()[1] if self.current_token() else 'EOF'}")
            self.next_token()
            
            return {
                "type": "sampleByPercentile",
                "negativeSign": negative_sign,
                "percentage": percentage,
                "percentageType": percentage_type
            }
        
        # Check for sample by bucket
        if self.check_keyword("BUCKET"):
            self.next_token()
            
            if self.current_token()[0] != self.lexer.INTEGER_VALUE:
                raise SyntaxError(f"Expected INTEGER_VALUE, got {self.current_token()[1] if self.current_token() else 'EOF'}")
            
            numerator = self.current_token()[1]
            self.next_token()
            
            self.match_keyword("OUT")
            self.match_keyword("OF")
            
            if self.current_token()[0] != self.lexer.INTEGER_VALUE:
                raise SyntaxError(f"Expected INTEGER_VALUE, got {self.current_token()[1] if self.current_token() else 'EOF'}")
            
            denominator = self.current_token()[1]
            self.next_token()
            
            on_expression = None
            if self.check_keyword("ON"):
                self.next_token()
                
                if self.peek_token() and self.peek_token()[0] == self.lexer.LEFT_PAREN:
                    qualified_name = self.qualifiedName()
                    self.expect(self.lexer.LEFT_PAREN)
                    self.expect(self.lexer.RIGHT_PAREN)
                    on_expression = {"type": "functionCall", "qualifiedName": qualified_name}
                else:
                    on_expression = {"type": "identifier", "identifier": self.identifier()}
            
            return {
                "type": "sampleByBucket",
                "numerator": numerator,
                "denominator": denominator,
                "onExpression": on_expression
            }
        
        # Check for sample by rows
        saved_index = self.current_token_index
        try:
            expr = self.expression()
            if self.check_keyword("ROWS"):
                self.next_token()
                return {
                    "type": "sampleByRows",
                    "expression": expr
                }
            else:
                # Rollback and treat as sample by bytes
                self.current_token_index = saved_index
            
        except Exception:
            # Rollback on any error
            self.current_token_index = saved_index
        
        # Default to sample by bytes
        return {
            "type": "sampleByBytes",
            "expression": self.expression()
        }


    def expressionSeq(self):
        """
        expressionSeq
            : expression (COMMA expression)*
        """
        expressions = [self.expression()]
        
        while self.current_token() and self.current_token()[0] == self.lexer.COMMA:
            self.next_token()
            expressions.append(self.expression())
        
        return expressions
        

    def querySpecification(self):
        """
        querySpecification
            : transformClause
            fromClause?
            lateralView*
            whereClause?
            aggregationClause?
            havingClause?
            windowClause?                                                         #transformQuerySpecification
            | selectClause
            fromClause?
            lateralView*
            whereClause?
            aggregationClause?
            havingClause?
            windowClause?                                                         #regularQuerySpecification
        """
        if self.check_keyword("SELECT"):
            select_clause = self.selectClause()
            
            from_clause = None
            if self.check_keyword("FROM"):
                from_clause = self.fromClause()
            
            lateral_views = []
            while self.check_keyword("LATERAL") and self.peek_token() and self.check_keyword("VIEW", self.peek_token()[1]):
                lateral_views.append(self.lateralView())
            
            where_clause = None
            if self.check_keyword("WHERE"):
                where_clause = self.whereClause()
            
            aggregation_clause = None
            if self.check_keyword("GROUP"):
                aggregation_clause = self.aggregationClause()
            
            having_clause = None
            if self.check_keyword("HAVING"):
                having_clause = self.havingClause()
            
            window_clause = None
            if self.check_keyword("WINDOW"):
                window_clause = self.windowClause()
            
            return {
                "type": "regularQuerySpecification",
                "selectClause": select_clause,
                "fromClause": from_clause,
                "lateralViews": lateral_views,
                "whereClause": where_clause,
                "aggregationClause": aggregation_clause,
                "havingClause": having_clause,
                "windowClause": window_clause
            }
        elif self.check_keyword("MAP") or self.check_keyword("REDUCE") or self.check_keyword("TRANSFORM"):
            transform_clause = self.transformClause()
            
            from_clause = None
            if self.check_keyword("FROM"):
                from_clause = self.fromClause()
            
            lateral_views = []
            while self.check_keyword("LATERAL") and self.peek_token() and self.check_keyword("VIEW", self.peek_token()[1]):
                lateral_views.append(self.lateralView())
            
            where_clause = None
            if self.check_keyword("WHERE"):
                where_clause = self.whereClause()
            
            aggregation_clause = None
            if self.check_keyword("GROUP"):
                aggregation_clause = self.aggregationClause()
            
            having_clause = None
            if self.check_keyword("HAVING"):
                having_clause = self.havingClause()
            
            window_clause = None
            if self.check_keyword("WINDOW"):
                window_clause = self.windowClause()
            
            return {
                "type": "transformQuerySpecification",
                "transformClause": transform_clause,
                "fromClause": from_clause,
                "lateralViews": lateral_views,
                "whereClause": where_clause,
                "aggregationClause": aggregation_clause,
                "havingClause": having_clause,
                "windowClause": window_clause
            }
        else:
            raise SyntaxError(f"Expected SELECT, MAP, REDUCE, or TRANSFORM, got {self.current_token()[1] if self.current_token() else 'EOF'}")
        

if __name__ == "__main__":
    # Example usage of the parser with a simple SQL query
    from SparkLexer import SqlBaseLexer
    
    sql = "SELECT id, name FROM users WHERE age > 18 ORDER BY name"
    lexer = SqlBaseLexer(sql)
    
    parser = SqlBaseParser(lexer)
    
    try:
        result = parser.parse()
        print("Parsing successful!")
        print(result)
    except Exception as e:
        print(f"Parsing error: {e}")
    