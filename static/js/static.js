// Tailwind 커스텀 설정 (폰트/컬러) - CDN 모드용
tailwind.config = {
    theme: {
        extend: {
            fontFamily: {
                'pixel': ['"Press Start 2P"', 'cursive'],
            },
            colors: {
                'brand-dark': '#0d1117',
                'brand-gray': '#161b22',
                'brand-blue': '#00dbde',
                'brand-light': '#c9d1d9',
                'brand-dim': '#8b949e',
            },
        },
    },
};

document.addEventListener('DOMContentLoaded', () => {
    // --- DOM 참조 ---
    const form = document.getElementById('generate-form');
    const input = document.getElementById('prompt-input');
    const button = document.getElementById('generate-button');

    const loader = document.getElementById('loading-spinner');
    const loadingText = document.getElementById('loading-text');
    const errorMessage = document.getElementById('error-message');

    const focusContainer = document.getElementById('focus-container');
    const historySidebar = document.getElementById('history-sidebar');
    const historyTitle = document.getElementById('history-title');
    const gallery = document.getElementById('gallery');

    // 로딩 문구
    const loadingPhrases = [
        'AI가 서울의 픽셀을 그리는 중...',
        '경복궁 지붕을 칠하고 있습니다...',
        '떡볶이에 고추장 양념을 버무리는 중...',
        '이순신 장군님을 32x32 픽셀로...',
        '거의 다 됐습니다! (8초 이내)'
    ];
    let loadingInterval = null;

    // --- 이벤트 리스너 ---
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const prompt = input.value.trim();
        if (!prompt) return;

        setLoading(true);

        try {
            const response = await fetch('/api/v1/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            const imageUrl = data.imageUrl;

            displayNewImage(imageUrl, prompt);
            input.value = '';
        } catch (err) {
            console.error('Error generating image:', err);
            showError('이미지 생성에 실패했습니다. 잠시 후 다시 시도해주세요.');
        } finally {
            setLoading(false);
        }
    });

    // --- 함수 정의 ---

    // 로딩 상태 on/off
    function setLoading(isLoading) {
        if (isLoading) {
            loader.classList.remove('hidden');
            loadingText.classList.remove('hidden');
            errorMessage.classList.add('hidden');

            button.disabled = true;
            button.classList.add('opacity-50', 'cursor-not-allowed');

            let phraseIndex = 0;
            loadingText.textContent = loadingPhrases[phraseIndex];

            loadingInterval = setInterval(() => {
                phraseIndex = (phraseIndex + 1) % loadingPhrases.length;
                loadingText.textContent = loadingPhrases[phraseIndex];
            }, 1500);
        } else {
            loader.classList.add('hidden');
            loadingText.classList.add('hidden');

            button.disabled = false;
            button.classList.remove('opacity-50', 'cursor-not-allowed');

            if (loadingInterval) {
                clearInterval(loadingInterval);
                loadingInterval = null;
            }
        }
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.remove('hidden');
    }

    // 새 이미지 포커스 + 이전 포커스는 오른쪽 히스토리로 이동
    function displayNewImage(imageUrl, prompt) {
        // 1. 기존 포커스 아이템이 있다면 히스토리로 이동
        const oldFocusItem = focusContainer.querySelector('.focus-item');
        if (oldFocusItem) {
            const historyItem = createGalleryItem(
                oldFocusItem.dataset.imageUrl,
                oldFocusItem.dataset.prompt
            );
            gallery.prepend(historyItem);
        }

        // 2. 새 포커스 아이템 생성
        const newFocus = document.createElement('div');
        newFocus.className = 'focus-item';
        newFocus.dataset.imageUrl = imageUrl;
        newFocus.dataset.prompt = prompt;

        newFocus.innerHTML = `
            <div class="aspect-square bg-gray-700 rounded-md mb-4 overflow-hidden">
                <img
                    src="${imageUrl}"
                    alt="${prompt} 픽셀 아트"
                    class="w-full h-full object-cover pixelated"
                >
            </div>
            <p class="text-[10px] md:text-xs text-center text-brand-light">
                "${prompt}" 픽셀 아트 생성 완료!
            </p>
        `;

        // 안내 문구 제거 후 새 포커스 삽입
        focusContainer.innerHTML = '';
        focusContainer.appendChild(newFocus);

        // 3. 히스토리 사이드바 표시
        historySidebar.classList.remove('hidden');
        historyTitle.classList.remove('hidden');
    }

    // 히스토리 카드 생성
    function createGalleryItem(imageUrl, prompt) {
        const item = document.createElement('div');
        item.className = 'gallery-item bg-brand-gray rounded-lg border border-gray-700 shadow-md p-2';

        item.innerHTML = `
            <div class="aspect-square bg-gray-800 rounded-md overflow-hidden">
                <img
                    src="${imageUrl}"
                    alt="${prompt} 픽셀 아트"
                    class="w-full h-full object-cover pixelated"
                >
            </div>
            <p class="mt-2 text-[9px] md:text-[10px] text-center text-brand-dim">
                "${prompt}"
            </p>
        `;
        return item;
    }
});
