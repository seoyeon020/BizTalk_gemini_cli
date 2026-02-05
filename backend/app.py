import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__, static_folder='../frontend', static_url_path='/')
# 모든 출처에서의 요청을 허용 (Vercel 배포 시 필요)
CORS(app)

# 대상별 프롬프트 템플릿 정의
PROMPT_TEMPLATES = {
    "상사": "당신은 상사에게 보고하는 비즈니스 문서 작성 전문가입니다. 다음 내용을 정중한 격식체로, 결론부터 명확하게 제시하는 보고 형식으로 변환해주세요:\n\n원본: {text}\n변환:",
    "타팀 동료": "당신은 타팀 동료와 협업하는 비즈니스 커뮤니케이션 전문가입니다. 다음 내용을 친절하고 상호 존중하는 어투로, 요청 사항과 마감 기한을 명확히 전달하는 협조 요청 형식으로 변환해주세요:\n\n원본: {text}\n변환:",
    "고객": "당신은 고객 응대 비즈니스 커뮤니케이션 전문가입니다. 다음 내용을 극존칭을 사용하고, 전문성과 서비스 마인드를 강조하는 안내, 공지, 사과 등의 목적에 부합하는 형식으로 변환해주세요:\n\n원본: {text}\n변환:"
}

@app.route('/api/convert', methods=['POST'])
def convert_text():
    """
    텍스트 변환을 위한 API 엔드포인트.
    """
    # 1. 환경 변수에서 API 키를 함수 실행 시점에 가져옵니다. (Vercel 최적화)
    api_key = os.environ.get("GROQ_API_KEY")
    
    if not api_key:
        return jsonify({"error": "서버 설정에서 GROQ_API_KEY를 찾을 수 없습니다. Vercel 환경변수를 확인하세요."}), 500

    data = request.json
    original_text = data.get('text')
    target = data.get('target')

    # 데이터 유효성 검사
    if not original_text or not target:
        return jsonify({"error": "텍스트와 변환 대상은 필수입니다."}), 400

    if target not in PROMPT_TEMPLATES:
        return jsonify({"error": "유효하지 않은 변환 대상입니다."}), 400

    # 프롬프트 구성
    prompt = PROMPT_TEMPLATES[target].format(text=original_text)

    try:
        # 2. 요청이 들어올 때마다 클라이언트를 생성합니다.
        client = Groq(api_key=api_key)
        
        # 3. Groq 공식 지원 모델명을 사용합니다.
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
        print(f"Groq API 호출 중 오류 발생: {e}")
        # 에러 내용을 구체적으로 반환하여 디버깅을 돕습니다.
        return jsonify({"error": f"텍스트 변환 중 오류가 발생했습니다: {str(e)}"}), 500

@app.route('/')
def index():
    # frontend 폴더 안의 index.html을 서빙합니다.
    return app.send_static_file('index.html')

if __name__ == '__main__':
    # 로컬 테스트용 설정
    app.run(debug=True, port=5000)