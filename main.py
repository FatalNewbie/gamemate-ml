# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from starlette.middleware.cors import CORSMiddleware

from data.data import data, features, genres, times
from model.model import load_model

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # localhost:3000에서 오는 요청만 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# 모델 로드
model = load_model('model/model.pkl')

class UserFeatures(BaseModel):
    preferred_genres: list
    play_times: list

def get_common_elements(user_features, other_features, elements):
    common_indices = np.where(np.array(user_features) * np.array(other_features))[0]
    return [elements[i] for i in common_indices]

@app.post("/recommendation")
async def predict(user_features: UserFeatures):
    user_data = np.hstack((user_features.preferred_genres, user_features.play_times)).reshape(1, -1)
    distances, indices = model.kneighbors(user_data)

    similar_users = indices[0][1:]  # 첫 번째 결과는 자기 자신이므로 제외
    results = []

    for idx in similar_users:
        common_genres = get_common_elements(user_features.preferred_genres, data['preferred_genres'][idx], genres)
        common_times = get_common_elements(user_features.play_times, data['play_times'][idx], times)

        user_info = {
            "recommend_user": data['name'][idx],
            "common_genre": common_genres,
            "common_play_time": common_times
        }
        results.append(user_info)

    return {"similar_users": results}
