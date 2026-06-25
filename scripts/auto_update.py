#!/usr/bin/env python3
import os, re, sys, subprocess
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

def update_makefile(filepath, old_ver, new_tag):
    with open(filepath) as f:
        content = f.read()
    new_ver = new_tag.lstrip('v')
    content = content.replace(f'PKG_VERSION:={old_ver}', f'PKG_VERSION:={new_ver}')
    content = re.sub(r'PKG_SOURCE_VERSION:=.*', f'PKG_SOURCE_VERSION:={new_tag}', content)
    with open(filepath, 'w') as f:
        f.write(content)

def run(cmd):
    return subprocess.run(cmd, shell=True).returncode

def main():
    run('git config user.name "github-actions"')
    run('git config user.email "actions@github.com"')

    updated = []

    for d in sorted(os.listdir('.')):
        if not os.path.isdir(d) or d.startswith('.'):
            continue
        pkg = parse_makefile(d)
        if not pkg:
            continue
        m = re.search(r'github\.com/([^/]+/[^.]+?)(?:\.git)?$', pkg['PKG_SOURCE_URL'])
        if not m:
            continue
        owner_repo = m.group(1)
        latest_tag = get_latest_tag(owner_repo)
        if not latest_tag:
            print(f"⚠ {pkg['PKG_NAME']}: 无法获取最新 tag，跳过")
            continue

        old_ver = pkg['PKG_VERSION']
        old_tag = f"v{old_ver}"

        if latest_tag == old_tag:
            print(f"✓ {pkg['PKG_NAME']}: {old_tag} 已是最新")
            continue

        print(f"⬆ {pkg['PKG_NAME']}: {old_tag} → {latest_tag}")
        update_makefile(pkg['file'], old_ver, latest_tag)
        run(f'git add {pkg["file"]}')
        updated.append(f'{pkg["PKG_NAME"]}: {old_tag} → {latest_tag}')

    if not updated:
        print("所有包均为最新，无需提交。")
        return

    # 将所有更新合并成一个 commit 推送到 main
    commit_msg = "chore: auto update packages\n\n" + "\n".join(f"- {u}" for u in updated)
    run(f'git commit -m "{commit_msg}"')
    ret = run('git push origin HEAD')
    if ret == 0:
        print(f"✅ 已直接推送到 main，共更新 {len(updated)} 个包")
    else:
        print("❌ 推送失败")
        sys.exit(1)

if __name__ == '__main__':
    main()
