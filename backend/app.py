import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
# from groq import Groq

# .env 파일에서 환경 변수 로드
load_dotenv()

app = Flask(__name__)
# 모든 도메인에서의 요청을 허용하도록 CORS 설정
CORS(app)

# Groq 클라이언트 초기화 (Sprint 3에서 실제 사용)
# client = Groq(
#     api_key=os.environ.get("GROQ_API_KEY"),
# )

@app.route('/')
def health_check():
    """헬스 체크를 위한 기본 엔드포인트"""
    return jsonify({"status": "ok", "message": "BizTone Converter API is running."})

@app.route('/api/convert', methods=['POST'])
def convert_tone():
    """
    텍스트 변환을 처리하는 메인 API 엔드포인트.
    Sprint 1에서는 더미(dummy) 데이터를 반환합니다.
    """
    try:
        # 클라이언트로부터 데이터 수신 (Sprint 3에서 사용 예정)
        # data = request.get_json()
        # text = data.get('text')
        # target = data.get('target')

        # Sprint 1: 더미 응답 생성
        dummy_response = "이것은 Sprint 1의 더미 응답입니다. API 연동이 성공적으로 확인되었습니다."
        
        return jsonify({"converted_text": dummy_response})

    except Exception as e:
        # 오류 발생 시 로그를 남기고 500 에러를 반환합니다.
        app.logger.error(f"An error occurred: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    # 디버그 모드로 Flask 앱 실행
    app.run(debug=True, port=5000)
