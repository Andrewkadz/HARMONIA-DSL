from phi_pi_e_interpreter import PhiPiEInterpreter

def test_interpreter():
    interpreter = PhiPiEInterpreter()
    
    print("\n=== Testing Basic Symbol Operations ===")
    # Test stabilization
    result = interpreter.stabilize(5)
    print(f"Stabilize test: {result}")
    
    # Test fusion
    result = interpreter.fuse([2, 3, 5])
    print(f"Fusion test: {result}")
    
    # Test pulse
    result = interpreter.pulse("test field")
    print(f"Pulse test: {result}")
    
    print("\n=== Testing Very Basic Fields ===")
    # Test simplest field
    simple_field = "Θ"
    print(f"\nTesting simplest field: {simple_field}")
    try:
        result = interpreter.parse_field(simple_field)
        print(f"Parsed result: {result}")
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        print("\nDetailed error:")
        traceback.print_exc()
    
    # Test field identifier
    id_field = "Θ₀"
    print(f"\nTesting field identifier: {id_field}")
    try:
        result = interpreter.parse_field(id_field)
        print(f"Parsed result: {result}")
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        print("\nDetailed error:")
        traceback.print_exc()
    
    # Test field with value
    value_field = "Θ₀:5"
    print(f"\nTesting field with value: {value_field}")
    try:
        result = interpreter.parse_field(value_field)
        print(f"Parsed result: {result}")
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        print("\nDetailed error:")
        traceback.print_exc()

    print("\n=== Testing New Methods ===")
    # Test loop
    loop_result = interpreter.loop([1, 2, 3])
    print(f"Loop test: {loop_result}")
    
    # Test stabilize with complex values
    complex_a = {"a": 1, "b": 2}
    complex_b = {"a": 1, "b": 2}
    stabilize_result = interpreter.stabilize(complex_a, complex_b)
    print(f"Stabilize complex test: {stabilize_result}")
    
    # Test get_tension_strength
    context = interpreter.FieldContext()
    tension_result = interpreter.get_tension_strength(complex_a, context)
    print(f"Tension strength test: {tension_result}")
    
    # Test simultaneity
    simultaneity_result = interpreter.simultaneity(["field1", "field2"])
    print(f"Simultaneity test: {simultaneity_result}")
    
    # Test equivalence
    eq_result = interpreter.equivalence(5, 5)
    print(f"Equivalence test: {eq_result}")
    
    # Test parse_field with complex expressions
    complex_field = "(Θ₀:5 + Θ₁:3)"
    print(f"\nTesting complex field: {complex_field}")
    try:
        result = interpreter.parse_field(complex_field)
        print(f"Parsed result: {result}")
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        print("\nDetailed error:")
        traceback.print_exc()
    
    # Test field with symbol
    symbol_field = "Θ₀:Ψ"
    print(f"\nTesting field with symbol: {symbol_field}")
    try:
        result = interpreter.parse_field(symbol_field)
        print(f"Parsed result: {result}")
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        print("\nDetailed error:")
        traceback.print_exc()
    
    print("\n=== Testing Runtime File ===")
    # Try to execute the OS Runtime file
    try:
        # Get the correct path to the runtime file
        import os
        runtime_path = os.path.join(os.path.expanduser("~"), "Downloads", "Φπε OS Runtime.hrm")
        print(f"\nUsing runtime path: {runtime_path}")
        
        with open(runtime_path, "r", encoding="utf-8") as f:
            runtime_code = f.read()
            print("\n=== Runtime Code ===")
            print(runtime_code)
            
            print("\n=== Execution Results ===")
            results = interpreter.execute(runtime_code)
            for i, result in enumerate(results):
                print(f"\nField {i+1} result:")
                print(result)
    except Exception as e:
        print(f"\nError executing runtime: {str(e)}")
        print(f"Details: {str(e)}")
        import traceback
        print("\nDetailed error:")
        traceback.print_exc()

if __name__ == "__main__":
    test_interpreter()
