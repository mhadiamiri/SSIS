from SparkLexer import SqlBaseLexer
from SparkParser2 import SqlBaseParser

def test_query(sql, expect_success=True):
    print(f"\nTesting query: {sql}")
    try:
        lexer = SqlBaseLexer(sql)
        parser = SqlBaseParser(lexer)
        result = parser.parse()
        if expect_success:
            print(f"✅ SUCCESS: Query parsed correctly")
            # Print just the type of the root result to avoid overwhelming output
            print(f"   Result type: {result.get('type', 'unknown')}")
            return True
        else:
            print(f"❓ UNEXPECTED SUCCESS: Query parsed but should have failed")
            return False
    except Exception as e:
        if expect_success:
            print(f"❌ UNEXPECTED ERROR: {e}")
            return False
        else:
            print(f"✅ EXPECTED ERROR: {e}")
            return True

# Correct queries
correct_queries = [
    # Simple SELECT query
    "SELECT id, name, age FROM users WHERE age > 21 ORDER BY name;",
    
    # Query with JOIN
    "SELECT u.id, u.name, o.order_date FROM users u JOIN orders o ON u.id = o.user_id;",
    
    # Query with GROUP BY
    "SELECT department, COUNT(*) FROM employees GROUP BY department;",
    
    # Query with subquery
    "SELECT * FROM (SELECT id, name FROM users) AS active_users;",
    
    # Query with ORDER BY and LIMIT
    "SELECT id, name FROM employees ORDER BY name LIMIT 10;"
]

# Erroneous queries
erroneous_queries = [
    # Missing FROM clause in a SELECT statement
    "SELECT id, name;",
    
    # Mismatched parentheses
    "SELECT * FROM (SELECT * FROM users WHERE id = 1;",
    
    # Invalid syntax - clauses in wrong order
    "SELECT * FROM users HAVING COUNT(*) > 5 WHERE age > 20;",
    
    # INSERT statement missing required parts
    "INSERT INTO users;",
    
    # Incomplete WHERE clause
    "SELECT * FROM users WHERE"
]

def run_tests():
    print("=== TESTING CORRECT QUERIES ===")
    correct_results = [test_query(query, expect_success=True) for query in correct_queries]
    
    print("\n=== TESTING ERRONEOUS QUERIES ===")
    error_results = [test_query(query, expect_success=False) for query in erroneous_queries]
    
    correct_count = sum(correct_results)
    error_count = sum(error_results)
    
    print(f"\n=== TEST SUMMARY ===")
    print(f"Correct queries: {correct_count}/{len(correct_queries)} passed")
    print(f"Erroneous queries: {error_count}/{len(erroneous_queries)} correctly failed")

if __name__ == "__main__":
    run_tests()