"""生成主页第二屏:最新笔记 + 分类入口。

结果以静态 HTML 写入 docs/index.md 的标记区块之间,
保证链接出现在页面源码中,对搜索引擎友好。
"""

import re
from pathlib import Path
from urllib.parse import quote

from generate_git_dates import ROOT, DOCS, ensure_full_history, git_dates

INDEX = DOCS / "index.md"
START = "<!-- homepage:start -->"
END = "<!-- homepage:end -->"
LATEST_COUNT = 6

FIRST_LEVEL = {
    "mathematics": "数学",
    "cs": "计算机科学",
    "cpp": "C++",
    "tools": "工具",
}

CATEGORIES = {
    "mathematics/discretemath": "离散数学",
    "mathematics/probability": "概率论",
    "cs/co": "计算机组成",
    "cs/csapp": "CSAPP",
    "cs/ds": "数据结构",
    "cpp/ms": "移动语义",
}

CJK = re.compile(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]")
WORD = re.compile(r"[A-Za-z0-9]+")


FRONTMATTER = re.compile(r"^---[ \t]*\n(.*?)\n---[ \t]*\n", re.S)
FRONTMATTER_TITLE = re.compile(r'^title:[ \t]*"?([^"\n]+)"?[ \t]*$', re.M)
HEADING = re.compile(r"^(#{1,2})[ \t]+(.+?)[ \t]*$")


def article_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    frontmatter = FRONTMATTER.match(text)
    if frontmatter:
        matched = FRONTMATTER_TITLE.search(frontmatter.group(1))
        if matched:
            return matched.group(1).strip()
    body = text[frontmatter.end() :] if frontmatter else text

    levels: dict[int, str] = {}
    in_code = False
    for line in body.splitlines():
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        matched = HEADING.match(line)
        if matched:
            levels.setdefault(len(matched.group(1)), matched.group(2))

    return levels.get(1) or levels.get(2) or path.stem


def count_chars(path: Path) -> tuple[int, int]:
    """返回 (总字数, 预计阅读分钟数)。中文按字、英文按词计。"""
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`]*`", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)

    cjk = len(CJK.findall(text))
    words = len(WORD.findall(text))
    minutes = max(1, round(cjk / 300 + words / 200))
    return cjk + words, minutes


def to_url(relative_path: str) -> str:
    slug = relative_path[: -len(".md")]
    if slug.endswith("index"):
        slug = slug[: -len("index")]
    return "/" + quote(slug.strip("/")) + ("/" if slug else "")


def collect_articles() -> list[dict]:
    articles = []
    for path in sorted(DOCS.rglob("*.md")):
        relative_path = path.relative_to(DOCS).as_posix()
        if relative_path.endswith("index.md"):
            continue
        dates = git_dates(relative_path)
        if not dates:
            continue
        folder = relative_path.rsplit("/", 1)[0] if "/" in relative_path else ""
        total, minutes = count_chars(path)
        articles.append(
            {
                "title": article_title(path),
                "url": to_url(relative_path),
                "category": CATEGORIES.get(folder, FIRST_LEVEL.get(folder, "笔记")),
                "updated": dates["updated"][:10],
                "chars": total,
                "minutes": minutes,
                "folder": folder.split("/")[0] if folder else "",
            }
        )
    return articles


def render(articles: list[dict]) -> str:
    latest = sorted(articles, key=lambda item: item["updated"], reverse=True)[:LATEST_COUNT]
    cards = "".join(
        '<a class="note-card" href="{url}">'
        '<span class="note-card__category">{category}</span>'
        '<h3 class="note-card__title">{title}</h3>'
        '<span class="note-card__meta">'
        '<span>更新于 {updated}</span>'
        "<span>约 {chars} 字 · {minutes} 分钟</span>"
        "</span></a>".format(**item)
        for item in latest
    )

    groups = "".join(
        '<a class="category-card" href="/{key}/">'
        '<span class="category-card__name">{name}</span>'
        '<span class="category-card__count">{count} 篇笔记</span>'
        "</a>".format(
            key=key,
            name=name,
            count=sum(1 for item in articles if item["folder"] == key),
        )
        for key, name in FIRST_LEVEL.items()
    )

    total = len(articles)
    return (
        '<section class="home-section" id="notes">'
        '<div class="home-section__inner">'
        '<h2 class="home-heading">最新笔记</h2>'
        '<p class="home-subheading">共 {total} 篇,按最近更新时间排序</p>'
        '<div class="note-grid">{cards}</div>'
        '<h2 class="home-heading">分类浏览</h2>'
        '<div class="category-grid">{groups}</div>'
        "</div></section>"
    ).format(total=total, cards=cards, groups=groups)


def main() -> None:
    ensure_full_history()
    articles = collect_articles()
    if not articles:
        print("未找到文章,跳过主页生成")
        return

    source = INDEX.read_text(encoding="utf-8")
    start = source.find(START)
    end = source.find(END)
    if start == -1 or end == -1:
        print(f"index.md 中缺少标记 {START} / {END},已跳过")
        return

    updated = source[: start + len(START)] + "\n" + render(articles) + "\n" + source[end:]
    if updated != source:
        INDEX.write_text(updated, encoding="utf-8")
    print(f"已生成主页:最新 {LATEST_COUNT} 篇,共 {len(articles)} 篇笔记")


if __name__ == "__main__":
    main()
