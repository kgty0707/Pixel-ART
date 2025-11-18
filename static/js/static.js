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
    const form = document.getElementById('generate-form');
    const input = document.getElementById('prompt-input');
    const button = document.getElementById('generate-button');

    const focusContainer = document.getElementById('focus-container');
    const historySidebar = document.getElementById('history-sidebar');
    const historyTitle = document.getElementById('history-title');
    const gallery = document.getElementById('gallery');

    const loadingPhrases = [
        'AI가 서울의 픽셀을 그리고 있어요..',
        '픽셀 하나하나에 마음을 담아 공들이는 중이예요..',
        '좀 더 신경쓰고 있어요..',
    ];
    let loadingInterval = null;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const prompt = input.value.trim();
        if (!prompt) return;

        setLoading(true); // 로딩 UI를 focusContainer에 그리기

        try {
            const response = await fetch('/api/v1/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt }),
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

            const data = await response.json();
            const jobId = data.jobId;
            if (!jobId) throw new Error('유효하지 않은 응답입니다.');

            const result = await waitForResult(jobId);

            let imageUrl = result.imageUrl;
            if (!imageUrl && result.imageData) {
                imageUrl = `data:image/png;base64,${result.imageData}`;
            }
            if (!imageUrl) throw new Error('이미지 URL을 찾을 수 없습니다.');

            displayNewImage(imageUrl, prompt);
            input.value = '';
        } catch (err) {
            console.error('Error generating image:', err);
            showError('이미지 생성에 실패했습니다. 잠시 후 다시 시도해주세요.');
        } finally {
            setLoading(false); // 로딩 종료 (인터벌 해제)
        }
    });

    // 폴링 함수 (그대로 유지)
    async function waitForResult(jobId) {
        while (true) {
            const res = await fetch(`/api/v1/result/${jobId}`);
            if (res.status === 202) {
                await new Promise((resolve) => setTimeout(resolve, 1000));
                continue;
            }
            if (!res.ok) throw new Error(`Result error! status: ${res.status}`);
            return await res.json();
        }
    }

    // 로딩 상태 처리: focusContainer 내부에 HTML 직접 주입
    function setLoading(isLoading) {
        if (isLoading) {
            button.disabled = true;
            button.classList.add('opacity-50', 'cursor-not-allowed');

            // 로딩 화면을 focusContainer 안에 그리기
            focusContainer.innerHTML = `
                <div class="flex flex-col items-center justify-center gap-4 animate-pulse">
                    <div class="loader"></div> 
                    
                    <p id="dynamic-loading-text" class="w-64 text-[10px] md:text-xs text-brand-dim text-center break-keep leading-relaxed">
                        ${loadingPhrases[0]}
                    </p>
                </div>
            `;

            // 문구 롤링 로직
            const dynamicText = document.getElementById('dynamic-loading-text');
            let phraseIndex = 0;
            
            loadingInterval = setInterval(() => {
                phraseIndex = (phraseIndex + 1) % loadingPhrases.length;
                if(dynamicText) {
                    dynamicText.textContent = loadingPhrases[phraseIndex];
                }
            }, 1500);

        } else {
            button.disabled = false;
            button.classList.remove('opacity-50', 'cursor-not-allowed');

            if (loadingInterval) {
                clearInterval(loadingInterval);
                loadingInterval = null;
            }
        }
    }

    // 에러 메시지도 focusContainer 중앙에 표시
    function showError(message) {
        focusContainer.innerHTML = `
            <div class="flex flex-col items-center justify-center gap-2 text-red-500">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <p class="text-[10px] md:text-xs text-center leading-relaxed">
                    ${message}
                </p>
                <button onclick="location.reload()" class="mt-2 text-[10px] underline hover:text-red-400">
                    새로고침
                </button>
            </div>
        `;
    }

    function displayNewImage(imageUrl, prompt) {
        const newFocus = document.createElement('div');
        newFocus.className = 'focus-item w-full max-w-sm flex flex-col items-center';
        newFocus.dataset.imageUrl = imageUrl;
        newFocus.dataset.prompt = prompt;

        newFocus.innerHTML = `
            <div class="w-full aspect-square bg-gray-700 rounded-xl mb-4 overflow-hidden shadow-2xl border border-gray-700 group relative">
                <img
                    src="${imageUrl}"
                    alt="${prompt} 픽셀 아트"
                    class="w-full h-full object-cover pixelated transition-transform duration-500 group-hover:scale-105 animate-diffusion"
                >
            </div>
            <div class="bg-brand-gray border border-gray-700 rounded-lg px-4 py-2">
                <p class="text-[10px] md:text-xs text-center text-brand-blue">
                    "${prompt}"
                </p>
            </div>
        `;

        // 컨테이너 비우고 새 요소 추가
        const focusContainer = document.getElementById('focus-container');
        focusContainer.innerHTML = '';
        focusContainer.appendChild(newFocus);
        
        // 히스토리 추가
        const gallery = document.getElementById('gallery');
        const historyItem = createGalleryItem(imageUrl, prompt);
        gallery.prepend(historyItem);

        // 히스토리 사이드바 표시
        const historySidebar = document.getElementById('history-sidebar');
        const historyTitle = document.getElementById('history-title');
        historySidebar.classList.remove('hidden');
        historyTitle.classList.remove('hidden');
    }

    function createGalleryItem(imageUrl, prompt) {
        const item = document.createElement('div');
        item.className = 'gallery-item bg-brand-gray rounded-lg border border-gray-700 shadow-md p-2 cursor-pointer hover:border-brand-blue transition-colors';
        
        // 클릭 시 다시 포커스로 가져오기
        item.onclick = () => displayNewImage(imageUrl, prompt);

        item.innerHTML = `
            <div class="aspect-square bg-gray-800 rounded-md overflow-hidden mb-2">
                <img
                    src="${imageUrl}"
                    alt="${prompt} 픽셀 아트"
                    class="w-full h-full object-cover pixelated"
                >
            </div>
            <p class="text-[9px] md:text-[10px] text-center text-brand-dim truncate px-1">
                ${prompt}
            </p>
        `;
        return item;
    }
});