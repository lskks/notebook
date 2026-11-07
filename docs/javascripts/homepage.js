// 主页:标记首页状态,并让第二屏卡片滚动进入时淡入
let homeObserver = null;

document$.subscribe(() => {
  const heroSection = document.querySelector('.hero-section.is-homepage');
  document.body.classList.toggle('is-homepage', Boolean(heroSection));

  homeObserver?.disconnect();
  homeObserver = null;

  const section = document.querySelector('.home-section');
  if (!section) return;

  const cards = section.querySelectorAll('.note-card, .category-card');
  if (!cards.length) return;

  if (!('IntersectionObserver' in window)) {
    cards.forEach((card) => card.classList.add('is-visible'));
    return;
  }

  section.classList.add('is-animated');
  homeObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        homeObserver.unobserve(entry.target);
      });
    },
    { threshold: 0.15 }
  );

  cards.forEach((card) => homeObserver.observe(card));
});

// 首屏向下按钮:instant navigation 会接管带 hash 的链接并打断滚动,
// 这里手动处理,保证第一次点击就能跳转。
document.addEventListener('click', (event) => {
  const button = event.target.closest('.hero-scroll-button');
  if (!button) return;

  const href = button.getAttribute('href');
  const target = href?.startsWith('#') ? document.querySelector(href) : null;
  if (!target) return;

  event.preventDefault();
  target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  history.replaceState(history.state, '', href);
});
