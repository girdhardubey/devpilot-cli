from pydantic import BaseModel, Field
from typing import List

# 1. Validates what YOU type into the CLI
class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=3, description="The coding task requested by the user")
    working_dir: str = Field(default=".", description="Target directory for file operations")

# 2. Tracks any file the AI reads, creates, or edits
class FileActionReport(BaseModel):
    file_path: str = Field(..., description="Path of the file that was read, created, or modified")
    action_taken: str = Field(..., description="e.g., created, modified, read")
    summary: str = Field(..., description="Short summary of changes in this file")

# 3. Forces the OpenAI Agent to reply in this exact format
class CodingAgentResponse(BaseModel):
    explanation: str = Field(..., description="Clear technical explanation of the solution")
    code_snippet: str = Field(..., description="The primary code block or command for the user")
    language: str = Field(..., description="Programming language for syntax highlighting, e.g., python, bash, sql")
    files_touched: List[FileActionReport] = Field(default_factory=list, description="List of files modified or inspected")
    next_steps: List[str] = Field(default_factory=list, description="Commands or steps the user should run next")