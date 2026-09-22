(function () {
    const DRIVE_API_URL = 'https://script.google.com/macros/s/AKfycbyb5Bc9dQn8IDZUutRbehaAqHTv3HcCjk5ma4jbF-O41XgzDLJKe04jKn3XcrZweC9_kg/exec';
    const cacheBust = Date.now();

    function getCategory(path) {
        const parts = path.split('/').map(part => part.toLowerCase());
        const galleryIndex = parts.indexOf('gallery');
        return galleryIndex >= 0 && parts[galleryIndex + 1]
            ? parts[galleryIndex + 1]
            : '';
    }

    function getTitle(filename) {
        return filename
            .replace(/\.[^/.]+$/, '')
            .replace(/[-_]+/g, ' ')
            .replace(/\b\w/g, letter => letter.toUpperCase());
    }

    function getImageUrl(url) {
        const fileId = new URL(url).searchParams.get('id');
        return fileId
            ? `https://lh3.googleusercontent.com/d/${fileId}=w1600?v=${cacheBust}`
            : `${url}${url.includes('?') ? '&' : '?'}v=${cacheBust}`;
    }

    function createGalleryItem(image) {
        const category = getCategory(image.folder);
        const item = document.createElement('div');
        item.className = 'masonry-item group';
        item.dataset.category = category || 'campus';
        item.innerHTML = `
            <div class="relative overflow-hidden rounded-xl bg-surface-container shadow-sm group-hover:shadow-lg transition-all duration-300 transform group-hover:-translate-y-1">
                <img class="w-full object-cover" src="${getImageUrl(image.url)}" alt="${getTitle(image.name)}">
                <div class="absolute inset-0 bg-gradient-to-t from-primary/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex flex-col justify-end p-6">
                    <span class="text-on-primary font-label-sm text-label-sm mb-1 uppercase tracking-widest">${category || 'Gallery'}</span>
                    <h3 class="text-on-primary font-headline-md text-headline-md">${getTitle(image.name)}</h3>
                </div>
            </div>`;
        return item;
    }

    function applyGalleryImages(images) {
        const galleryGrid = document.getElementById('gallery-grid');
        if (!galleryGrid) return;

        const galleryImages = images.filter(image => image.folder.toLowerCase().includes('/gallery/'));
        if (!galleryImages.length) return;

        galleryGrid.replaceChildren(...galleryImages.map(createGalleryItem));
    }

    function applyGalleryHighlights(images) {
        const slides = document.querySelectorAll('[data-gallery-slide]');
        if (!slides.length) return;

        const galleryImages = images.filter(image =>
            image.folder.toLowerCase().includes('/gallery/')
        );
        if (!galleryImages.length) return;

        let offset = 0;
        const updateSlides = () => {
            slides.forEach((slide, index) => {
                const image = galleryImages[(offset + index) % galleryImages.length];
                slide.style.backgroundImage = `url("${getImageUrl(image.url)}")`;
                slide.dataset.alt = getTitle(image.name);
            });
            offset = (offset + 1) % galleryImages.length;
        };

        updateSlides();
        if (galleryImages.length > slides.length) {
            window.setInterval(updateSlides, 5000);
        }
    }

    function applyFacultyImages(images) {
        const facultyImages = new Map(
            images
                .filter(image => image.folder.toLowerCase().includes('/faculty/'))
                .map(image => [image.name.toLowerCase(), image])
        );

        document.querySelectorAll('[data-drive-name]').forEach(imageElement => {
            const expectedName = imageElement.dataset.driveName.toLowerCase();
            const match = facultyImages.get(expectedName);

            if (match) {
                imageElement.src = getImageUrl(match.url);
                imageElement.addEventListener('error', () => {
                    console.error(`Drive image is not publicly viewable: ${match.name}`);
                }, { once: true });
            }
        });
    }

    function getPageFolder() {
        const pageName = window.location.pathname.split('/').pop().replace(/\.html?$/i, '').toLowerCase();
        const pageFolders = {
            index: 'homepage',
            about: 'about',
            academics: 'academics',
            facilities: 'facilities',
            faculty: 'faculty',
            admissions: 'admissions',
            news: 'news',
            events: 'events',
            'vidvat-coaching': 'vidvat-coaching'
        };

        return pageFolders[pageName] || '';
    }

    function applyPageImages(images) {
        const pageFolder = getPageFolder();
        if (!pageFolder || pageFolder === 'faculty') return;

        const pageImages = images.filter(image => {
            const folder = image.folder.toLowerCase();
            return folder.includes(`/${pageFolder}`) && (
                pageFolder !== 'faculty' || folder.includes('/faculty/')
            );
        });

        document.querySelectorAll('img[src^="images/"]').forEach(imageElement => {
            const sourceName = imageElement.getAttribute('src').split('/').pop().toLowerCase();
            const match = pageImages.find(image => image.name.toLowerCase() === sourceName);

            if (match) imageElement.src = getImageUrl(match.url);
        });
    }

    async function loadDriveImages() {
        try {
            const response = await fetch(`${DRIVE_API_URL}?v=${cacheBust}`, {
                cache: 'no-store'
            });
            if (!response.ok) throw new Error(`Drive image request failed: ${response.status}`);

            const images = await response.json();
            if (!Array.isArray(images)) throw new Error('Drive image response was not an array');

            applyGalleryImages(images);
            applyGalleryHighlights(images);
            applyFacultyImages(images);
            applyPageImages(images);
        } catch (error) {
            console.error('Drive images could not be loaded.', error);
        }
    }

    loadDriveImages();
})();
