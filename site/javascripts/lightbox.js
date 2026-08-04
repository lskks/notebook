document$.subscribe(() => {
  const TRANSITION_MS = 300;

  const images = document.querySelectorAll('.md-typeset img:not([data-no-lightbox])');
  images.forEach(img => {
    if (img.closest('a')) return;
    img.style.cursor = 'zoom-in';
    img.addEventListener('click', () => {
      const overlay = document.createElement('div');
      overlay.className = 'lightbox-overlay';
      overlay.setAttribute('role', 'dialog');
      overlay.setAttribute('aria-label', '放大图片');

      const imgClone = document.createElement('img');
      imgClone.src = img.src;
      imgClone.alt = img.alt || '';
      imgClone.className = 'lightbox-img';

      overlay.appendChild(imgClone);
      document.body.appendChild(overlay);

      requestAnimationFrame(() => {
        overlay.classList.add('lightbox-active');
      });

      const close = () => {
        if (!overlay.classList.contains('lightbox-active')) return;
        overlay.classList.remove('lightbox-active');
        const removeOverlay = () => overlay.remove();
        overlay.addEventListener('transitionend', removeOverlay, { once: true });
        setTimeout(removeOverlay, TRANSITION_MS + 50);
      };

      overlay.addEventListener('click', (e) => {
        if (e.target === overlay) close();
      });

      const onKeydown = (e) => {
        if (e.key === 'Escape') {
          close();
          document.removeEventListener('keydown', onKeydown);
        }
      };
      document.addEventListener('keydown', onKeydown);
    });
  });
});