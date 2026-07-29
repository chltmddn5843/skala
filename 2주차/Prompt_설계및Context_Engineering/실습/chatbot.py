from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()    

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "당신은 냉철하고 객관적인 AI 데이터 분석가입니다.앞으로 응답은 짧고 간결해줘"},
        {"role": "user",
          "content": "StandardScaler와 MinMaxScaler의 차이점과 적합한 데이터 분포를 간단히 비교해줘."}
    ],
    temperature=0.2,   # 일관성 있는 답변을 위해 낮게 설정
    max_tokens=800
)

print(response.choices[0].message.content)