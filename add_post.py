#!/usr/bin/env python3
"""Add or update a post in data/posts.json, then git commit & push.

Examples:
  # new post (no products yet)
  python3 add_post.py --id my-post --title "제목" --date 2026-10-27 \
      --youtube https://www.youtube.com/watch?v=XXXX [--thumbnail assets/x.jpg]

  # add products (repeatable --product "이름|URL|메모"); merges into existing post
  python3 add_post.py --id my-post --product "상품명|https://link.coupang.com/a/xxxx|한줄 설명"

  # replace the whole product list instead of appending
  python3 add_post.py --id my-post --replace-products --product "..."

  # remove a post
  python3 add_post.py --id my-post --delete

Options: --no-push (commit only), --dry-run (print JSON, no write).
Posts are kept sorted newest first by date.
"""
import argparse, json, os, subprocess, sys
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data", "posts.json")


def https_url(u, what):
    p = urlparse(u)
    if p.scheme != "https" or not p.netloc:
        sys.exit(f"error: {what} must be an https URL: {u}")
    return u


def parse_product(s):
    parts = [x.strip() for x in s.split("|")]
    if len(parts) < 2 or not parts[0]:
        sys.exit(f'error: --product must be "이름|URL|메모": {s}')
    return {"name": parts[0], "url": https_url(parts[1], "product url"),
            "note": parts[2] if len(parts) > 2 else ""}


def git(*args):
    subprocess.run(["git", "-C", ROOT, *args], check=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--id", required=True)
    ap.add_argument("--title"); ap.add_argument("--date"); ap.add_argument("--youtube")
    ap.add_argument("--thumbnail")
    ap.add_argument("--product", action="append", default=[])
    ap.add_argument("--replace-products", action="store_true")
    ap.add_argument("--delete", action="store_true")
    ap.add_argument("--no-push", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    with open(DATA, encoding="utf-8") as f:
        posts = json.load(f)
    idx = next((i for i, p in enumerate(posts) if p.get("id") == a.id), None)

    if a.delete:
        if idx is None: sys.exit(f"error: no post with id {a.id}")
        posts.pop(idx); msg = f"Remove post {a.id}"
    else:
        if idx is None:
            if not (a.title and a.date):
                sys.exit("error: new post needs --title and --date")
            post = {"id": a.id, "title": "", "date": "", "youtube_url": "", "products": []}
            posts.append(post); msg = f"Add post {a.id}"
        else:
            post = posts[idx]; msg = f"Update post {a.id}"
        if a.title: post["title"] = a.title
        if a.date: post["date"] = a.date
        if a.youtube: post["youtube_url"] = https_url(a.youtube, "youtube url")
        if a.thumbnail: post["thumbnail"] = a.thumbnail
        new = [parse_product(s) for s in a.product]
        if a.replace_products:
            post["products"] = new
        else:
            existing = post.setdefault("products", [])
            urls = {p["url"] for p in existing}
            existing.extend(p for p in new if p["url"] not in urls)
    posts.sort(key=lambda p: p.get("date", ""), reverse=True)

    out = json.dumps(posts, ensure_ascii=False, indent=2) + "\n"
    if a.dry_run:
        print(out); return
    with open(DATA, "w", encoding="utf-8") as f:
        f.write(out)
    git("add", "-A", "data", "assets")
    if subprocess.run(["git", "-C", ROOT, "diff", "--cached", "--quiet"]).returncode == 0:
        print("no changes"); return
    git("commit", "-m", msg)
    if not a.no_push:
        git("pull", "--rebase", "--quiet")
        git("push", "--quiet")
    print(msg)


if __name__ == "__main__":
    main()
