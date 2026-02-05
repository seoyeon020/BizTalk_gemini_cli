document.addEventListener('DOMContentLoaded', () => {
    const convertBtn = document.getElementById('convert-button');
    const copyBtn = document.getElementById('copy-button');
    const keywordInput = document.getElementById('original-text'); // ID 변경
    const resultOutput = document.getElementById('converted-text'); // ID 변경
    const currentCharCount = document.getElementById('current-char-count'); // 글자 수 카운터 엘리먼트 추가

    const MAX_LENGTH = 500; // 최대 글자 수 상수 정의

    // 글자 수 카운터 업데이트 함수
    const updateCharCount = () => {
        const currentLength = keywordInput.value.length;
        currentCharCount.textContent = currentLength;
        if (currentLength > MAX_LENGTH) {
            currentCharCount.style.color = 'red';
            convertBtn.disabled = true; // 최대 글자 수 초과 시 변환 버튼 비활성화
        } else {
            currentCharCount.style.color = '';
            convertBtn.disabled = false; // 최대 글자 수 이내일 때 변환 버튼 활성화
        }
    };

    // 초기 글자 수 설정 및 input 이벤트 리스너 추가
    if (keywordInput) {
        updateCharCount(); // 페이지 로드 시 초기 글자 수 설정
        keywordInput.addEventListener('input', updateCharCount);
    }
    
    // Convert button click event
    convertBtn.addEventListener('click', async () => {
        const keywords = keywordInput.value.trim();
        const selectedPersona = document.querySelector('input[name="target"]:checked').value; // name 변경

        if (!keywords) {
            alert('핵심 키워드를 입력해주세요.');
            keywordInput.focus();
            return;
        }

        // 입력 글자 수 제한 확인
        if (keywords.length > MAX_LENGTH) {
            alert(`입력 가능한 최대 글자 수는 ${MAX_LENGTH}자 입니다. 현재 ${keywords.length}자 입력되었습니다.`);
            return;
        }

        // Start loading state
        resultOutput.classList.add('loading');
        resultOutput.value = 'AI가 메시지를 생성 중입니다. 잠시만 기다려주세요...'; // textarea에 직접 값 설정
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
            resultOutput.value = data.converted_message; // textarea에 직접 값 설정

        } catch (error) {
            console.error('Error:', error);
            resultOutput.value = `오류가 발생했습니다: ${error.message}. 잠시 후 다시 시도해주세요.`; // textarea에 직접 값 설정
        } finally {
            // End loading state
            resultOutput.classList.remove('loading');
            convertBtn.disabled = false;
            copyBtn.disabled = false; // Re-enable copy button
        }
    });

    // Copy button click event
    copyBtn.addEventListener('click', () => {
        const textToCopy = resultOutput.value; // textarea의 value 속성 사용
        // Check if there's text to copy and if it's not the loading message
        if (textToCopy && textToCopy !== '변환 버튼을 누르면 결과가 여기에 표시됩니다.' && textToCopy !== 'AI가 메시지를 생성 중입니다. 잠시만 기다려주세요...' && !resultOutput.classList.contains('loading')) {
            navigator.clipboard.writeText(textToCopy)
                .then(() => {
                    // alert('메시지가 클립보드에 복사되었습니다.');
                    // 피드백 메시지 표시
                    const feedbackMessage = document.getElementById('feedback-message');
                    if (feedbackMessage) {
                        feedbackMessage.textContent = '메시지가 클립보드에 복사되었습니다!';
                        feedbackMessage.style.opacity = '1';
                        setTimeout(() => {
                            feedbackMessage.style.opacity = '0';
                            feedbackMessage.textContent = '';
                        }, 2000);
                    }
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