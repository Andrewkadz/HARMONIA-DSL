from phi_pi_e_interpreter import PhiPiEInterpreter

def test_interpreter():
    # Create an instance of the interpreter
    interpreter = PhiPiEInterpreter()
    
    # Test cases
    test_cases = [
        # Simple symbol
        ("Φ", "Simple symbol"),
        # Symbol with numeric subscript
        ("Θ₀", "Symbol with numeric subscript"),
        # Symbol with numeric subscript and value
        ("Θ₀:5", "Symbol with numeric subscript and value"),
        # Field identifier with value
        ("field:Φ", "Field identifier with symbol"),
        # Nested expression
        ("(Φ)", "Nested expression"),
        # Multiple fields
        ("ΦΤΘ₀Τfield:Φ", "Multiple fields"),
        # Invalid cases
        ("invalid_symbol", "Invalid symbol"),
        ("Θ_abc", "Invalid subscript"),
        ("field:invalid", "Invalid field value"),
        # More complex cases
        ("Θ₀ΤΘ₁ΤΘ₂", "Multiple subscripted symbols"),
        ("field:Θ₀Τanother:Θ₁", "Multiple fields with subscripts"),
        ("(Θ₀ΤΘ₁)", "Nested expression with subscripts")
    ]

    # Run tests
    print("\nRunning Φπε Interpreter Tests\n")
    for i, (test, description) in enumerate(test_cases, 1):
        print(f"\nTest {i}: {description}")
        print(f"Input: {test}")
        try:
            print("\nCleaning input...")
            cleaned = interpreter.clean_input(test)
            print(f"Cleaned: {cleaned}")
            
            print("\nSplitting fields...")
            fields = interpreter.split_fields(cleaned)
            print(f"Fields: {fields}")
            
            print("\nExecuting...")
            result = interpreter.execute(test)
            print(f"\nResult: {result}")
        except Exception as e:
            print(f"\nError: {str(e)}")
            import traceback
            print("\nTraceback:")
            traceback.print_exc()

if __name__ == "__main__":
    test_interpreter()
