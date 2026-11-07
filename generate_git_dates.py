"""从 Git 历史生成文章的创建与最近修改时间。"""

import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
OUTPUT = DOCS / "javascripts" / "git-dates.js"


def git_dates(relative_path: str) -> dict[str, str] | None:
    result = subprocess.run(
        ["git", "log", "--follow", "--format=%aI", "--", f"docs/{relative_path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    dates = result.stdout.splitlines()
    if not dates:
        return None
    return {"created": dates[-1], "updated": dates[0]}


def main() -> None:
    data = {}
    for path in sorted(DOCS.rglob("*.md")):
        relative_path = path.relative_to(DOCS).as_posix()
        dates = git_dates(relative_path)
        if dates:
            data[relative_path] = dates

    content = (
        "// 此文件由 generate_git_dates.py 自动生成，请勿手动修改。\n"
        f"window.__GIT_DATES__ = {json.dumps(data, ensure_ascii=False, indent=2)};\n"
    )
    if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != content:
        OUTPUT.write_text(content, encoding="utf-8")
    print(f"已生成 {len(data)} 篇文章的时间数据：{OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
