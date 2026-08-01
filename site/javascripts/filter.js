document$.subscribe(() => {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const contentItems = document.querySelectorAll('.content-item');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            const filter = button.getAttribute('data-filter');
            
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            contentItems.forEach(item => {
                if (filter === 'all') {
                    item.style.display = 'block';
                    item.style.opacity = '1';
                } else {
                    if (item.getAttribute('data-category') === filter) {
                        item.style.display = 'block';
                        item.style.opacity = '1';
                    } else {
                        item.style.display = 'none';
                        item.style.opacity = '0';
                    }
                }
            });
        });
    });
});