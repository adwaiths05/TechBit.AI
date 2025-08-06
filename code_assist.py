import asyncio
from crewai import Agent, Task, Crew
from transformers import pipeline

class CodingCrew:
    def __init__(self):
        self.llm = pipeline("text-generation", model="codellama/CodeLlama-13b-hf", token="YOUR_HF_TOKEN")

    def generate_code(self, prompt):
        result = self.llm(prompt, max_length=200, num_return_sequences=1)
        return result[0]["generated_text"]

    async def execute_code(self, code, expected_output):
        try:
            local_vars = {}
            exec(code, {}, local_vars)
            result = local_vars.get("result", None)
            return str(result) == str(expected_output), result
        except Exception as e:
            return False, str(e)

    def setup_crew(self, prompt, expected_output):
        coder = Agent(
            role="Code Generator",
            goal="Generate correct Python code for the given prompt",
            backstory="Expert Python developer with debugging skills",
            llm=self.llm
        )

        debugger = Agent(
            role="Code Debugger",
            goal="Fix code to match expected output",
            backstory="Specialist in identifying and resolving code errors",
            llm=self.llm
        )

        explainer = Agent(
            role="Code Explainer",
            goal="Provide clear explanations of code",
            backstory="Technical writer skilled in simplifying complex code",
            llm=self.llm
        )

        code_task = Task(
            description=f"Write a Python function for: {prompt}",
            agent=coder,
            expected_output=expected_output
        )

        debug_task = Task(
            description="Debug and fix code to match expected output",
            agent=debugger,
            expected_output=expected_output
        )

        explain_task = Task(
            description="Explain the final code in simple terms",
            agent=explainer
        )

        return Crew(agents=[coder, debugger, explainer], tasks=[code_task, debug_task, explain_task])

    async def run(self, prompt, expected_output, max_attempts=3):
        crew = self.setup_crew(prompt, expected_output)
        attempt = 0
        code = None
        output = None

        while attempt < max_attempts:
            result = await crew.kickoff_async()
            code = result.tasks_output[0].output
            success, output = await self.execute_code(code, expected_output)
            if success:
                break
            prompt += f"\nPrevious code failed with output: {output}. Fix it."
            crew = self.setup_crew(prompt, expected_output)
            attempt += 1

        print(f"Code:\n{code}\nOutput: {output}")
        user_wants_explanation = input("Want an explanation? (yes/no): ").lower() == "yes"
        if user_wants_explanation:
            explanation = result.tasks_output[2].output
            print(f"Explanation:\n{explanation}")

async def main():
    crew = CodingCrew()
    await crew.run("Write a Python function to reverse a string", "dlrow")

if __name__ == "__main__":
    asyncio.run(main())
