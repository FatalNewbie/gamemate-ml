from fastapi import FastAPI, Depends
from pydantic import BaseModel
import numpy as np
from model.ml_model import load_model
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from data.database import get_db
from user.user_model import User, Genre, PlayTime

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

# 장르와 플레이 시간대 리스트 정의
genres_list = ['FPS', 'RPG', '전략', '액션', '시뮬레이션']
times_list = ['AM 9:00 ~ AM 11:00', 'AM 11:00 ~ PM 2:00', 'PM 2:00 ~ PM 5:00', 'PM 5:00 ~ PM 8:00',
              'PM 8:00 ~ PM 11:00', 'PM 11:00 ~ AM 3:00', 'AM 3:00 ~ AM 9:00']


class UserFeatures(BaseModel):
    preferred_genres: list
    play_times: list


def get_common_elements(user_features, other_features, elements):
    common_indices = np.where(np.array(user_features) * np.array(other_features))[0]
    return [elements[i] for i in common_indices]


@app.post("/recommendation")
async def predict(user_features: UserFeatures, db: Session = Depends(get_db)):
    try:
        user_data = np.hstack((user_features.preferred_genres, user_features.play_times)).reshape(1, -1)
        distances, indices = model.kneighbors(user_data)

        similar_users = indices[0][1:]
        results = []

        for idx in similar_users:
            user = db.query(User).filter(User.id == idx + 1).first()
            if user:
                common_genres = get_common_elements(user_features.preferred_genres,
                                                    [genre.id for genre in user.preferred_genres], genres_list)
                common_times = get_common_elements(user_features.play_times, [time.id for time in user.play_times],
                                                   times_list)

                user_info = {
                    "recommend_user": user.nickname,
                    "common_genre": common_genres,
                    "common_play_time": common_times
                }
                results.append(user_info)
            else:
                print(f"User with id {idx + 1} not found")

        return {"similar_users": results}
    except Exception as e:
        print(f"Error in recommendation: {str(e)}")
        return {"error": str(e)}
