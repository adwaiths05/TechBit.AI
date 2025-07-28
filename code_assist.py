import asyncio
from transformers import pipeline

# Initialize CodeLlama for code generation and explanation
llm = pipeline("text-generation", model="codellama/CodeLlama-13b-hf", token="YOUR_HF_TOKEN")

# Generate code based on user prompt
def generate_code(prompt):
    result = llm(prompt, max_length=200, num_return_sequences=1)
    return result[0]["generated_text"]

# Execute code (mocked sandbox, replace with Pyodide for browser execution)
async def execute_code(code, expected_output):
    try:
        # Mock execution using exec() for demo (use Pyodide in production)
        local_vars = {}
        exec(code, {}, local_vars)
        result = local_vars.get("result", None)
        return str(result) == str(expected_output), result
    except Exception as e:
        return False, str(e)

# Iteratively refine code until correct output
async def refine_code(prompt, expected_output, max_attempts=3):
    attempt = 0
    code = generate_code(prompt)
    while attempt < max_attempts:
        success, output = await execute_code(code, expected_output)
        if success:
            return code, output
        prompt += f"\nPrevious code failed with output: {output}. Fix it."
        code = generate_code(prompt)
        attempt += 1
    return code, output

# Main function for the coding agent
async def main(prompt, expected_output):
    # Generate and refine code
    code, output = await refine_code(prompt, expected_output)
    print(f"Code:\n{code}\nOutput: {output}")

    # Ask for explanation
    user_wants_explanation = input("Want an explanation? (yes/no): ").lower() == "yes"
    if user_wants_explanation:
        explanation = llm(f"Explain this code:\n{code}", max_length=200)[0]["generated_text"]
        print(f"Explanation:\n{explanation}")

# Run with Pyodide compatibility
if platform.system() == "Emscripten":
    asyncio.ensure_future(main("Write a Python function to reverse a string", "dlrow"))
else:
    if __name__ == "__main__":
        asyncio.run(main("Write a Python function to reverse a string", "dlrow"))
