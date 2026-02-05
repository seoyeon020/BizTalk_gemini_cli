import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
# 모든 도메인에서의 요청을 허용 (Vercel 환경 필수)
CORS(app)

# 대상별 프롬프트 템플릿
PROMPT_TEMPLATES = {
    "상사": "당신은 상사에게 보고하는 비즈니스 문서 작성 전문가입니다. 다음 내용을 정중한 격식체로, 결론부터 명확하게 제시하는 보고 형식으로 변환해주세요:\n\n원본: {text}\n변환:",
    "타팀 동료": "당신은 타팀 동료와 협업하는 비즈니스 커뮤니케이션 전문가입니다. 다음 내용을 친절하고 상호 존중하는 어투로, 요청 사항과 마감 기한을 명확히 전달하는 협조 요청 형식으로 변환해주세요:\n\n원본: {text}\n변환:",
    "고객": "당신은 고객 응대 비즈니스 커뮤니케이션 전문가입니다. 다음 내용을 극존칭을 사용하고, 전문성과 서비스 마인드를 강조하는 안내, 공지, 사과 등의 목적에 부합하는 형식으로 변환해주세요:\n\n원본: {text}\n변환:"
}

@app.route('/api/convert', methods=['POST'])
def convert_text():
    # 1. 환경 변수에서 API 키 로드
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return jsonify({"error": "Vercel 환경변수에 GROQ_API_KEY가 설정되지 않았습니다."}), 500

    # 2. 클라이언트 요청 데이터 수신
    data = request.json
    if not data:
        return jsonify({"error": "데이터가 전송되지 않았습니다."}), 400

    original_text = data.get('text')
    target = data.get('target')

    if not original_text or not target:
        return jsonify({"error": "텍스트와 변환 대상은 필수입니다."}), 400

    if target not in PROMPT_TEMPLATES:
        return jsonify({"error": "유효하지 않은 변환 대상입니다."}), 400

    # 3. 프롬프트 생성 및 Groq 호출
    prompt = PROMPT_TEMPLATES[target].format(text=original_text)

    try:
        # 불필요한 인자 없이 가장 기본적으로 초기화 (proxies 에러 방지)
        client = Groq(api_key=api_key)

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=500,
        )
        
        converted_text = chat_completion.choices[0].message.content
        
        return jsonify({
            "original_text": original_text,
            "converted_text": converted_text,
            "target": target
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"변환 중 오류 발생: {str(e)}"}), 500

# Vercel은 이 루트 경로 설정을 무시할 수 있으므로 vercel.json과 병행 사용하세요.
@app.route('/')
def index():
    return "Backend is running!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)