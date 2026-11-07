// 文章字数统计与预计阅读时长
document$.subscribe(() => {
  // 只统计正文区域
  const content = document.querySelector('.md-content__inner');
  if (!content) return;

  // 移除旧的统计条(instant navigation 下页面不刷新)
  document.querySelector('.word-count-badge')?.remove();

  const text = content.innerText || '';

  // 中文(及日韩)字符按字计数,英文按词计数
  const cjkChars = (text.match(/[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]/g) || []).length;
  const enWords = (text.replace(/[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]/g, ' ')
    .match(/[a-zA-Z0-9]+/g) || []).length;
  const total = cjkChars + enWords;
  if (total === 0) return;

  // 预计阅读时长:中文 300 字/分钟,英文 200 词/分钟
  const minutes = Math.max(1, Math.round(cjkChars / 300 + enWords / 200));

  const badge = document.createElement('div');
  badge.className = 'word-count-badge';
  badge.innerHTML = `
    <span class="word-count-badge__item">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/>
        <polyline points="14 2 14 8 20 8"/>
        <line x1="16" y1="13" x2="8" y2="13"/>
        <line x1="16" y1="17" x2="8" y2="17"/>
      </svg>
      <span>全文约 ${total.toLocaleString()} 字</span>
    </span>
    <span class="word-count-badge__item">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <circle cx="12" cy="12" r="9"/>
        <polyline points="12 7 12 12 15.5 14"/>
      </svg>
      <span>预计阅读 ${minutes} 分钟</span>
    </span>`;

  // 插入到正文标题之后
  const h1 = content.querySelector('h1');
  if (h1) {
    h1.after(badge);
  } else {
    content.prepend(badge);
  }
});
