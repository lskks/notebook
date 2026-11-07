// 在文章末尾显示 Git 创建与最近修改时间
document$.subscribe(() => {
  document.querySelector('.article-dates')?.remove();

  const content = document.querySelector('.md-content__inner');
  const editLink = document.querySelector('a.md-content__button[rel="edit"]');
  if (!content || !editLink || !window.__GIT_DATES__) return;

  const match = editLink.href.match(/\/docs\/([^?#]+\.md)(?:[?#].*)?$/);
  if (!match) return;

  const dates = window.__GIT_DATES__[decodeURIComponent(match[1])];
  if (!dates) return;

  const formatDate = (iso) => iso.slice(0, 10);

  const footer = document.createElement('footer');
  footer.className = 'article-dates';
  footer.setAttribute('aria-label', '文章时间');
  footer.innerHTML = `
    <span class="article-dates__item">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M8 2v4"/><path d="M16 2v4"/>
        <rect width="18" height="18" x="3" y="4" rx="2"/>
        <path d="M3 10h18"/><path d="M12 14v4"/><path d="M10 16h4"/>
      </svg>
      <span>创建 <time datetime="${dates.created}">${formatDate(dates.created)}</time></span>
    </span>
    <span class="article-dates__item">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M3 12a9 9 0 1 0 3-6.7L3 8"/>
        <path d="M3 3v5h5"/><path d="M12 7v5l3 2"/>
      </svg>
      <span>更新 <time datetime="${dates.updated}">${formatDate(dates.updated)}</time></span>
    </span>`;

  // 放在标签之前;有脚注时自然位于脚注之后
  const tags = content.querySelector('.md-tags');
  if (tags) {
    content.insertBefore(footer, tags);
  } else {
    content.appendChild(footer);
  }
});
