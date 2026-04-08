TASKS = {
    "easy": {
        "code": """def greet():
    print("Hello World)""",
        "language": "python",
        "expected": {
            "issue": "syntax_error",
            "impact": "code will not run",
            "fix": "close the string properly"
        }
    },

    "medium": {
        "code": """def authenticate(user_input, password):
    query = "SELECT * FROM users WHERE name = '" + user_input + "'"
    return execute(query)""",
        "language": "python",
        "expected": {
            "issue": "security_vulnerability",
            "impact": "sql injection risk",
            "fix": "use parameterized queries"
        }
    },

    "hard": {
        "code": """def process_data(arr):
    result = []
    for i in range(len(arr)):
        result.append(arr[i] * 2)
    return result""",
        "language": "python",
        "expected": {
            "issue": "inefficient_code",
            "impact": "unnecessary indexing overhead",
            "fix": "use list comprehension"
        }
    }
}