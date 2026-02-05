import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

@app.route('/api/convert', methods=['POST'])
def convert_message():
    # 1. 함수 내부에서 키를 가져와야 배포 시 가장 안전합니다.
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return jsonify({"error": "GROQ_API_KEY not found."}), 500

    data = request.get_json()
    keywords = data.get('keywords')
    persona = data.get('persona')

    if not keywords or not persona:
        return jsonify({"error": "Missing keywords or persona in request."}), 400

    # 페르소나 매칭 (상사, 타팀 동료, 고객 값에 대응)
    # JS에서 보내는 값에 따라 매핑해줍니다.
    persona_instructions = {
        "upward": "상사에게 적합한 정중하고 전문적인 비즈니스 메시지로 변환해주세요. 결론부터 시작하세요.",
        "lateral": "동료에게 적합한 친절하고 협력적인 메시지로 변환해주세요.",
        "external": "외부 고객에게 적합한 극존칭과 신뢰를 강조한 메시지로 변환해주세요."
    }

    # 만약 JS에서 보내는 값이 '상사', '고객' 형태라면 아래처럼 처리하세요.
    # system_prompt = persona_instructions.get(persona, "정중한 비즈니스 메시지로 변환해주세요.")

    system_prompt = persona_instructions.get(persona, persona_instructions["lateral"])
    user_message = f"Convert this message: '{keywords}'"

    try:
        # 클라이언트를 여기서 생성 (서버리스 환경 최적화)
        client = Groq(api_key=api_key)
        
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            # [알림] 아래 모델명은 Groq 공식 지원 모델입니다. 
            # 지원되지 않는 모델명 사용 시 401/404 에러가 발생하므로 수정했습니다.
            model="llama-3.3-70b-versatile", 
            temperature=0.7,
            max_tokens=300,
        )

        converted_message = chat_completion.choices[0].message.content
        return jsonify({"converted_message": converted_message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 정적 파일 서빙은 vercel.json 설정에 맡기는 것이 좋습니다.
if __name__ == '__main__':
    app.run(debug=True, port=5000)