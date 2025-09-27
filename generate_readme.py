import os
from openai import OpenAI
import subprocess
from datetime import datetime

# Read changed Python files from GitHub Actions env
changed_files = os.getenv("CHANGED_PY_FILES", "").split()
print("🔍 Debug: CHANGED_PY_FILES =", changed_files)

if not changed_files or changed_files == [""]:
    print("ℹ️ No Python files changed. Skipping README update.")
    exit(0)

print(f"🔹 Changed Python files: {changed_files}")

# Initialize OpenAI client using GitHub secret
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Prepare diffs of changed files
diff_texts = []
for f in changed_files:
    if os.path.exists(f):
        try:
            diff = subprocess.check_output(["git", "diff", f], text=True)
            diff_texts.append(diff)
        except subprocess.CalledProcessError:
            print(f"⚠️ Could not get diff for {f}, skipping.")

diff_text = "\n\n".join(diff_texts)
if not diff_text.strip():
    print("ℹ️ No diffs found. Skipping README update.")
    exit(0)

# GPT prompt
prompt = f"""
You are a helpful assistant. Generate a concise README.md update 
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

readme_suggestion = response.choices[0].message.content.strip()
print("✅ GPT README suggestion generated:\n")
print(readme_suggestion)

# Prepare update content with timestamp
readme_file = "README.md"
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
update_content = f"\n\n## GPT Suggested Update ({timestamp})\n{readme_suggestion}\n"

# Ensure README.md exists
if not os.path.exists(readme_file):
    with open(readme_file, "w", encoding="utf-8") as f:
        f.write("# Project\n")

# Append update unconditionally
with open(readme_file, "a", encoding="utf-8") as f:
    f.write(update_content)

print(f"📄 Updated {readme_file} successfully.")
