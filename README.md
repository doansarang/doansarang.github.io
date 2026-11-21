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
