document.addEventListener('DOMContentLoaded', () => {
    const convertBtn = document.getElementById('convert-btn');
    const copyBtn = document.getElementById('copy-btn');
    const keywordInput = document.getElementById('keyword-input');
    const resultOutput = document.getElementById('result-output');

    // Convert button click event
    convertBtn.addEventListener('click', async () => {
        const keywords = keywordInput.value.trim();
        const selectedPersona = document.querySelector('input[name="persona"]:checked').value;

        if (!keywords) {
            alert('핵심 키워드를 입력해주세요.');
            keywordInput.focus();
            return;
        }

        // Start loading state
        resultOutput.classList.add('loading');
        resultOutput.innerHTML = '<p class="loading-message">AI가 메시지를 생성 중입니다. 잠시만 기다려주세요...</p>';
        convertBtn.disabled = true;
        copyBtn.disabled = true; // Disable copy button while loading

        try {
            // Fetch request to the backend API
            const response = await fetch('/api/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    keywords: keywords,
                    persona: selectedPersona,
                }),
            });

            if (!response.ok) {
                // Try to parse error response from backend
                let errorMsg = `API call failed with status ${response.status}`;
                try {
                    const errorData = await response.json();
                    errorMsg = errorData.error || errorMsg;
                } catch (e) {
                    // If response is not JSON, use the status text
                    errorMsg = response.statusText || errorMsg;
                }
                throw new Error(errorMsg);
            }

            const data = await response.json();
            // Display the converted message received from the backend
            resultOutput.innerHTML = `<p>${data.converted_message}</p>`;

        } catch (error) {
            console.error('Error:', error);
            resultOutput.innerHTML = `<p style="color: red;">오류가 발생했습니다: ${error.message}. 잠시 후 다시 시도해주세요.</p>`;
        } finally {
            // End loading state
            resultOutput.classList.remove('loading');
            convertBtn.disabled = false;
            copyBtn.disabled = false; // Re-enable copy button
        }
    });

    // Copy button click event
    copyBtn.addEventListener('click', () => {
        const textToCopy = resultOutput.innerText;
        // Check if there's text to copy and if it's not the loading message
        if (textToCopy && textToCopy !== '변환 버튼을 누르면 결과가 여기에 표시됩니다.' && !resultOutput.classList.contains('loading')) {
            navigator.clipboard.writeText(textToCopy)
                .then(() => {
                    alert('메시지가 클립보드에 복사되었습니다.');
                })
                .catch(err => {
                    console.error('복사 실패:', err);
                    alert('복사에 실패했습니다.');
                });
        } else if (resultOutput.classList.contains('loading')) {
            alert('메시지가 로딩 중입니다. 완료 후 다시 시도해주세요.');
        } else {
            alert('복사할 내용이 없습니다.');
        }
    });
});