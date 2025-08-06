import asyncio
import gradio as gr
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

    async def run(self, prompt, expected_output, want_explanation):
        crew = self.setup_crew(prompt, expected_output)
        attempt = 0
        code = None
        output = None
        max_attempts = 3

        while attempt < max_attempts:
            result = await crew.kickoff_async()
            code = result.tasks_output[0].output
            success, output = await self.execute_code(code, expected_output)
            if success:
                break
            prompt += f"\nPrevious code failed with output: {output}. Fix it."
            crew = self.setup_crew(prompt, expected_output)
            attempt += 1

        explanation = result.tasks_output[2].output if want_explanation else ""
        return f"**Code:**\n```python\n{code}\n```\n**Output:**\n{output}\n" + (f"**Explanation:**\n{explanation}" if want_explanation else "")

def run_coding_crew(prompt, expected_output, want_explanation):
    crew = CodingCrew()
    return asyncio.run(crew.run(prompt, expected_output, want_explanation))

with gr.Blocks() as demo:
    gr.Markdown("# Coding Crew UI")
    prompt_input = gr.Textbox(label="Enter your coding prompt", placeholder="e.g., Write a Python function to reverse a string")
    expected_output_input = gr.Textbox(label="Expected Output", placeholder="e.g., dlrow")
    explanation_checkbox = gr.Checkbox(label="Want an explanation?", value=False)
    submit_button = gr.Button("Run")
    output = gr.Markdown()

    submit_button.click(
        fn=run_coding_crew,
        inputs=[prompt_input, expected_output_input, explanation_checkbox],
        outputs=output
    )

demo.launch()
