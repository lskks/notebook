"""为构建产物的 sitemap.xml 补充 lastmod（取 Git 最近提交时间）。"""

import re
from pathlib import Path
from urllib.parse import unquote, urlparse

from generate_git_dates import ROOT, ensure_full_history, git_dates

SITEMAP = ROOT / "site" / "sitemap.xml"
SITE_URL = "https://www.ljhkss.top"

LOC_PATTERN = re.compile(r"(?P<indent>[ \t]*)<loc>(?P<loc>[^<]+)</loc>")
LASTMOD_PATTERN = re.compile(r"[ \t]*<lastmod>[^<]*</lastmod>\n?")


def page_dates(url: str) -> dict[str, str] | None:
    path = unquote(urlparse(url).path)
    relative_path = path.strip("/")
    candidates = (
        [f"{relative_path}/index.md", f"{relative_path}.md"]
        if relative_path
        else ["index.md"]
    )
    for candidate in candidates:
        if (ROOT / "docs" / candidate).is_file():
            return git_dates(candidate)
    return None


def add_lastmod(match: re.Match[str]) -> str:
    indent, loc = match.group("indent"), match.group("loc")
    dates = page_dates(loc) if loc.startswith(SITE_URL) else None
    if not dates:
        return match.group(0)
    return f"{indent}<loc>{loc}</loc>\n{indent}<lastmod>{dates['updated'][:10]}</lastmod>"


def main() -> None:
    ensure_full_history()
    if not SITEMAP.is_file():
        print(f"未找到 sitemap，跳过：{SITEMAP.relative_to(ROOT)}")
        return

    original = SITEMAP.read_text(encoding="utf-8")
    stripped = LASTMOD_PATTERN.sub("", original)
    updated = LOC_PATTERN.sub(add_lastmod, stripped)
    if updated != original:
        SITEMAP.write_text(updated, encoding="utf-8")

    count = updated.count("<lastmod>")
    print(f"已为 sitemap 中 {count} 个 URL 补充 lastmod")


if __name__ == "__main__":
    main()
