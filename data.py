# data/data.py
import numpy as np

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
