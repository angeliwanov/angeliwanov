import requests
import os
import re

# Get GH_TOKEN from environment
token = os.getenv('GH_TOKEN')
username = 'angeliwanov'
headers = {'Authorization': f'token {token}'}

# Fetch all repositories
repos = []
page = 1
while True:
    response = requests.get(
        f'https://api.github.com/users/{username}/repos?per_page=100&page={page}',
        headers=headers
    ).json()
    if not response:
        break
    repos.extend(response)
    page += 1

# Aggregate language stats
languages = {}
for repo in repos:
    lang_response = requests.get(
        f"https://api.github.com/repos/{username}/{repo['name']}/languages",
        headers=headers
    ).json()
    for lang, bytes in lang_response.items():
        # Skip HTML and CSS
        if lang.lower() not in ['html', 'css']:
            languages[lang] = languages.get(lang, 0) + bytes

# Calculate percentages
total_bytes = sum(languages.values())
if total_bytes == 0:
    print("No language data found.")
    exit(0)
language_stats = {lang: (bytes / total_bytes) * 100 for lang, bytes in languages.items()}

# Read current README
with open('README.md', 'r') as file:
    content = file.read()

# Generate language stats markdown
stats_markdown = "## My Programming Languages\n"
stats_markdown += f"![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username={username}&hide=html,css&hide_border=true&layout=compact)\n\n"

# Update README (preserve existing content, replace language section)
pattern = r'## My Programming Languages\n.*?\n\n'
new_content = re.sub(pattern, stats_markdown, content, flags=re.DOTALL)
if not new_content:
    new_content = content + "\n" + stats_markdown

# Write updated README
with open('README.md', 'w') as file:
    file.write(new_content)