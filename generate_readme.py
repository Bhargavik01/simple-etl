import os
from openai import OpenAI
import subprocess

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Get list of changed files in last commit
result = subprocess.run(
    ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
    capture_output=True, text=True
)
changed_files = result.stdout.strip().split("\n")
print("🔹 Changed files:", changed_files)

# Only proceed if Python files changed
py_files = [f for f in changed_files if f.endswith(".py")]
if not py_files:
    print("ℹ️ No Python files changed. Skipping README suggestion.")
    exit(0)

# Get diff of Python files
diff_result = subprocess.run(
    ["git", "diff", "HEAD~1", "HEAD"] + py_files,
    capture_output=True, text=True
)
diff_text = diff_result.stdout
print("\n🔹 Diff of Python files:\n", diff_text[:500], "...")  # print first 500 chars

# Build GPT prompt
prompt = f"""
You are an assistant that updates README.md files.
The following Python code changed in the repo:

{diff_text}

Suggest updates to the README.md file to reflect these changes.
Only include the new content for README, do not rewrite unrelated sections.
"""

# Call GPT-4
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that updates README.md based on code changes."},
        {"role": "user", "content": prompt}
    ]
)

readme_suggestion = response.choices[0].message.content
print("\n✅ Suggested README update:\n")
print(readme_suggestion)
