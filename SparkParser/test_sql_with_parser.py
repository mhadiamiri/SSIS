# ----------------------------- SQLGLOT -----------------------------
# import sqlglot

# def test_sql_queries():
#     valid_queries = [
#         "SELECT * FROM table_name",
#         "SELECT col1, col2 FROM my_table WHERE col3 > 100",
#         "SELECT col1, SUM(col2) FROM sales GROUP BY col1",
#         "SELECT * FROM employees ORDER BY name ASC",
#         "SELECT DISTINCT col1 FROM customers"
#     ]

#     invalid_queries = [
#         "SELECT TOP 5 * FROM employees;",
#         "DECLARE @myVar INT = 10; SELECT @myVar;",
#         "SELECT IIF(1 = 1, 'Yes', 'No') AS Result;",
#         "SELECT * INTO new_table FROM old_table;",
#         "SELECT * FROM customers WITH (NOLOCK);"
#     ]

#     print("Testing Valid Queries:")
#     for query in valid_queries:
#         try:
#             sqlglot.parse_one(query, dialect="spark") # , identity=True )
#             print(f"✅ Valid: {query}")
#         except Exception as e:
#             print(f"❌ Failed (Should be valid): {query} - Error: {e}")

#     print("\nTesting Invalid Queries:")
#     for query in invalid_queries:
#         try:
#             sqlglot.parse_one(query, dialect="spark") # , identity=True )
#             print(f"❌ Failed (Should be invalid): {query} - No error detected")
#         except Exception as e:
#             print(f"✅ Correctly Identified Invalid: {query} - Error: {e}")

# if __name__ == "__main__":
#     test_sql_queries()


# ----------------------------- PYSPARK -----------------------------
# from pyspark.sql import SparkSession
# from pyspark.sql.utils import AnalysisException

# def validate_spark_sql_query(query):
#     # Initialize a local SparkSession
#     spark = SparkSession.builder \
#         .appName("SQLValidator") \
#         .master("local[*]") \
#         .getOrCreate()
    
#     try:
#         # Attempt to parse the query by running explain()
#         spark.sql(query).explain()
#         return True, "Query is syntactically correct"
#     except AnalysisException as e:
#         return False, f"Syntax error: {str(e)}"
#     finally:
#         spark.stop()

# # Example usage
# if __name__ == "__main__":
#     # Test queries
#     valid_query = "SELECT * FROM my_table WHERE id > 10"
#     invalid_query = "SELECT * FROM WHERE id >"  # Intentionally broken

#     # Validate queries
#     is_valid, message = validate_spark_sql_query(valid_query)
#     print(f"Valid query: {is_valid} - {message}")
    
#     is_valid, message = validate_spark_sql_query(invalid_query)
#     print(f"Invalid query: {is_valid} - {message}")

# from pysparkdt import SparkDT
# from pyspark.sql import SparkSession

# # Initialize a Spark session with pysparkdt
# sparkdt = SparkDT()
# spark = sparkdt.spark

# # Create a temporary table
# data = [(1, "Alice"), (2, "Bob"), (3, "Charlie")]
# columns = ["id", "name"]
# df = spark.createDataFrame(data, columns)
# df.createOrReplaceTempView("people")

# # Define a Spark SQL query
# sql_query = "SELECT * FROM people WHERE id = 2"

# try:
#     # Execute the SQL query
#     result = spark.sql(sql_query)
#     result.show()
# except Exception as e:
#     print(f"Syntax Error: {e}")

# # Stop the Spark session
# spark.stop()

import subprocess
import os

def windows_to_linux_path(path):
    path = path.replace("\\", "/")
    if ":" in path:
        drive, rest = path.split(":", 1)
        return f"/mnt/{drive.lower()}{rest}"
    return path


