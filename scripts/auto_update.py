#!/usr/bin/env python3
import os, re, sys
import requests
from packaging.version import Version

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    print("❌ 未设置 GITHUB_TOKEN 环境变量")
    sys.exit(1)

HEADERS = {'Authorization': f'Bearer {GITHUB_TOKEN}', 'Accept': 'application/vnd.github+json'}

def parse_makefile(dirpath):
    filepath = os.path.join(dirpath, 'Makefile')
    if not os.path.exists(filepath):
        return None
    with open(filepath) as f:
        content = f.read()
    data = {'dir': dirpath, 'file': filepath}
    for key in ['PKG_NAME', 'PKG_VERSION', 'PKG_SOURCE_URL']:
        m = re.search(rf'{key}:=(\S+)', content)
        if m:
            data[key] = m.group(1)
    return data if all(k in data for k in ['PKG_NAME', 'PKG_VERSION', 'PKG_SOURCE_URL']) else None

def get_latest_tag(owner_repo):
    url = f'https://api.github.com/repos/{owner_repo}/git/refs/tags'
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        return None
    tags = []
    for item in resp.json():
        tag = item['ref'].replace('refs/tags/', '')
        tag_clean = tag.lstrip('v')
        try:
            tags.append((tag, Version(tag_clean)))
        except:
            continue
    if not tags:
        return None
    tags.sort(key=lambda x: x[1], reverse=True)
    return tags[0][0]

def update_makefile(filepath, old_ver, new_tag, old_tag):
    with open(filepath) as f:
        content = f.read()
    new_ver = new_tag.lstrip('v')
    content = content.replace(f'PKG_VERSION:={old_ver}', f'PKG_VERSION:={new_ver}')
    content = content.replace(f'PKG_SOURCE_VERSION:={old_tag}', f'PKG_SOURCE_VERSION:={new_tag}')
    with open(filepath, 'w') as f:
        f.write(content)

def main():
    for d in os.listdir('.'):
        if not os.path.isdir(d) or d.startswith('.'):
            continue
        pkg = parse_makefile(d)
        if not pkg:
            continue
        m = re.search(r'github\.com/([^/]+/[^.]+)\.git', pkg['PKG_SOURCE_URL'])
        if not m:
            continue
        owner_repo = m.group(1)
        latest_tag = get_latest_tag(owner_repo)
        if not latest_tag:
            continue
        old_tag = f"v{pkg['PKG_VERSION']}"
        if latest_tag != old_tag:
            print(f"⬆ {pkg['PKG_NAME']}: {old_tag} → {latest_tag}")
            update_makefile(pkg['file'], pkg['PKG_VERSION'], latest_tag, old_tag)
            branch = f"update/{pkg['PKG_NAME']}-{latest_tag}"
            os.system(f'git config user.name "github-actions"')
            os.system(f'git config user.email "actions@github.com"')
            os.system(f'git checkout -b {branch}')
            os.system(f'git add {pkg["file"]}')
            os.system(f'git commit -m "{pkg["PKG_NAME"]}: update to {latest_tag}"')
            os.system(f'git push origin {branch}')
            os.system(f'gh pr create --title "{pkg["PKG_NAME"]}: update to {latest_tag}" --body "自动更新。" --base main --head {branch}')
        else:
            print(f"✓ {pkg['PKG_NAME']}: {old_tag} 已是最新")

if __name__ == '__main__':
    main()