document$.subscribe(function() {
  'use strict';

  const imageOptimizer = {
    init: function() {
      this.setupLazyLoading();
      this.setupResponsiveImages();
      this.handleImageErrors();
      this.preloadCriticalImages();
    },

    setupLazyLoading: function() {
      const images = document.querySelectorAll('.md-typeset img');

      if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              const img = entry.target;
              const src = img.getAttribute('data-src');

              if (src) {
                img.src = src;
                img.removeAttribute('data-src');
              }

              img.classList.add('loaded', 'is-loaded');
              observer.unobserve(img);
            }
          });
        }, {
          rootMargin: '50px 0px',
          threshold: 0.01
        });

        images.forEach(img => {
          if (!img.hasAttribute('loading')) {
            img.setAttribute('loading', 'lazy');
          }

          if (img.dataset.src) {
            imageObserver.observe(img);
          } else {
            img.classList.add('loaded', 'is-loaded');
          }
        });
      } else {
        images.forEach(img => {
          if (!img.hasAttribute('loading')) {
            img.setAttribute('loading', 'lazy');
          }
          img.classList.add('loaded', 'is-loaded');
        });
      }
    },

    setupResponsiveImages: function() {
      const images = document.querySelectorAll('.md-typeset img[srcset]');

      images.forEach(img => {
        const loadResponsiveImage = () => {
          const width = window.innerWidth;
          let src = img.src;

          if (width <= 480 && img.dataset.src480) {
            src = img.dataset.src480;
          } else if (width <= 768 && img.dataset.src768) {
            src = img.dataset.src768;
          } else if (width <= 1024 && img.dataset.src1024) {
            src = img.dataset.src1024;
          }

          if (src !== img.src) {
            const newImg = new Image();
            newImg.onload = function() {
              img.src = src;
            };
            newImg.src = src;
          }
        };

        window.addEventListener('resize', this.debounce(loadResponsiveImage, 250));
        loadResponsiveImage();
      });
    },

    handleImageErrors: function() {
      document.addEventListener('error', function(e) {
        if (e.target.tagName === 'IMG') {
          e.target.classList.add('error');
          console.warn('图片加载失败:', e.target.src);
        }
      }, true);
    },

    preloadCriticalImages: function() {
      const criticalImages = [
        '../images/hero-bg.webp',
        '../images/favicon.jpg'
      ];

      if ('requestIdleCallback' in window) {
        requestIdleCallback(() => {
          criticalImages.forEach(src => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = 'image';
            link.href = src;
            document.head.appendChild(link);
          });
        });
      }
    },

    debounce: function(func, wait) {
      let timeout;
      return function executedFunction(...args) {
        const later = () => {
          clearTimeout(timeout);
          func.apply(this, args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
      };
    }
  };

  imageOptimizer.init();
});