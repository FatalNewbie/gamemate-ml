from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pickle

app = FastAPI()

# 예시 데이터
data = {
    'user_id': [1, 2, 3, 4, 5],
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'age': [25, 30, 22, 35, 28],
    'gender': ['F', 'M', 'M', 'M', 'F'],
    'preferred_genres': [
        [1, 0, 1, 0, 1],  # Alice
        [0, 1, 0, 1, 0],  # Bob
        [1, 1, 0, 0, 1],  # Charlie
        [0, 0, 1, 1, 0],  # David
        [1, 1, 1, 0, 0]  # Eve
    ],
    'play_times': [
        [1, 0, 0, 0, 0, 1, 1],  # Alice: 오전
        [0, 1, 1, 0, 0, 0, 0],  # Bob: 오후
        [1, 1, 0, 0, 1, 0, 0],  # Charlie: 밤
        [0, 0, 0, 1, 1, 1, 0],  # David: 저녁
        [1, 1, 0, 1, 0, 0, 0]  # Eve: 새벽
    ]
}

genres = ['FPS', 'RPG', '전략', '액션', '시뮬레이션']
times = ['AM 9:00 ~ AM 11:00', 'AM 11:00 ~ PM 2:00', 'PM 2:00 ~ PM 5:00', 'PM 5:00 ~ PM 8:00', 'PM 8:00 ~ PM 11:00',
         'PM 11:00 ~ AM 3:00', 'AM 3:00 ~ AM 9:00']

# 특징 벡터 생성
features = np.hstack((data['preferred_genres'], data['play_times']))

# 모델 로드
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)


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
            "추천 유저": data['name'][idx],
            "공통 장르": common_genres,
            "공통 게임 시간대": common_times
        }
        results.append(user_info)

    return {"similar_users": results}
