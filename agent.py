import json
from openai import OpenAI
from rich.console import Console
from config import settings
from schemas import PromptRequest, CodingAgentResponse
from tools import AGENT_TOOLS, TOOL_MAP

client = OpenAI(api_key=settings.openai_api_key)
console = Console()

SYSTEM_PROMPT = """You are DevPilot, an autonomous senior AI coding assistant running in a developer's terminal.
You have access to file system tools (list_directory, read_file, write_file).
- When asked to inspect, debug, or create files, use your tools proactively.
- Always write clean, modular, well-commented code.
- Once tools are complete, provide your final structured response."""

def run_coding_agent(request: PromptRequest) -> CodingAgentResponse:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Working Directory: {request.working_dir}\nTask: {request.prompt}"},
    ]

    for _ in range(6):
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
            tools=AGENT_TOOLS,
            tool_choice="auto",
        )

        assistant_msg = response.choices[0].message

        if not assistant_msg.tool_calls:
            break

        messages.append(assistant_msg)

        for tool_call in assistant_msg.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)

            console.print(f"[bold cyan]⚡ Agent calling tool:[/bold cyan] [yellow]{func_name}({func_args})[/yellow]")

            tool_fn = TOOL_MAP.get(func_name)
            if tool_fn:
                tool_output = tool_fn(**func_args)
            else:
                tool_output = f"Error: Tool '{func_name}' not found."

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(tool_output),
                }
            )

    structured_completion = client.beta.chat.completions.parse(
        model=settings.openai_model,
        messages=messages,
        response_format=CodingAgentResponse,
    )

    return structured_completion.choices[0].message.parsed