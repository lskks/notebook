document$.subscribe(() => {
  const heroSection = document.querySelector('.hero-section.is-homepage');
  if (heroSection) {
    document.body.classList.add('is-homepage');
  } else {
    document.body.classList.remove('is-homepage');
  }
});