import os
from openai import OpenAI
import subprocess

# Read changed Python files from environment
changed_files = os.getenv("CHANGED_PY_FILES", "").split()
print("🔍 Debug: CHANGED_PY_FILES =", changed_files)
if not changed_files or changed_files == [""]:
    print("ℹ️ No Python files changed. Skipping README suggestion.")
    exit(0)

print(f"🔹 Changed Python files: {changed_files}")

# Initialize OpenAI client using GitHub secret
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Prepare a diff of changed files
diff_texts = []
for f in changed_files:
    if os.path.exists(f):
        try:
            diff = subprocess.check_output(["git", "diff", f], text=True)
            diff_texts.append(diff)
        except subprocess.CalledProcessError:
            pass

diff_text = "\n\n".join(diff_texts)

# Call GPT to generate README suggestion
prompt = f"""
You are a helpful assistant. Generate a concise and clear README.md update 
based on the following code changes. Suggest new sections or update existing ones:

{diff_text}
"""

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful coding assistant."},
        {"role": "user", "content": prompt},
    ]
)

readme_suggestion = response.choices[0].message.content
print("✅ GPT README suggestion generated:\n")
print(readme_suggestion)

# Append suggestion to README.md only if it doesn't already exist
readme_file = "README.md"
if os.path.exists(readme_file):
    with open(readme_file, "r", encoding="utf-8") as f:
        readme_content = f.read()
else:
    readme_content = ""

if readme_suggestion.strip() in readme_content:
    print("ℹ️ Suggestion already exists in README.md. Skipping append.")
else:
    with open(readme_file, "a", encoding="utf-8") as f:
        f.write("\n\n" + readme_suggestion)
    print(f"\n📄 Updated {readme_file} successfully.")
