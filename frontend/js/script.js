document.addEventListener('DOMContentLoaded', () => {
    const originalTextInput = document.getElementById('original-text');
    const convertedTextInput = document.getElementById('converted-text');
    const convertButton = document.getElementById('convert-button');
    const copyButton = document.getElementById('copy-button');
    const currentCharCount = document.getElementById('current-char-count');
    const feedbackMessage = document.getElementById('feedback-message');
    const radioButtons = document.querySelectorAll('input[name="target"]');

    const MAX_CHARS = 500;
    const API_ENDPOINT = '/api/convert'; // Flask backend endpoint

    // --- Utility Functions ---
    function showFeedback(message, type) {
        feedbackMessage.textContent = message;
        feedbackMessage.className = `feedback-message show ${type}`;
        setTimeout(() => {
            feedbackMessage.className = 'feedback-message';
        }, 3000);
    }

    // --- Event Listeners ---

    // Character count for original text input
    originalTextInput.addEventListener('input', () => {
        const textLength = originalTextInput.value.length;
        currentCharCount.textContent = textLength;
        if (textLength > MAX_CHARS) {
            originalTextInput.value = originalTextInput.value.substring(0, MAX_CHARS);
            currentCharCount.textContent = MAX_CHARS;
            showFeedback('최대 500자까지 입력 가능합니다.', 'error');
        }
    });

    // Convert button click handler
    convertButton.addEventListener('click', async () => {
        const originalText = originalTextInput.value.trim();
        const selectedTarget = document.querySelector('input[name="target"]:checked').value;

        if (!originalText) {
            showFeedback('변환할 텍스트를 입력해주세요.', 'error');
            return;
        }

        convertButton.disabled = true;
        convertButton.textContent = '변환 중...';
        convertedTextInput.value = ''; // Clear previous result

        try {
            const response = await fetch(API_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: originalText, target: selectedTarget }),
            });

            const data = await response.json();

            if (response.ok) {
                convertedTextInput.value = data.converted_text;
                showFeedback('텍스트 변환 성공!', 'success');
            } else {
                showFeedback(`오류: ${data.error || '알 수 없는 에러가 발생했습니다.'}`, 'error');
            }
        } catch (error) {
            console.error('API 호출 중 오류 발생:', error);
            showFeedback('API 호출 중 문제가 발생했습니다. 서버를 확인해주세요.', 'error');
        } finally {
            convertButton.disabled = false;
            convertButton.textContent = '변환하기';
        }
    });

    // Copy button click handler
    copyButton.addEventListener('click', async () => {
        if (!convertedTextInput.value) {
            showFeedback('변환된 텍스트가 없습니다.', 'error');
            return;
        }

        try {
            await navigator.clipboard.writeText(convertedTextInput.value);
            showFeedback('변환된 텍스트가 클립보드에 복사되었습니다!', 'success');
        } catch (err) {
            console.error('클립보드 복사 실패:', err);
            showFeedback('클립보드 복사에 실패했습니다. 수동으로 복사해주세요.', 'error');
        }
    });

    // Initialize character count on load
    originalTextInput.dispatchEvent(new Event('input'));
});