def check_spark_sql_syntax(sql_query):
    """
    Runs a shell script that checks Spark SQL syntax and returns the output.
    
    :param sql_query: The SQL query to check
    :return: Tuple of (is_valid: bool, message: str)
    """
    try:
        absolute_path = os.path.abspath("Spark_Container/run-spark-sql.sh")
        if os.name=='nt':
            absolute_path = windows_to_linux_path(absolute_path)

        # Command to run the .sh script, passing the SQL query as an argument
        command = ["bash", absolute_path, sql_query]

        # Execute the shell script
        result = subprocess.run(command, capture_output=True, text=True)

        # Get output and error
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        marker = "[PARSE_SYNTAX_ERROR]"
        if marker in stdout:
            result_text = f"{marker}\n{stdout.split(marker, 1)[1].strip()}"
            return False, result_text
        
        elif "[TABLE_OR_VIEW_NOT_FOUND]" in stdout:
            return True, stdout
        
        elif stderr:
            return False, stderr
        
        else:
            if result.returncode == 0:
                return True, stdout or "Query validated successfully."
            else:
                return False, stdout or stderr or "Unknown validation error."

    except Exception as e:
        return False, f"Exception while running shell script: {str(e)}"



if __name__ == "__main__":
    # Valid SparkSQL queries that should pass
    valid_queries = [
        # 1. Complex SELECT with multiple JOINs and window functions
        """
        SELECT 
            a.customer_id, 
            b.product_name,
            SUM(a.quantity) AS total_quantity,
            AVG(a.price) AS avg_price,
            RANK() OVER (PARTITION BY a.customer_id ORDER BY SUM(a.quantity) DESC) as product_rank
        FROM orders a
        JOIN products b ON a.product_id = b.id
        LEFT JOIN customers c ON a.customer_id = c.id
        WHERE a.order_date BETWEEN '2023-01-01' AND '2023-12-31'
        AND c.country IN ('US', 'CA', 'MX')
        GROUP BY a.customer_id, b.product_name
        HAVING SUM(a.quantity) > 10
        ORDER BY a.customer_id, product_rank
        LIMIT 100
        """,
        
        # 2. CTE with UNION ALL
        """
        WITH revenue_data AS (
            SELECT region, product, SUM(amount) as total
            FROM sales
            WHERE year = 2023
            GROUP BY region, product
        ),
        prev_year_data AS (
            SELECT region, product, SUM(amount) as total
            FROM sales
            WHERE year = 2022
            GROUP BY region, product
        )
        SELECT 
            COALESCE(r.region, p.region) as region,
            COALESCE(r.product, p.product) as product,
            r.total as current_year,
            p.total as previous_year,
            (r.total - p.total) as growth
        FROM revenue_data r
        FULL OUTER JOIN prev_year_data p 
        ON r.region = p.region AND r.product = p.product
        ORDER BY region, product
        """,
        
        # 3. Complex aggregation with CUBE
        """
        SELECT 
            COALESCE(region, 'All Regions') as region,
            COALESCE(category, 'All Categories') as category,
            COALESCE(product, 'All Products') as product,
            SUM(sales) as total_sales,
            COUNT(DISTINCT customer_id) as customer_count
        FROM sales_data
        WHERE year = 2023
        GROUP BY CUBE(region, category, product)
        HAVING SUM(sales) > 1000
        ORDER BY region, category, product
        """,
        
        # 4. Nested subqueries with EXISTS
        """
        SELECT 
            product_id, 
            product_name,
            price
        FROM products p
        WHERE EXISTS (
            SELECT 1 
            FROM orders o
            WHERE o.product_id = p.product_id
            AND o.order_date >= date_add(current_date(), -90)
            AND o.quantity > 5
        )
        AND NOT EXISTS (
            SELECT 1
            FROM inventory i
            WHERE i.product_id = p.product_id
            AND i.stock_quantity < 10
        )
        """,
        
        # 5. CASE expressions and date functions
        """
        SELECT
            user_id,
            CASE 
                WHEN datediff(current_date(), last_login_date) <= 7 THEN 'Active'
                WHEN datediff(current_date(), last_login_date) <= 30 THEN 'Recent'
                WHEN datediff(current_date(), last_login_date) <= 90 THEN 'Inactive'
                ELSE 'Dormant'
            END as user_status,
            COUNT(*) as login_count,
            MIN(login_date) as first_login,
            MAX(login_date) as last_login,
            date_format(MAX(login_date), 'yyyy-MM') as last_login_month
        FROM user_logins
        WHERE login_date >= add_months(current_date(), -12)
        GROUP BY 
            user_id,
            CASE 
                WHEN datediff(current_date(), last_login_date) <= 7 THEN 'Active'
                WHEN datediff(current_date(), last_login_date) <= 30 THEN 'Recent'
                WHEN datediff(current_date(), last_login_date) <= 90 THEN 'Inactive'
                ELSE 'Dormant'
            END
        """,
        
        # 6. Multiple CTEs and window functions
        """
        WITH monthly_sales AS (
            SELECT 
                date_format(order_date, 'yyyy-MM') as month,
                product_id,
                SUM(quantity * price) as revenue
            FROM orders
            WHERE order_date >= '2022-01-01'
            GROUP BY date_format(order_date, 'yyyy-MM'), product_id
        ),
        ranked_products AS (
            SELECT
                month,
                product_id,
                revenue,
                RANK() OVER (PARTITION BY month ORDER BY revenue DESC) as rank
            FROM monthly_sales
        )
        SELECT
            r.month,
            r.product_id,
            p.product_name,
            r.revenue,
            r.rank,
            ROUND(r.revenue / SUM(r.revenue) OVER (PARTITION BY r.month) * 100, 2) as revenue_percentage
        FROM ranked_products r
        JOIN products p ON r.product_id = p.product_id
        WHERE r.rank <= 5
        ORDER BY r.month, r.rank
        """,
        
        # 7. PIVOT operation
        """
        SELECT * 
        FROM (
            SELECT 
                product_category,
                quarter,
                sales_amount
            FROM quarterly_sales
            WHERE year = 2023
        )
        PIVOT (
            SUM(sales_amount)
            FOR quarter IN ('Q1', 'Q2', 'Q3', 'Q4')
        )
        """,
        
        # 8. Complex JOIN with array and struct operations
        """
        SELECT 
            u.user_id,
            u.name,
            e.event_type,
            e.event_time,
            explode(e.properties) as property
        FROM users u
        JOIN events e ON u.user_id = e.user_id
        LATERAL VIEW explode(u.interests) interests_view AS interest
        WHERE e.event_date >= '2023-01-01'
        AND array_contains(u.interests, 'data science')
        AND e.properties['device_type'] = 'mobile'
        """,
        
        # 9. Using TRANSFORM, FILTER, arrays, and maps
        """
        SELECT
            customer_id,
            transform(
                filter(purchases, p -> p.amount > 100),
                p -> struct(p.product_id, p.amount, p.purchase_date)
            ) as large_purchases,
            map_keys(attributes) as attribute_keys,
            map_values(attributes) as attribute_values,
            array_sort(array_distinct(collect_list(category))) as unique_categories
        FROM customer_data
        GROUP BY customer_id, attributes
        HAVING size(
            filter(purchases, p -> p.amount > 1000)
        ) > 0
        """,
        
        # 10. WITH RECURSIVE (added in Spark 3.1)
        """
        WITH RECURSIVE employee_hierarchy AS (
            SELECT id, name, manager_id, 1 as level
            FROM employees
            WHERE manager_id IS NULL
            
            UNION ALL
            
            SELECT e.id, e.name, e.manager_id, eh.level + 1
            FROM employees e
            JOIN employee_hierarchy eh ON e.manager_id = eh.id
        )
        SELECT * FROM employee_hierarchy
        ORDER BY level, id
        """
    ]

    # Invalid SparkSQL queries that should fail the syntax check
    invalid_queries = [
        # 1. T-SQL's OUTPUT clause (not supported in SparkSQL)
        """
        INSERT INTO target_table (col1, col2, col3)
        OUTPUT inserted.id, inserted.col1, inserted.col2 INTO audit_table
        SELECT col1, col2, col3 FROM source_table
        WHERE col1 > 100
        """,
        
        # 2. T-SQL's TOP with PERCENT (SparkSQL uses LIMIT instead)
        """
        SELECT TOP 10 PERCENT
            customer_id,
            SUM(order_total) as total_spend
        FROM orders
        GROUP BY customer_id
        ORDER BY total_spend DESC
        """,
        
        # 3. T-SQL's CROSS APPLY (SparkSQL uses LATERAL instead)
        """
        SELECT 
            c.customer_id,
            c.customer_name,
            o.order_id,
            o.order_date
        FROM customers c
        CROSS APPLY (
            SELECT TOP 3 order_id, order_date
            FROM orders
            WHERE customer_id = c.customer_id
            ORDER BY order_date DESC
        ) o
        """,
        
        # 4. T-SQL's MERGE statement (different syntax in SparkSQL)
        """
        MERGE INTO target_table AS t
        USING source_table AS s
        ON t.id = s.id
        WHEN MATCHED AND s.value > 100 THEN
            UPDATE SET t.col1 = s.col1, t.col2 = s.col2
        WHEN MATCHED AND s.value <= 100 THEN
            DELETE
        WHEN NOT MATCHED THEN
            INSERT (id, col1, col2) VALUES (s.id, s.col1, s.col2)
        """,
        
        # 5. T-SQL's STRING_AGG function (SparkSQL uses CONCAT_WS with COLLECT_LIST)
        """
        SELECT
            category,
            STRING_AGG(product_name, ', ') WITHIN GROUP (ORDER BY product_name) as product_list
        FROM products
        GROUP BY category
        """,
        
        # 6. T-SQL's OFFSET-FETCH (SparkSQL uses LIMIT with OFFSET)
        """
        SELECT
            product_id,
            product_name,
            price
        FROM products
        ORDER BY price DESC
        OFFSET 10 ROWS
        FETCH NEXT 10 ROWS ONLY
        """,
        
        # 7. T-SQL's ISNULL function (SparkSQL uses COALESCE or IFNULL)
        """
        SELECT
            order_id,
            ISNULL(discount, 0) as effective_discount,
            order_total - ISNULL(discount, 0) as final_amount
        FROM orders
        """,
        
        # 8. T-SQL's PIVOT with dynamic columns
        """
        DECLARE @cols NVARCHAR(MAX);
        SET @cols = (SELECT STRING_AGG(QUOTENAME(quarter), ',')
                    FROM (SELECT DISTINCT quarter FROM quarterly_sales) as quarters);
        
        EXEC('SELECT * FROM quarterly_sales
            PIVOT (SUM(sales_amount) FOR quarter IN (' + @cols + ')) AS pvt');
        """,
        
        # 9. T-SQL's Common Table Expression with RECURSIVE keyword in wrong position
        """
        WITH employee_hierarchy RECURSIVE AS (
            SELECT id, name, manager_id, 1 as level
            FROM employees
            WHERE manager_id IS NULL
            
            UNION ALL
            
            SELECT e.id, e.name, e.manager_id, eh.level + 1
            FROM employees e
            JOIN employee_hierarchy eh ON e.manager_id = eh.id
        )
        SELECT * FROM employee_hierarchy
        ORDER BY level, id
        """,
        
        # 10. T-SQL's TRY_CONVERT function (SparkSQL uses CAST with exception handling)
        """
        SELECT
            order_id,
            TRY_CONVERT(DECIMAL(10,2), price_string) as price,
            order_date
        FROM raw_orders
        WHERE TRY_CONVERT(DATE, order_date_string) >= '2023-01-01'
        """
    ]


    
    print("Testing valid queries:")
    for i, query in enumerate(valid_queries, 1):
        is_valid, message = check_spark_sql_syntax(query)
        print(f"Query {i}: {'✓ Valid' if is_valid else '✗ Invalid'} - {message}")
    
    print("\nTesting invalid queries:")
    for i, query in enumerate(invalid_queries, 1):
        is_valid, message = check_spark_sql_syntax(query)
        print(f"Query {i}: {'✓ Valid' if is_valid else '✗ Invalid'} - {message}")
