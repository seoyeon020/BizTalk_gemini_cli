import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

app = Flask(__name__, static_folder='../frontend', static_url_path='/')
# 프론트엔드からの 모든 출처에서의 요청을 허용
CORS(app) 

# Groq 클라이언트 초기화
# API 키는 환경 변수 'GROQ_API_KEY'에서 자동으로 로드됩니다.
groq_client = None # Initialize groq_client
original_http_proxy = None
original_https_proxy = None
original_no_proxy = None

try:
    # Temporarily remove proxy environment variables that might interfere with Groq client initialization
    original_http_proxy = os.environ.pop('HTTP_PROXY', None)
    original_https_proxy = os.environ.pop('HTTPS_PROXY', None)
    original_no_proxy = os.environ.pop('NO_PROXY', None)

    groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    print("Groq client initialized successfully.")

except Exception as e:
    print(f"Error initializing Groq client: {e}")

finally:
    # Restore proxy environment variables if they existed
    if original_http_proxy is not None:
        os.environ['HTTP_PROXY'] = original_http_proxy
    if original_https_proxy is not None:
        os.environ['HTTPS_PROXY'] = original_https_proxy
    if original_no_proxy is not None:
        os.environ['NO_PROXY'] = original_no_proxy

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
    Sprint 1에서는 실제 변환 로직 대신 더미 데이터를 반환합니다.
    """
    data = request.json
    original_text = data.get('text')
    target = data.get('target')

    if not original_text or not target:
        return jsonify({"error": "텍스트와 변환 대상은 필수입니다."}), 400

    if target not in PROMPT_TEMPLATES:
        return jsonify({"error": "유효하지 않은 변환 대상입니다."}), 400

    # 적절한 프롬프트 템플릿 선택
    prompt = PROMPT_TEMPLATES[target].format(text=original_text)

    if groq_client is None:
        return jsonify({"error": "Groq API 클라이언트가 초기화되지 않았습니다. API 키를 확인해주세요."}), 500

    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="moonshotai/kimi-k2-instruct-0905",
            temperature=0.7, # 텍스트 생성의 다양성을 조절
            max_tokens=500, # 생성될 최대 토큰 수
        )
        converted_text = chat_completion.choices[0].message.content
        
        response_data = {
            "original_text": original_text,
            "converted_text": converted_text,
            "target": target
        }
        
        return jsonify(response_data)

    except Exception as e:
        print(f"Groq API 호출 중 오류 발생: {e}")
        return jsonify({"error": f"텍스트 변환 중 오류가 발생했습니다: {e}"}), 500

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)