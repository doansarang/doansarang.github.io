# 도안사랑교회 홈페이지

대전 유성구 원신흥동 도안사랑교회 홈페이지입니다. GitHub Pages로 운영합니다.

## 구성

| 주소 | 내용 |
| --- | --- |
| `/` | 대문 (교회소개 영상, 목사님 영상 프로필, 모바일 바로가기) |
| `/welcome/` `/vision/` `/churchtime/` `/directions/` | 교회소개 (인사말, 비전, 예배시간, 오시는 길) |
| `/missionization/` | 사랑의 선교지 |
| `/album/` | 선교&전도 앨범 |
| `/story/` | 사랑이야기 |

사랑의말씀 메뉴(설교모음, J안나방송)는 유튜브 채널로 연결됩니다.

## 내용 고치는 법

페이지 HTML은 `_build/build.py`가 `_build/content.json`을 읽어서 만듭니다.
글, 영상, 앨범을 바꿀 때는 `content.json`을 고친 뒤 아래 명령으로 다시 만듭니다.

```
python3 _build/build.py
```

- 사진: `assets/img/album/<글번호>/`, 앨범 목록 썸네일은 `assets/img/thumbs/<글번호>.jpg`
- 인사말 등 이미지 페이지: `assets/img/pages/`
- 디자인: `assets/css/style.css`

2026년 11월, 기존 Rhymix 홈페이지(doansarang.com)의 내용과 디자인을 옮겨 만들었습니다.

## 글꼴

- 제목, 성경 구절: **고운 바탕**(류양희, SIL OFL 1.1)
- 본문, 메뉴: **Pretendard**(길형진, SIL OFL 1.1)

둘 다 jsDelivr에서 필요한 글자 묶음만 불러옵니다. 상업적 사용, 웹 임베딩이 무료로 허용되며 글꼴 파일 자체를 판매하는 것만 금지됩니다.

## 행사 홍보 (대문 알림)

큰 행사가 있으면 대문 맨 위(예배 안내 바로 위)에 포스터와 안내가 나옵니다.

1. 포스터 그림을 `assets/img/events/`에 넣습니다. 큰 그림(원본)과 가로 720px짜리 작은 그림 두 개를 둡니다.
2. `_build/content.json`의 `events`에 한 칸을 추가합니다.

```json
{
  "label": "특별초청예배",
  "title": "인공지능과 신앙",
  "lead": "한두 줄 소개",
  "date": "2026-11-22",
  "when": "11월 22일(주일) 오전 10시 50분",
  "place": "도안사랑교회 본당",
  "people": [["말씀", "장순흥 총장"], ["특별찬양", "김신의 가수"]],
  "poster": "/assets/img/events/파일.jpg",
  "poster_small": "/assets/img/events/파일-720.jpg",
  "poster_size": [1086, 1448],
  "story": 2
}
```

- `date`가 지나면 대문에서 저절로 사라집니다(한국 시간 기준). 지운 뒤 다시 올릴 필요가 없습니다.
- 30일 안으로 다가오면 "D-3", 당일에는 "오늘" 표시가 붙습니다.
- `story`에 사랑이야기 글 번호를 적으면 "안내 글 보기" 단추가 생깁니다. 사랑이야기 글에는 `images`(본문 사진)와 `og_image`(카톡 공유 그림, 1200×630)를 넣을 수 있습니다.
