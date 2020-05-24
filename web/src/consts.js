const CLOTHES_CATEGORIES = [
  {
    upper: '전체',
    lower: []
  },
  {
    upper: '상의',
    lower: [
      '반팔티셔츠', '긴팔티셔츠', '반팔셔츠', '긴팔셔츠',
      '맨투맨', '터틀넥', '후드티', '니트',
      '블라우스', '끈나시', '민소매'
    ]
  },
  {
    upper: '하의',
    lower: [
      '반바지', '핫팬츠', '슬랙스', '청바지',
      '골덴바지', '트레이닝바지'
    ]
  },
  {
    upper: '치마',
    lower: [
      '미니스커트', '롱스커트'
    ]
  },
  {
    upper: '아우터',
    lower: [
      '블레이져', '숏패딩', '조끼패딩', '롱패딩',
      '야구점퍼', '항공점퍼', '바람막이', '야상',
      '무스탕', '코트', '트랙탑', '가죽자켓',
      '청자켓', '가디건'
    ]
  },
  {
    upper: '한벌옷',
    lower: [
      '원피스'
    ]
  }
]

const CODY_CATEGORIES = [
  {
    upper: '스타일',
    lower: [
      '심플', '스트릿', '화려', '데이트', '정장'
    ]
  },
  {
    upper: '리뷰',
    lower: [
      '등록'
    ]
  }
]
const SERVER_BASE_URL = 'http://localhost:8000'

export default {
  CLOTHES_CATEGORIES,
  CODY_CATEGORIES,
  SERVER_BASE_URL
}
