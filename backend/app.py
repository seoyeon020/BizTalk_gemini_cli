import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

@app.route('/api/convert', methods=['POST'])
def convert_message():
    print("API /api/convert called.") # 추가
    # 1. 함수 내부에서 키를 가져와야 배포 시 가장 안전합니다.
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("ERROR: GROQ_API_KEY not found in environment variables.") # 추가
        return jsonify({"error": "GROQ_API_KEY not found."}), 500
    print("GROQ_API_KEY successfully retrieved.") # 추가

    data = request.get_json()
    if data is None: # JSON 파싱 실패 시 처리 추가
        print("ERROR: Request body is not valid JSON.")
        return jsonify({"error": "Request body must be JSON."}), 400

    keywords = data.get('keywords')
    persona = data.get('persona')

    if not keywords or not persona:
        print(f"ERROR: Missing keywords({keywords}) or persona({persona}) in request.") # 추가
        return jsonify({"error": "Missing keywords or persona in request."}), 400
    print(f"Keywords: '{keywords}', Persona: '{persona}' received.") # 추가

    # 페르소나 매칭 (상사, 타팀 동료, 고객 값에 대응)
    # JS에서 보내는 값에 따라 매핑해줍니다.
    persona_instructions = {
        "upward": "상사에게 적합한 정중하고 전문적인 비즈니스 메시지로 변환해주세요. 결론부터 시작하세요.",
        "lateral": "동료에게 적합한 친절하고 협력적인 메시지로 변환해주세요.",
        "external": "외부 고객에게 적합한 극존칭과 신뢰를 강조한 메시지로 변환해주세요."
    }

    system_prompt = persona_instructions.get(persona, persona_instructions["lateral"])
    user_message = f"Convert this message: '{keywords}'"
    print(f"System Prompt: '{system_prompt}'") # 추가
    print(f"User Message for Groq: '{user_message}'") # 추가

    try:
        # 클라이언트를 여기서 생성 (서버리스 환경 최적화)
        print("Attempting to create Groq client.") # 추가
        client = Groq(api_key=api_key)
        print("Groq client created. Attempting chat completion.") # 추가
        
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=300,
        )
        print("Chat completion successful.") # 추가

        converted_message = chat_completion.choices[0].message.content
        print(f"Converted message: '{converted_message[:50]}...'") # 추가 (너무 길면 자름)
        return jsonify({"converted_message": converted_message})

    except Exception as e:
        print(f"ERROR: Exception during Groq API call: {e}") # 추가
        return jsonify({"error": str(e)}), 500

# 정적 파일 서빙은 vercel.json 설정에 맡기는 것이 좋습니다.
if __name__ == '__main__':
    app.run(debug=True, port=5000)