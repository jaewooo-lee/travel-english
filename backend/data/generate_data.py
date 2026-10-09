import json
import os

# 100일간의 여행 영어 다이얼로그 및 핵심 표현 생성 스크립트
# 10개 테마 * 10일 = 100일치 데이터 구성

days_data = []

# 테마 정의
themes = [
    "기내 및 공항 (In-flight & Airport)",      # Day 1 - 10
    "교통수단 이용 (Transportation)",          # Day 11 - 20
    "호텔 및 숙소 (Hotel & Accommodations)",   # Day 21 - 30
    "식당 및 카페 (Restaurants & Cafes)",      # Day 31 - 40
    "길 찾기 및 위치 (Directions & Location)",   # Day 41 - 50
    "쇼핑 및 면세점 (Shopping & Duty Free)",    # Day 51 - 60
    "관광 및 매표소 (Sightseeing & Tickets)",   # Day 61 - 70
    "문제 및 긴급 상황 (Trouble & Emergencies)", # Day 71 - 80
    "일상 대화 및 친교 (Socializing & Chatting)",# Day 81 - 90
    "귀국 및 면세 신고 (Departure & Customs)"    # Day 91 - 100
]

# 100일 시나리오 원본 데이터 정의
scenarios = {
    # 테마 1: 기내 및 공항 (1~10)
    1: {
        "title": "기내 좌석 찾기",
        "dialogue": [
            {"role": "Passenger", "korean": "실례합니다, 제 좌석이 어디인지 알려주실 수 있나요?", "english": "Excuse me, could you tell me where my seat is?"},
            {"role": "Flight Attendant", "korean": "물론입니다. 탑승권을 보여주시겠어요?", "english": "Of course. May I see your boarding pass?"},
            {"role": "Passenger", "korean": "여기 있습니다. 24A 좌석이에요.", "english": "Here it is. It's seat 24A."},
            {"role": "Flight Attendant", "korean": "이쪽 통로로 쭉 가시면 왼쪽에 있습니다.", "english": "Go straight down this aisle, and it's on your left."}
        ],
        "expressions": [
            {"korean": "탑승권", "english": "boarding pass"},
            {"korean": "통로 좌석 / 창가 좌석", "english": "aisle seat / window seat"},
            {"korean": "담요 하나만 더 주시겠어요?", "english": "Could I get another blanket?"}
        ]
    },
    2: {
        "title": "기내식 및 음료 주문",
        "dialogue": [
            {"role": "Flight Attendant", "korean": "소고기와 닭고기 중 어떤 것으로 하시겠습니까?", "english": "Would you like beef or chicken?"},
            {"role": "Passenger", "korean": "소고기로 주세요. 그리고 마실 것은 무엇이 있나요?", "english": "Beef, please. And what do you have to drink?"},
            {"role": "Flight Attendant", "korean": "물, 주스, 콜라, 와인, 맥주가 있습니다.", "english": "We have water, juice, soda, wine, and beer."},
            {"role": "Passenger", "korean": "오렌지 주스로 부탁드립니다.", "english": "Orange juice, please."}
        ],
        "expressions": [
            {"korean": "기내식", "english": "in-flight meal"},
            {"korean": "어떤 것으로 하시겠습니까?", "english": "Which one would you like?"},
            {"korean": "소고기로 주세요", "english": "Beef, please"}
        ]
    },
    3: {
        "title": "기내 온도 및 불편사항 해결",
        "dialogue": [
            {"role": "Passenger", "korean": "실례합니다, 기내가 조금 추운데요. 담요 한 장 더 받을 수 있을까요?", "english": "Excuse me, it's a bit cold in here. Can I get another blanket?"},
            {"role": "Flight Attendant", "korean": "네, 바로 가져다 드리겠습니다. 다른 필요하신 것은 없으신가요?", "english": "Sure, I'll bring you one right away. Anything else you need?"},
            {"role": "Passenger", "korean": "제 좌석 스크린이 작동하지 않아요. 확인해 주시겠어요?", "english": "My seat screen is not working. Could you check it?"},
            {"role": "Flight Attendant", "korean": "불편을 드려 죄송합니다. 시스템을 재부팅해 드리겠습니다.", "english": "I'm sorry for the inconvenience. I will reboot the system for you."}
        ],
        "expressions": [
            {"korean": "담요", "english": "blanket"},
            {"korean": "불편을 드려 죄송합니다", "english": "Sorry for the inconvenience"},
            {"korean": "스크린이 작동하지 않아요", "english": "The screen is not working"}
        ]
    },
    4: {
        "title": "입국 신고서 작성",
        "dialogue": [
            {"role": "Passenger", "korean": "이 입국 신고서는 어떻게 작성해야 하나요?", "english": "How do I fill out this arrival card?"},
            {"role": "Flight Attendant", "korean": "여권 정보와 체류하실 호텔 주소를 영어로 적으시면 됩니다.", "english": "You need to write your passport details and your hotel address in English."},
            {"role": "Passenger", "korean": "펜을 빌릴 수 있을까요?", "english": "Could I borrow a pen?"},
            {"role": "Flight Attendant", "korean": "여기 있습니다. 작성 후 여권과 함께 보관해 주세요.", "english": "Here you go. Keep it with your passport after filling it out."}
        ],
        "expressions": [
            {"korean": "입국 신고서", "english": "arrival card / immigration form"},
            {"korean": "~을 작성하다", "english": "fill out"},
            {"korean": "펜을 빌리다", "english": "borrow a pen"}
        ]
    },
    5: {
        "title": "입국 심사 (목적 및 기간)",
        "dialogue": [
            {"role": "Immigration Officer", "korean": "방문 목적이 무엇인가요?", "english": "What is the purpose of your visit?"},
            {"role": "Passenger", "korean": "관광입니다. 휴가로 왔어요.", "english": "Sightseeing. I'm here on vacation."},
            {"role": "Immigration Officer", "korean": "얼마나 머무실 예정입니까?", "english": "How long will you be staying?"},
            {"role": "Passenger", "korean": "일주일 동안 머물 예정입니다. 여기 왕복 항공권입니다.", "english": "I will stay for one week. Here is my return ticket."}
        ],
        "expressions": [
            {"korean": "방문 목적", "english": "purpose of visit"},
            {"korean": "휴가 중", "english": "on vacation"},
            {"korean": "왕복 항공권", "english": "round-trip ticket"}
        ]
    },
    6: {
        "title": "수하물 수령 및 분실",
        "dialogue": [
            {"role": "Passenger", "korean": "서울발 KE081편의 수하물 수령대는 어디인가요?", "english": "Where is the baggage carousel for flight KE081 from Seoul?"},
            {"role": "Airport Staff", "korean": "5번 수하물 수령대로 가시면 됩니다.", "english": "You should go to baggage carousel number 5."},
            {"role": "Passenger", "korean": "제 가방이 나오지 않았어요. 어디서 신고해야 하죠?", "english": "My bag didn't come out. Where can I report it?"},
            {"role": "Airport Staff", "korean": "저쪽 분실물 센터(Baggage Claim Service) 데스크로 가세요.", "english": "Go to the Baggage Claim Service desk over there."}
        ],
        "expressions": [
            {"korean": "수하물 수령대", "english": "baggage carousel / baggage claim"},
            {"korean": "가방이 안 나왔어요", "english": "My bag didn't come out"},
            {"korean": "분실물 센터", "english": "lost and found / baggage claim service"}
        ]
    },
    7: {
        "title": "세관 신고",
        "dialogue": [
            {"role": "Customs Officer", "korean": "신고할 물건이 있으십니까?", "english": "Do you have anything to declare?"},
            {"role": "Passenger", "korean": "아니요, 없습니다. 모두 개인 소지품입니다.", "english": "No, I don't. Everything is for my personal use."},
            {"role": "Customs Officer", "korean": "가방을 이 엑스레이 검색대에 올려주세요.", "english": "Please put your bags on this X-ray scanner."},
            {"role": "Passenger", "korean": "네, 알겠습니다.", "english": "Sure, no problem."}
        ],
        "expressions": [
            {"korean": "신고할 물건", "english": "anything to declare"},
            {"korean": "개인 사용 용도", "english": "personal use"},
            {"korean": "세관", "english": "customs"}
        ]
    },
    8: {
        "title": "환전 및 유심 구매",
        "dialogue": [
            {"role": "Passenger", "korean": "달러를 유로로 환전하고 싶습니다. 수수료는 얼마인가요?", "english": "I'd like to exchange dollars into euros. What is the commission fee?"},
            {"role": "Clerk", "korean": "수수료는 2%입니다. 여권을 보여주시겠어요?", "english": "The commission is 2%. May I see your passport, please?"},
            {"role": "Passenger", "korean": "네, 여기요. 그리고 여행자용 SIM 카드도 판매하나요?", "english": "Yes, here it is. And do you also sell SIM cards for tourists?"},
            {"role": "Clerk", "korean": "네, 데이터 무제한 7일권이 20유로입니다.", "english": "Yes, a 7-day unlimited data card is 20 euros."}
        ],
        "expressions": [
            {"korean": "환전하다", "english": "exchange money"},
            {"korean": "수수료", "english": "commission fee / transaction fee"},
            {"korean": "여행자용 SIM 카드", "english": "tourist SIM card"}
        ]
    },
    9: {
        "title": "공항 안내소 문의",
        "dialogue": [
            {"role": "Passenger", "korean": "실례합니다, 시내 지도를 한 장 얻을 수 있을까요?", "english": "Excuse me, can I get a city map?"},
            {"role": "Information Staff", "korean": "네, 여기 시내 지도와 지하철 노선도입니다.", "english": "Sure, here is a city map and a subway map."},
            {"role": "Passenger", "korean": "공항 철도 타는 곳은 어디인지 알려주시겠어요?", "english": "Could you tell me where to take the airport train?"},
            {"role": "Information Staff", "korean": "에스컬레이터를 타고 지하 1층으로 내려가시면 바로 보입니다.", "english": "Take the escalator down to the B1 level, and you will see it right away."}
        ],
        "expressions": [
            {"korean": "시내 지도", "english": "city map"},
            {"korean": "공항 철도", "english": "airport train / airport express"},
            {"korean": "안내 데스크", "english": "information desk"}
        ]
    },
    10: {
        "title": "공항 버스/택시 승강장 찾기",
        "dialogue": [
            {"role": "Passenger", "korean": "시내로 가는 공항버스 매표소는 어디인가요?", "english": "Where is the ticket office for the airport bus to the city center?"},
            {"role": "Airport Staff", "korean": "4번 출구 밖에 매표기와 승강장이 있습니다.", "english": "There are ticket machines and bus stops just outside exit 4."},
            {"role": "Passenger", "korean": "택시 승강장은 어디에 있나요?", "english": "Where is the taxi stand?"},
            {"role": "Airport Staff", "korean": "3번 출구로 나가서 횡단보도를 건너면 택시들이 대기하고 있습니다.", "english": "Exit through gate 3, cross the crosswalk, and taxis are waiting there."}
        ],
        "expressions": [
            {"korean": "시내 중심가", "english": "city center / downtown"},
            {"korean": "택시 승강장", "english": "taxi stand / taxi rank"},
            {"korean": "매표기", "english": "ticket machine"}
        ]
    },

    # 테마 2: 교통수단 이용 (11~20)
    11: {
        "title": "택시 호출 및 목적지 말하기",
        "dialogue": [
            {"role": "Passenger", "korean": "힐튼 호텔로 가주세요. 얼마나 걸리나요?", "english": "To the Hilton Hotel, please. How long will it take?"},
            {"role": "Driver", "korean": "교통 체증이 없다면 20분 정도 걸립니다.", "english": "It will take about 20 minutes if there is no traffic."},
            {"role": "Passenger", "korean": "제가 비행기 시간이 촉박해서 그런데, 조금 빨리 가주실 수 있나요?", "english": "I'm in a hurry for my flight, so could you go a bit faster?"},
            {"role": "Driver", "korean": "안전하게 최대한 빨리 가보겠습니다.", "english": "I'll do my best to get there as quickly and safely as possible."}
        ],
        "expressions": [
            {"korean": "교통 체증", "english": "traffic jam / heavy traffic"},
            {"korean": "서두르다", "english": "in a hurry"},
            {"korean": "최대한 빨리", "english": "as quickly as possible"}
        ]
    },
    12: {
        "title": "택시 요금 지불 및 잔돈",
        "dialogue": [
            {"role": "Driver", "korean": "도착했습니다. 요금은 25달러입니다.", "english": "We've arrived. The fare is 25 dollars."},
            {"role": "Passenger", "korean": "신용카드로 결제해도 되나요?", "english": "Can I pay by credit card?"},
            {"role": "Driver", "korean": "죄송하지만 현금만 받습니다.", "english": "Sorry, I only take cash."},
            {"role": "Passenger", "korean": "여기 30달러 있습니다. 거스름돈은 괜찮습니다.", "english": "Here is 30 dollars. Keep the change."}
        ],
        "expressions": [
            {"korean": "택시 요금", "english": "taxi fare"},
            {"korean": "카드로 결제하다", "english": "pay by credit card"},
            {"korean": "잔돈은 가지세요", "english": "Keep the change"}
        ]
    },
    13: {
        "title": "지하철 매표소 이용",
        "dialogue": [
            {"role": "Passenger", "korean": "센트럴 파크로 가려면 어떤 티켓을 사야 하나요?", "english": "Which ticket should I buy to go to Central Park?"},
            {"role": "Clerk", "korean": "1회권이나 하루 정기권을 구매하실 수 있습니다.", "english": "You can buy a single-ride ticket or a 1-day pass."},
            {"role": "Passenger", "korean": "1회권은 얼마인가요?", "english": "How much is a single-ride ticket?"},
            {"role": "Clerk", "korean": "3달러입니다. 매표기에서 구매하실 수 있어요.", "english": "It's 3 dollars. You can purchase it at the ticket machine."}
        ],
        "expressions": [
            {"korean": "1회권", "english": "single-ride ticket / one-way ticket"},
            {"korean": "1일권(정기권)", "english": "1-day pass"},
            {"korean": "지하철 노선도", "english": "subway map"}
        ]
    },
    14: {
        "title": "버스 노선 및 하차역 확인",
        "dialogue": [
            {"role": "Passenger", "korean": "이 버스가 미술관(Museum)으로 가나요?", "english": "Does this bus go to the art museum?"},
            {"role": "Driver", "korean": "네, 갑니다. 다섯 정거장 후에 내리시면 돼요.", "english": "Yes, it does. You need to get off after five stops."},
            {"role": "Passenger", "korean": "도착하면 말씀해 주시겠어요?", "english": "Could you let me know when we get there?"},
            {"role": "Driver", "korean": "네, 걱정 마세요. 도착하면 알려드릴게요.", "english": "Sure, don't worry. I'll tell you when we arrive."}
        ],
        "expressions": [
            {"korean": "버스 정류장", "english": "bus stop"},
            {"korean": "버스에서 내리다", "english": "get off the bus"},
            {"korean": "알려주다", "english": "let me know / tell me"}
        ]
    },
    15: {
        "title": "기차역 플랫폼 및 티켓",
        "dialogue": [
            {"role": "Passenger", "korean": "런던행 다음 기차는 몇 시에 출발하나요?", "english": "What time does the next train to London leave?"},
            {"role": "Clerk", "korean": "오후 2시 15분에 출발합니다. 티켓을 예약하시겠습니까?", "english": "It departs at 2:15 PM. Would you like to book a ticket?"},
            {"role": "Passenger", "korean": "네, 편도로 한 장 주세요. 어느 플랫폼으로 가야 하나요?", "english": "Yes, one single ticket, please. Which platform should I go to?"},
            {"role": "Clerk", "korean": "3번 플랫폼으로 가시면 됩니다. 티켓 여기 있습니다.", "english": "Go to platform 3. Here is your ticket."}
        ],
        "expressions": [
            {"korean": "편도 티켓", "english": "single ticket / one-way ticket"},
            {"korean": "왕복 티켓", "english": "return ticket / round-trip ticket"},
            {"korean": "출발 플랫폼", "english": "departure platform"}
        ]
    },
    16: {
        "title": "렌터카 예약 확인 및 인수",
        "dialogue": [
            {"role": "Passenger", "korean": "안녕하세요, 제 이름으로 차량을 예약했습니다.", "english": "Hello, I reserved a car under my name."},
            {"role": "Agent", "korean": "예약 내역을 확인해 보겠습니다. 운전면허증과 신용카드를 주시겠어요?", "english": "Let me check the reservation. May I have your driver's license and credit card?"},
            {"role": "Passenger", "korean": "네, 국제운전면허증도 여기 있습니다.", "english": "Yes, here is my international driving permit as well."},
            {"role": "Agent", "korean": "확인되었습니다. 차량은 밖의 B구역에 주차되어 있습니다.", "english": "Confirmed. The car is parked in Zone B outside."}
        ],
        "expressions": [
            {"korean": "차량을 예약하다", "english": "reserve a car"},
            {"korean": "국제 운전면허증", "english": "international driving permit (IDP)"},
            {"korean": "신용카드", "english": "credit card"}
        ]
    },
    17: {
        "title": "렌터카 보험 및 반납",
        "dialogue": [
            {"role": "Agent", "korean": "보험은 완전 자차(Full Cover)로 하시겠습니까?", "english": "Would you like full coverage insurance?"},
            {"role": "Passenger", "korean": "네, 완전 자차 보험으로 포함해 주세요.", "english": "Yes, please include full coverage insurance."},
            {"role": "Passenger", "korean": "차량을 반납할 때 연료를 가득 채워야 하나요?", "english": "Do I need to return the car with a full tank of gas?"},
            {"role": "Agent", "korean": "네, 인수한 상태와 동일하게 가득 채워서 반납하셔야 합니다.", "english": "Yes, you must return it full, just as you received it."}
        ],
        "expressions": [
            {"korean": "완전 자차 보험", "english": "full coverage insurance"},
            {"korean": "연료를 가득 채운 상태", "english": "a full tank of gas"},
            {"korean": "차량을 반납하다", "english": "return the car"}
        ]
    },
    18: {
        "title": "우버/그랩 승차 위치 조율",
        "dialogue": [
            {"role": "Driver", "korean": "안녕하세요, 저는 지금 2번 터미널 출구 앞에 있습니다. 어디 계신가요?", "english": "Hello, I am in front of Terminal 2 Exit now. Where are you?"},
            {"role": "Passenger", "korean": "저는 스타벅스 맞은편 횡단보도 옆에 서 있어요.", "english": "I'm standing next to the crosswalk opposite Starbucks."},
            {"role": "Driver", "korean": "아, 알겠습니다. 비상등을 켜고 그리로 갈게요. 제 차량 번호는 5678입니다.", "english": "Oh, I see. I'll pull up with my hazard lights on. My plate number is 5678."},
            {"role": "Passenger", "korean": "네, 흰색 차량이 보이네요. 타고 가겠습니다.", "english": "Yes, I see the white car. I'll get in."}
        ],
        "expressions": [
            {"korean": "맞은편", "english": "opposite / across from"},
            {"korean": "비상등", "english": "hazard lights"},
            {"korean": "차량 번호판", "english": "license plate / plate number"}
        ]
    },
    19: {
        "title": "교통 체증 및 우회 요청",
        "dialogue": [
            {"role": "Passenger", "korean": "길이 아주 많이 막히네요. 다른 빠른 길은 없나요?", "english": "The traffic is very heavy. Is there another fast route?"},
            {"role": "Driver", "korean": "내비게이션상으로 우회 도로가 조금 더 빠르다고 나오네요.", "english": "The GPS shows that a detour is a bit faster."},
            {"role": "Passenger", "korean": "그럼 우회 도로로 가주세요. 감사합니다.", "english": "Then please take the detour. Thank you."},
            {"role": "Driver", "korean": "네, 그쪽 방향으로 경로를 변경하겠습니다.", "english": "Sure, I'll reroute in that direction."}
        ],
        "expressions": [
            {"korean": "우회 도로", "english": "detour / bypass"},
            {"korean": "경로를 바꾸다", "english": "reroute / change the route"},
            {"korean": "내비게이션", "english": "GPS / navigation"}
        ]
    },
    20: {
        "title": "대중교통 추천받기",
        "dialogue": [
            {"role": "Passenger", "korean": "실례합니다, 여기서 차이나타운에 가려면 지하철과 버스 중 무엇이 더 빠른가요?", "english": "Excuse me, to get to Chinatown from here, which is faster, the subway or the bus?"},
            {"role": "Local", "korean": "지금 시간대에는 지하철을 타는 것이 훨씬 빠릅니다.", "english": "At this time of day, taking the subway is much faster."},
            {"role": "Passenger", "korean": "몇 호선을 타야 하나요?", "english": "Which line should I take?"},
            {"role": "Local", "korean": "초록색 2호선을 타시고 3정거장 후에 내리시면 됩니다.", "english": "Take the green Line 2 and get off after 3 stops."}
        ],
        "expressions": [
            {"korean": "지하철 호선", "english": "subway line"},
            {"korean": "~가 훨씬 빠르다", "english": "is much faster"},
            {"korean": "대중교통", "english": "public transportation"}
        ]
    },

    # 테마 3: 호텔 및 숙소 (21~30)
    21: {
        "title": "체크인 예약 확인",
        "dialogue": [
            {"role": "Guest", "korean": "안녕하세요, 체크인을 하고 싶습니다. '김재우'로 예약했습니다.", "english": "Hello, I'd like to check in. I have a reservation under the name Jaewoo Kim."},
            {"role": "Receptionist", "korean": "반갑습니다. 예약 내역을 확인할 수 있도록 여권을 보여주시겠어요?", "english": "Welcome. May I see your passport to verify the reservation?"},
            {"role": "Guest", "korean": "여기 있습니다. 예약 확인서도 필요한가요?", "english": "Here it is. Do you also need the booking confirmation?"},
            {"role": "Receptionist", "korean": "아니요, 여권만으로 확인되었습니다. 잠시만 기다려 주세요.", "english": "No, the passport is enough. Just a moment, please."}
        ],
        "expressions": [
            {"korean": "체크인하다", "english": "check in"},
            {"korean": "~의 이름으로 예약하다", "english": "have a reservation under the name"},
            {"korean": "예약 확인서", "english": "booking confirmation"}
        ]
    },
    22: {
        "title": "보증금(디포짓) 및 결제",
        "dialogue": [
            {"role": "Receptionist", "korean": "보증금(Deposit)을 위해 신용카드가 필요합니다.", "english": "We need a credit card for the security deposit."},
            {"role": "Guest", "korean": "보증금은 얼마인가요? 그리고 체크아웃할 때 환불되나요?", "english": "How much is the deposit, and is it refunded when I check out?"},
            {"role": "Receptionist", "korean": "100달러이며, 체크아웃할 때 파손이나 결제 건이 없으면 승인 취소됩니다.", "english": "It's 100 dollars. It will be voided at checkout if there are no damages or extra charges."},
            {"role": "Guest", "korean": "네, 여기 카드가 있습니다.", "english": "Okay, here is my card."}
        ],
        "expressions": [
            {"korean": "보증금", "english": "security deposit"},
            {"korean": "승인 취소되다", "english": "be voided / refunded"},
            {"korean": "추가 요금", "english": "extra charges"}
        ]
    },
    23: {
        "title": "방 변경 요청 (소음, 뷰 등)",
        "dialogue": [
            {"role": "Guest", "korean": "방이 도로변이라 너무 시끄러워요. 다른 방으로 바꿀 수 있을까요?", "english": "My room is on the street side and it's too noisy. Can I change to another room?"},
            {"role": "Receptionist", "korean": "불편을 드려 죄송합니다. 안뜰 전망(Courtyard view)의 조용한 방으로 변경해 드릴까요?", "english": "Sorry for the inconvenience. Would you like to switch to a quiet room with a courtyard view?"},
            {"role": "Guest", "korean": "네, 조용한 방이면 좋겠습니다. 감사합니다.", "english": "Yes, a quiet room would be great. Thank you."},
            {"role": "Receptionist", "korean": "새 객실 열쇠를 준비해 드리겠습니다. 기존 방의 짐을 옮겨 드릴까요?", "english": "I'll prepare the new room key. Shall we help move your luggage?"}
        ],
        "expressions": [
            {"korean": "너무 시끄러운", "english": "too noisy"},
            {"korean": "방을 변경하다", "english": "change/switch rooms"},
            {"korean": "안뜰 전망", "english": "courtyard view"}
        ]
    },
    24: {
        "title": "객실 비품 추가 요청",
        "dialogue": [
            {"role": "Guest", "korean": "실례합니다, 802호실인데 타월을 두 장만 더 주실 수 있나요?", "english": "Excuse me, I'm in room 802. Could we get two more towels?"},
            {"role": "Receptionist", "korean": "네, 바로 하우스키핑 부서에 연락해서 보내드리겠습니다.", "english": "Sure, I'll contact housekeeping and have them sent up right away."},
            {"role": "Guest", "korean": "그리고 생수도 부족한데, 추가 요금이 붙나요?", "english": "And we are also short of bottled water. Is there an extra charge?"},
            {"role": "Receptionist", "korean": "하루에 두 병은 무료로 제공되며, 추가되는 생수는 무료입니다.", "english": "Two bottles per day are complimentary, and any additional bottles are free of charge."}
        ],
        "expressions": [
            {"korean": "하우스키핑", "english": "housekeeping"},
            {"korean": "무료의", "english": "complimentary / free of charge"},
            {"korean": "생수", "english": "bottled water"}
        ]
    },
    25: {
        "title": "와이파이 및 부대시설 문의",
        "dialogue": [
            {"role": "Guest", "korean": "객실 안에서 와이파이는 어떻게 연결하나요?", "english": "How do I connect to the Wi-Fi in the room?"},
            {"role": "Receptionist", "korean": "호텔 Wi-Fi를 선택하신 후, 객실 번호와 성(Last name)을 입력하시면 됩니다.", "english": "Select the hotel Wi-Fi, then enter your room number and your last name."},
            {"role": "Guest", "korean": "헬스장과 수영장 이용 시간은 어떻게 되나요?", "english": "What are the hours for the gym and the swimming pool?"},
            {"role": "Receptionist", "korean": "둘 다 오전 6시부터 오후 10시까지 오픈하며, 3층에 위치해 있습니다.", "english": "Both are open from 6 AM to 10 PM, located on the 3rd floor."}
        ],
        "expressions": [
            {"korean": "와이파이에 연결하다", "english": "connect to the Wi-Fi"},
            {"korean": "부대시설", "english": "facilities / amenities"},
            {"korean": "객실 번호", "english": "room number"}
        ]
    },
    26: {
        "title": "에어컨/히터 고장 신고",
        "dialogue": [
            {"role": "Guest", "korean": "방 안의 에어컨이 작동하지 않아서 방이 너무 덥습니다.", "english": "The air conditioner in my room isn't working, and the room is too hot."},
            {"role": "Receptionist", "korean": "불편을 드려 죄송합니다. 기술자(Technician)를 즉시 보내드리겠습니다.", "english": "I'm sorry for the inconvenience. I will send a technician right away."},
            {"role": "Guest", "korean": "만약 지금 고칠 수 없다면, 방을 바꾸어 주시겠어요?", "english": "If it can't be fixed now, could you change my room?"},
            {"role": "Receptionist", "korean": "네, 수리가 오래 걸릴 경우 바로 다른 방으로 안내해 드리겠습니다.", "english": "Yes, if the repair takes too long, we will move you to another room immediately."}
        ],
        "expressions": [
            {"korean": "작동하지 않다", "english": "not working / out of order"},
            {"korean": "기술자", "english": "technician / repairman"},
            {"korean": "방을 바꾸다", "english": "change the room"}
        ]
    },
    27: {
        "title": "조식 시간 및 장소 확인",
        "dialogue": [
            {"role": "Guest", "korean": "아침 식사는 어디서 하나요? 그리고 몇 시부터 가능한가요?", "english": "Where can I have breakfast, and what time does it start?"},
            {"role": "Receptionist", "korean": "조식은 1층에 있는 '오로라' 레스토랑에서 제공되며, 아침 6시반부터 10시까지입니다.", "english": "Breakfast is served at the 'Aurora' restaurant on the 1st floor, from 6:30 AM to 10:00 AM."},
            {"role": "Guest", "korean": "제 방 번호만 말하면 입장할 수 있나요?", "english": "Can I just give them my room number to enter?"},
            {"role": "Receptionist", "korean": "네, 입구에서 방 번호를 말씀하시면 됩니다. 예약에 조식이 포함되어 있으십니다.", "english": "Yes, just state your room number at the entrance. Breakfast is included in your reservation."}
        ],
        "expressions": [
            {"korean": "조식이 제공되다", "english": "breakfast is served"},
            {"korean": "방 번호를 대다", "english": "give/state room number"},
            {"korean": "예약에 포함되다", "english": "included in the reservation"}
        ]
    },
    28: {
        "title": "모닝콜 예약",
        "dialogue": [
            {"role": "Guest", "korean": "내일 아침에 모닝콜을 예약하고 싶습니다.", "english": "I'd like to request a wake-up call for tomorrow morning."},
            {"role": "Receptionist", "korean": "네, 몇 시에 전화를 드리면 될까요?", "english": "Sure, what time should we call you?"},
            {"role": "Guest", "korean": "오전 6시 반에 깨워주세요.", "english": "Please wake me up at 6:30 AM."},
            {"role": "Receptionist", "korean": "6시 반에 모닝콜을 등록해 드렸습니다. 편안한 밤 되세요.", "english": "I have set the wake-up call for 6:30 AM. Have a good night."}
        ],
        "expressions": [
            {"korean": "모닝콜", "english": "wake-up call"},
            {"korean": "~을 요청하다", "english": "request / ask for"},
            {"korean": "깨워주다", "english": "wake someone up"}
        ]
    },
    29: {
        "title": "수하물 보관 요청",
        "dialogue": [
            {"role": "Guest", "korean": "체크아웃 후에 짐을 몇 시간 동안 맡아줄 수 있나요?", "english": "Can you keep my luggage for a few hours after checkout?"},
            {"role": "Receptionist", "korean": "물론입니다. 수하물 보관실(Luggage storage)에 안전하게 보관해 드립니다.", "english": "Certainly. We can store it safely in our luggage storage room."},
            {"role": "Guest", "korean": "오후 5시쯤 돌아와서 찾을 예정입니다.", "english": "I'll be back to pick it up around 5 PM."},
            {"role": "Receptionist", "korean": "여기 짐표(Luggage tag)를 받으세요. 나중에 짐을 찾으실 때 이 표를 보여주시면 됩니다.", "english": "Here is your luggage tag. Just show this tag when you retrieve your bags."}
        ],
        "expressions": [
            {"korean": "짐을 맡기다", "english": "store/keep luggage"},
            {"korean": "짐표", "english": "luggage tag / baggage claim check"},
            {"korean": "찾아가다(회수하다)", "english": "pick up / retrieve"}
        ]
    },
    30: {
        "title": "체크아웃 및 추가 요금",
        "dialogue": [
            {"role": "Guest", "korean": "체크아웃 하려고 합니다. 504호실입니다.", "english": "I'd like to check out. I'm in room 504."},
            {"role": "Receptionist", "korean": "감사합니다. 미니바를 이용하시거나 추가 결제하실 항목이 있나요?", "english": "Thank you. Did you use the minibar or have any other extra charges?"},
            {"role": "Guest", "korean": "아니요, 이용하지 않았습니다. 여기 열쇠 카드 있습니다.", "english": "No, I didn't. Here is my key card."},
            {"role": "Receptionist", "korean": "확인되었습니다. 영수증은 이메일로 보내드리겠습니다. 즐거운 여행 되세요!", "english": "All clear. I will email the receipt to you. Have a great trip!"}
        ],
        "expressions": [
            {"korean": "체크아웃하다", "english": "check out"},
            {"korean": "미니바", "english": "minibar"},
            {"korean": "영수증", "english": "receipt"}
        ]
    },

    # 테마 4: 식당 및 카페 (31~40)
    31: {
        "title": "예약 확인 및 테이블 안내",
        "dialogue": [
            {"role": "Guest", "korean": "안녕하세요, 오후 7시에 '민우'로 예약했습니다.", "english": "Hello, I have a reservation at 7 PM under the name Minwoo."},
            {"role": "Host", "korean": "확인해 보겠습니다. 네, 7시에 두 분 예약 맞으시네요. 이쪽으로 안내해 드리겠습니다.", "english": "Let me check. Yes, a table for two at 7 PM. Please follow me this way."},
            {"role": "Guest", "korean": "창가 자리로 앉을 수 있을까요?", "english": "Could we sit by the window?"},
            {"role": "Host", "korean": "마침 창가에 빈 테이블이 있네요. 여기로 모시겠습니다.", "english": "Fortunately, we have an empty table by the window. Here you go."}
        ],
        "expressions": [
            {"korean": "창가 자리", "english": "window seat / table by the window"},
            {"korean": "따라오세요", "english": "follow me / this way, please"},
            {"korean": "예약을 확인하다", "english": "confirm/check reservation"}
        ]
    },
    32: {
        "title": "메뉴 추천 요청 및 대기 시간",
        "dialogue": [
            {"role": "Guest", "korean": "이 레스토랑의 대표 요리는 무엇인가요? 추천해 주시겠어요?", "english": "What is the signature dish here? Can you recommend something?"},
            {"role": "Waiter", "korean": "저희 가게는 티본 스테이크와 크림 파스타가 가장 유명합니다.", "english": "Our T-bone steak and cream pasta are the most popular items."},
            {"role": "Guest", "korean": "좋네요. 스테이크를 주문하면 요리가 나오는 데 얼마나 걸리나요?", "english": "Great. If I order the steak, how long will it take to prepare?"},
            {"role": "Waiter", "korean": "약 15분에서 20분 정도 소요됩니다.", "english": "It takes about 15 to 20 minutes."}
        ],
        "expressions": [
            {"korean": "대표 요리(시그니처)", "english": "signature dish"},
            {"korean": "가장 유명한 / 인기 있는", "english": "most popular / famous"},
            {"korean": "얼마나 걸리나요?", "english": "How long will it take?"}
        ]
    },
    33: {
        "title": "주문하기",
        "dialogue": [
            {"role": "Waiter", "korean": "주문하시겠습니까?", "english": "Are you ready to order?"},
            {"role": "Guest", "korean": "네, 티본 스테이크 하나와 시저 샐러드 하나 주세요.", "english": "Yes, we'd like one T-bone steak and a Caesar salad, please."},
            {"role": "Waiter", "korean": "알겠습니다. 음료는 필요 없으신가요?", "english": "Certainly. Would you like anything to drink?"},
            {"role": "Guest", "korean": "레드 와인 두 잔도 같이 주세요.", "english": "Two glasses of red wine as well, please."}
        ],
        "expressions": [
            {"korean": "주문할 준비가 되다", "english": "ready to order"},
            {"korean": "시저 샐러드", "english": "Caesar salad"},
            {"korean": "~도 같이 주세요", "english": "as well, please"}
        ]
    },
    34: {
        "title": "굽기 정도 및 알레르기 설명",
        "dialogue": [
            {"role": "Waiter", "korean": "스테이크의 굽기는 어떻게 해드릴까요?", "english": "How would you like your steak cooked?"},
            {"role": "Guest", "korean": "미디엄 웰던으로 구워주세요.", "english": "Medium-well, please."},
            {"role": "Guest", "korean": "그리고 제가 견과류 알레르기가 있어서, 샐러드에 견과류는 빼주세요.", "english": "And I'm allergic to nuts, so please leave them out of the salad."},
            {"role": "Waiter", "korean": "네, 주방에 전달하여 견과류가 들어가지 않도록 특별히 주의하겠습니다.", "english": "Got it. I'll inform the kitchen to make sure there are no nuts."}
        ],
        "expressions": [
            {"korean": "굽기 정도", "english": "cooked (rare/medium/well-done)"},
            {"korean": "알레르기가 있는", "english": "allergic to"},
            {"korean": "~을 빼다", "english": "leave out / exclude"}
        ]
    },
    35: {
        "title": "물, 음료 및 소스 추가 주문",
        "dialogue": [
            {"role": "Guest", "korean": "실례합니다, 여기 물 좀 채워주시겠어요?", "english": "Excuse me, could you refill our water, please?"},
            {"role": "Waiter", "korean": "네, 바로 채워 드리겠습니다. 일반 물과 탄산수 중 어떤 것을 원하시나요?", "english": "Sure, I'll do that right away. Still water or sparkling water?"},
            {"role": "Guest", "korean": "일반 물로 주세요. 그리고 스테이크 소스도 더 주실 수 있나요?", "english": "Still water, please. And can we also have some more steak sauce?"},
            {"role": "Waiter", "korean": "네, 소스도 추가로 가져다 드리겠습니다.", "english": "Certainly, I'll bring some extra sauce for you."}
        ],
        "expressions": [
            {"korean": "리필하다(다시 채우다)", "english": "refill"},
            {"korean": "일반 물(스틸워터)", "english": "still water"},
            {"korean": "탄산수", "english": "sparkling water"}
        ]
    },
    36: {
        "title": "카페에서 음료 주문",
        "dialogue": [
            {"role": "Barista", "korean": "안녕하세요, 무엇을 도와드릴까요?", "english": "Hi, what can I get for you today?"},
            {"role": "Guest", "korean": "아이스 아메리카노 한 잔이랑 따뜻한 라떼 한 잔 주세요.", "english": "I'd like an iced americano and a hot latte, please."},
            {"role": "Barista", "korean": "라떼의 컵 사이즈는 어떻게 하시겠어요? 그리고 우유 종류는요?", "english": "What size would you like for the latte? And what kind of milk?"},
            {"role": "Guest", "korean": "라떼는 톨 사이즈로 하시고, 저지방 우유로 변경해 주세요.", "english": "Tall size for the latte, and make it with low-fat milk, please."}
        ],
        "expressions": [
            {"korean": "저지방 우유", "english": "low-fat milk"},
            {"korean": "두유 / 아몬드유", "english": "soy milk / almond milk"},
            {"korean": "아이스 아메리카노", "english": "iced americano"}
        ]
    },
    37: {
        "title": "디저트 및 남은 음식 포장",
        "dialogue": [
            {"role": "Guest", "korean": "디저트 메뉴판을 볼 수 있을까요?", "english": "Could we see the dessert menu, please?"},
            {"role": "Waiter", "korean": "네, 여기 있습니다. 치즈케이크와 애플 파이가 좋습니다.", "english": "Here it is. The cheesecake and apple pie are excellent."},
            {"role": "Guest", "korean": "아, 배가 너무 부르네요. 혹시 남은 피자를 포장해 갈 수 있을까요?", "english": "Oh, I'm too full. Can we get this leftover pizza wrapped up?"},
            {"role": "Waiter", "korean": "네, 포장 박스에 담아다 드리겠습니다. 잠시만요.", "english": "Sure, I'll box it up for you. Just a moment."}
        ],
        "expressions": [
            {"korean": "디저트 메뉴판", "english": "dessert menu"},
            {"korean": "남은 음식", "english": "leftovers"},
            {"korean": "포장하다", "english": "box it up / wrap it up / to go"}
        ]
    },
    38: {
        "title": "계산서 요청",
        "dialogue": [
            {"role": "Guest", "korean": "실례합니다, 계산서 좀 갖다 주시겠어요?", "english": "Excuse me, could we have the check, please?"},
            {"role": "Waiter", "korean": "네, 테이블에서 도와드릴까요, 아니면 카운터에서 계산하시겠습니까?", "english": "Sure, would you like to pay at the table or at the register?"},
            {"role": "Guest", "korean": "테이블에서 계산하겠습니다.", "english": "We will pay at the table."},
            {"role": "Waiter", "korean": "알겠습니다. 영수증과 함께 계산서를 가져다 드리겠습니다.", "english": "Got it. I will bring the bill along with the receipt."}
        ],
        "expressions": [
            {"korean": "계산서(체크)", "english": "check / bill"},
            {"korean": "계산 카운터", "english": "register / counter"},
            {"korean": "테이블에서 계산하다", "english": "pay at the table"}
        ]
    },
    39: {
        "title": "분할 계산 요청",
        "dialogue": [
            {"role": "Guest", "korean": "따로따로 계산할 수 있을까요?", "english": "Can we split the bill, please?"},
            {"role": "Waiter", "korean": "네, 가능합니다. 반반씩 계산해 드릴까요, 아니면 따로 주문한 대로 해드릴까요?", "english": "Yes, we can. Shall I split it 50/50, or by what you ordered?"},
            {"role": "Guest", "korean": "주문한 카드 2개로 정확히 절반씩 결제해 주세요.", "english": "Please charge half to each of these two cards."},
            {"role": "Waiter", "korean": "알겠습니다. 두 장의 카드로 각각 결제 처리해 오겠습니다.", "english": "Sure, I'll process the payment with both cards."}
        ],
        "expressions": [
            {"korean": "계산서를 나누다", "english": "split the bill / split the check"},
            {"korean": "따로따로 계산하다", "english": "pay separately"},
            {"korean": "절반씩", "english": "fifty-fifty (50/50)"}
        ]
    },
    40: {
        "title": "팁(Tip) 및 영수증 확인",
        "dialogue": [
            {"role": "Guest", "korean": "이 계산서에 팁(서비스 비용)이 포함되어 있나요?", "english": "Is the tip included in this bill?"},
            {"role": "Waiter", "korean": "아니요, 포함되어 있지 않습니다. 서비스 요금은 손님의 선택입니다.", "english": "No, it's not. The gratuity is at your discretion."},
            {"role": "Guest", "korean": "알겠습니다. 15% 정도 팁을 카드로 추가 결제해 주세요.", "english": "Okay, please add a 15% tip to the card payment."},
            {"role": "Waiter", "korean": "감사합니다. 여기 영수증과 결제 카드입니다. 좋은 하루 보내세요!", "english": "Thank you. Here is your receipt and card. Have a wonderful day!"}
        ],
        "expressions": [
            {"korean": "팁(봉사료)", "english": "tip / gratuity"},
            {"korean": "~이 포함되다", "english": "be included"},
            {"korean": "선택 사항", "english": "at one's discretion / optional"}
        ]
    },

    # 테마 5: 길 찾기 및 위치 (41~50)
    41: {
        "title": "특정 장소 위치 묻기",
        "dialogue": [
            {"role": "Passenger", "korean": "실례합니다, 지하철역이 어디에 있는지 알려주실 수 있나요?", "english": "Excuse me, can you tell me where the subway station is?"},
            {"role": "Local", "korean": "네, 이 길을 따라 한 블록 더 가신 뒤 우회전하세요.", "english": "Yes, go straight down this street for one block and then turn right."},
            {"role": "Passenger", "korean": "걸어가기에 먼가요?", "english": "Is it far to walk?"},
            {"role": "Local", "korean": "아니요, 걸어서 5분 정도밖에 안 걸립니다.", "english": "No, it only takes about five minutes on foot."}
        ],
        "expressions": [
            {"korean": "우회전하다 / 좌회전하다", "english": "turn right / turn left"},
            {"korean": "한 블록", "english": "one block"},
            {"korean": "도보로", "english": "on foot / walking"}
        ]
    },
    42: {
        "title": "거리 및 소요 시간 묻기",
        "dialogue": [
            {"role": "Passenger", "korean": "여기서 대영 박물관까지 거리가 얼마나 되나요?", "english": "How far is it from here to the British Museum?"},
            {"role": "Local", "korean": "약 2킬로미터 정도 떨어져 있습니다.", "english": "It's about two kilometers away."},
            {"role": "Passenger", "korean": "걸어가면 얼마나 걸릴까요?", "english": "How long would it take to walk?"},
            {"role": "Local", "korean": "도보로 25분 정도 소요되니, 버스를 타는 것을 추천합니다.", "english": "It will take around 25 minutes on foot, so I recommend taking a bus."}
        ],
        "expressions": [
            {"korean": "거리가 얼마나 되나요?", "english": "How far is it?"},
            {"korean": "~에서 떨어져 있는", "english": "away from"},
            {"korean": "추천하다", "english": "recommend"}
        ]
    },
    43: {
        "title": "지도로 길 찾기 도움",
        "dialogue": [
            {"role": "Passenger", "korean": "실례합니다만, 지도에서 저희의 현재 위치를 좀 짚어주시겠어요?", "english": "Excuse me, could you point out our current location on this map?"},
            {"role": "Local", "korean": "네, 저희는 지금 브로드웨이 45번가 사거리에 있습니다.", "english": "Sure, we are right here at the intersection of Broadway and 45th Street."},
            {"role": "Passenger", "korean": "타임스 스퀘어로 가려면 어느 방향으로 가야 하죠?", "english": "Which direction should we go to get to Times Square?"},
            {"role": "Local", "korean": "북쪽(위쪽)으로 직진해서 가시면 전광판들이 보일 겁니다.", "english": "Just head straight north, and you'll see the screens soon."}
        ],
        "expressions": [
            {"korean": "사거리(교차로)", "english": "intersection / crossroads"},
            {"korean": "현재 위치", "english": "current location"},
            {"korean": "~을 가리키다/짚다", "english": "point out"}
        ]
    },
    44: {
        "title": "길을 잃었을 때 도움",
        "dialogue": [
            {"role": "Passenger", "korean": "죄송한데 제가 길을 잃었어요. 기차역으로 가는 길을 잃어버렸습니다.", "english": "Excuse me, I'm lost. I've lost my way to the train station."},
            {"role": "Local", "korean": "걱정 마세요. 저기 보이는 큰 현대식 빌딩이 바로 기차역 건물입니다.", "english": "Don't worry. That large modern building over there is the train station."},
            {"role": "Passenger", "korean": "아, 그렇군요! 저 방향으로 직진해서 가면 되나요?", "english": "Oh, I see! Should I just walk straight in that direction?"},
            {"role": "Local", "korean": "네, 횡단보도 하나만 건너시면 바로 정문입니다.", "english": "Yes, just cross one crosswalk and you will reach the main entrance."}
        ],
        "expressions": [
            {"korean": "길을 잃다", "english": "be lost / lose one's way"},
            {"korean": "정문", "english": "main entrance"},
            {"korean": "걱정 마세요", "english": "Don't worry"}
        ]
    },
    45: {
        "title": "Landmark 위치 문의",
        "dialogue": [
            {"role": "Passenger", "korean": "실례합니다, 에펠탑이 보이는 전망 포인트가 근처에 있나요?", "english": "Excuse me, is there a good viewing spot for the Eiffel Tower nearby?"},
            {"role": "Local", "korean": "네, 트로카데로 광장에 가면 에펠탑을 가장 아름답게 볼 수 있습니다.", "english": "Yes, if you go to Trocadéro Square, you can get the best view of the Eiffel Tower."},
            {"role": "Passenger", "korean": "광장까지 버스로 가야 하나요?", "english": "Should I take a bus to get to the square?"},
            {"role": "Local", "korean": "걸어가셔도 10분 내로 닿을 수 있습니다. 강을 건너 바로 건너편에 있습니다.", "english": "You can reach it on foot within 10 minutes. It's just across the river."}
        ],
        "expressions": [
            {"korean": "전망 좋은 포인트", "english": "viewing spot / viewpoint"},
            {"korean": "가장 아름다운 뷰", "english": "the best view"},
            {"korean": "~에 닿다", "english": "reach / get to"}
        ]
    },
    46: {
        "title": "화장실 위치 묻기",
        "dialogue": [
            {"role": "Passenger", "korean": "실례합니다, 근처에 공중화장실이 있나요?", "english": "Excuse me, is there a public restroom nearby?"},
            {"role": "Local", "korean": "근처에는 공중화장실이 없지만, 저기 스타벅스 화장실을 이용할 수 있을 겁니다.", "english": "There is no public restroom nearby, but you can probably use the one in the Starbucks over there."},
            {"role": "Passenger", "korean": "화장실 번호키나 영수증 비밀번호가 필요한가요?", "english": "Do I need a key or a receipt code to access the restroom?"},
            {"role": "Local", "korean": "네, 카운터에서 음료를 주문하면 영수증에 비밀번호가 적혀 있을 거예요.", "english": "Yes, if you order a drink at the counter, the code will be printed on the receipt."}
        ],
        "expressions": [
            {"korean": "공중화장실", "english": "public restroom / toilet"},
            {"korean": "비밀번호 키", "english": "access code / passcode"},
            {"korean": "영수증에 인쇄된", "english": "printed on the receipt"}
        ]
    },
    47: {
        "title": "가장 가까운 ATM 찾기",
        "dialogue": [
            {"role": "Passenger", "korean": "가장 가까운 현금 자동 인출기(ATM)는 어디에 있나요?", "english": "Where is the nearest ATM?"},
            {"role": "Local", "korean": "코너를 돌면 바로 있는 씨티은행 안에 은행 ATM이 있습니다.", "english": "There is a bank ATM inside Citibank just around the corner."},
            {"role": "Passenger", "korean": "그 은행이 지금 시간에도 열려 있나요?", "english": "Is the bank open at this hour?"},
            {"role": "Local", "korean": "은행은 닫혔지만 ATM 구역은 24시간 열려 있어서 언제든 카드 카드로 현금을 뽑을 수 있습니다.", "english": "The bank is closed, but the ATM lobby is open 24 hours so you can withdraw cash anytime."}
        ],
        "expressions": [
            {"korean": "현금 인출기", "english": "ATM (Automated Teller Machine)"},
            {"korean": "현금을 뽑다(인출하다)", "english": "withdraw cash"},
            {"korean": "길 모퉁이를 돌다", "english": "around the corner"}
        ]
    },
    48: {
        "title": "약국/슈퍼마켓 찾기",
        "dialogue": [
            {"role": "Passenger", "korean": "실례합니다, 근처에 약국이 어디에 있나요? 머리가 아파서요.", "english": "Excuse me, where is a pharmacy nearby? I have a headache."},
            {"role": "Local", "korean": "길 건너편에 초록색 십자가 간판이 달린 약국이 보입니다.", "english": "You can see a pharmacy with a green cross sign across the street."},
            {"role": "Passenger", "korean": "오늘 일요일인데 영업을 하나요?", "english": "Is it open today? It's Sunday."},
            {"role": "Local", "korean": "저 약국은 당번 약국이라 일요일에도 늦게까지 엽니다.", "english": "That pharmacy is on duty, so it is open late even on Sundays."}
        ],
        "expressions": [
            {"korean": "약국", "english": "pharmacy / drugstore"},
            {"korean": "당번 약국(당직)", "english": "on-duty pharmacy"},
            {"korean": "두통이 있다", "english": "have a headache"}
        ]
    },
    49: {
        "title": "횡단보도 및 지하도 찾기",
        "dialogue": [
            {"role": "Passenger", "korean": "길을 건너고 싶은데 횡단보도가 보이지 않네요. 어디로 가야 하나요?", "english": "I want to cross the street, but I don't see a crosswalk. Where should I go?"},
            {"role": "Local", "korean": "이 아래 지하도를 통해서만 건널 수 있습니다.", "english": "You can only cross the street through the underpass below."},
            {"role": "Passenger", "korean": "지하도 입구는 어디에 있나요?", "english": "Where is the entrance to the underpass?"},
            {"role": "Local", "korean": "저기 은행 옆에 지하로 내려가는 계단이 있습니다.", "english": "There is a flight of stairs going underground next to the bank over there."}
        ],
        "expressions": [
            {"korean": "횡단보도", "english": "crosswalk / pedestrian crossing"},
            {"korean": "지하도", "english": "underpass / pedestrian subway"},
            {"korean": "길을 건너다", "english": "cross the street"}
        ]
    },
    50: {
        "title": "목적지 지나쳤을 때 대처",
        "dialogue": [
            {"role": "Passenger", "korean": "기사님, 혹시 제가 목적지인 시청을 지나친 건가요?", "english": "Excuse me driver, did I miss my stop at City Hall?"},
            {"role": "Driver", "korean": "네, 두 정거장 전에 지나쳤습니다. 말씀하시는 걸 잊으셨군요.", "english": "Yes, we passed it two stops ago. You forgot to mention it."},
            {"role": "Passenger", "korean": "다음 정거장에서 내려 주시면 걸어서 되돌아가겠습니다.", "english": "Please let me off at the next stop and I'll walk back."},
            {"role": "Driver", "korean": "알겠습니다. 다음 신호등 앞에 바로 내려드릴게요.", "english": "Alright. I'll drop you off right in front of the next traffic light."}
        ],
        "expressions": [
            {"korean": "목적지를 지나치다", "english": "miss one's stop"},
            {"korean": "내려주다", "english": "let someone off / drop someone off"},
            {"korean": "걸어서 되돌아가다", "english": "walk back"}
        ]
    },

    # 테마 6: 쇼핑 및 면세점 (51~60)
    51: {
        "title": "상품 탐색 및 직원 도움 거절",
        "dialogue": [
            {"role": "Clerk", "korean": "안녕하세요, 찾으시는 특별한 상품이 있으신가요?", "english": "Hello, are you looking for anything in particular?"},
            {"role": "Customer", "korean": "아니요, 그냥 둘러보는 중이에요. 고맙습니다.", "english": "No, thank you. I'm just looking around."},
            {"role": "Clerk", "korean": "알겠습니다. 도움이 필요하시면 언제든지 불러주세요.", "english": "Alright. If you need any help, please let me know."},
            {"role": "Customer", "korean": "네, 고맙습니다.", "english": "Sure, thanks."}
        ],
        "expressions": [
            {"korean": "특별히 찾는 것", "english": "anything in particular"},
            {"korean": "그냥 둘러보는 중", "english": "just looking around / browsing"},
            {"korean": "직접 물어볼게요", "english": "I'll let you know"}
        ]
    },
    52: {
        "title": "다른 색상/사이즈 문의",
        "dialogue": [
            {"role": "Customer", "korean": "이 셔츠가 아주 예쁜데, 혹시 미디엄(M) 사이즈가 있나요?", "english": "This shirt is very nice. Do you have it in medium?"},
            {"role": "Clerk", "korean": "재고를 확인해 보겠습니다. 잠시만요... 아, 미디엄 사이즈는 있습니다.", "english": "Let me check the stock. Just a moment... Yes, we have a medium in stock."},
            {"role": "Customer", "korean": "파란색 말고 흰색이나 베이지색도 있나요?", "english": "Do you also have it in white or beige, rather than blue?"},
            {"role": "Clerk", "korean": "베이지색도 M 사이즈로 남아있습니다. 가져다 드릴까요?", "english": "We have it in beige as well. Shall I bring it for you?"}
        ],
        "expressions": [
            {"korean": "M 사이즈로", "english": "in medium / in size M"},
            {"korean": "재고가 있는", "english": "in stock"},
            {"korean": "재고를 확인하다", "english": "check the stock"}
        ]
    },
    53: {
        "title": "피팅룸 및 입어보기",
        "dialogue": [
            {"role": "Customer", "korean": "이 옷을 한 번 입어봐도 될까요?", "english": "Can I try this on?"},
            {"role": "Clerk", "korean": "물론이죠. 피팅룸(Fitting room)은 매장 구석 거울 뒤쪽에 있습니다.", "english": "Certainly. The fitting rooms are in the corner behind that mirror."},
            {"role": "Customer", "korean": "한 번에 몇 벌까지 들고 들어갈 수 있나요?", "english": "How many items can I take in at one time?"},
            {"role": "Clerk", "korean": "최대 세 벌까지 들고 들어가실 수 있습니다.", "english": "You can take up to three items at a time."}
        ],
        "expressions": [
            {"korean": "~을 입어보다", "english": "try on / try this on"},
            {"korean": "피팅룸(탈의실)", "english": "fitting room / dressing room"},
            {"korean": "최대 ~개까지", "english": "up to"}
        ]
    },
    54: {
        "title": "가격 및 할인 여부",
        "dialogue": [
            {"role": "Customer", "korean": "이 제품은 가격이 얼마인가요? 가격표가 없어요.", "english": "How much is this item? There is no price tag on it."},
            {"role": "Clerk", "korean": "이것은 원래 50달러인데, 현재 20% 세일 중입니다.", "english": "This is originally 50 dollars, but it is currently 20% off."},
            {"role": "Customer", "korean": "여기에 학생 할인이나 첫 구매 할인을 추가로 적용할 수 있나요?", "english": "Can I get an additional student discount or first purchase discount?"},
            {"role": "Clerk", "korean": "학생증을 보여주시면 추가로 10%를 더 할인해 드립니다.", "english": "If you show your student ID, we can give you an extra 10% off."}
        ],
        "expressions": [
            {"korean": "가격표", "english": "price tag"},
            {"korean": "할인 중인", "english": "on sale / discounted / % off"},
            {"korean": "추가 할인", "english": "additional/extra discount"}
        ]
    },
    55: {
        "title": "면세(Tax Refund) 가능 여부",
        "dialogue": [
            {"role": "Customer", "korean": "이 매장에서 텍스 리펀(세금 환급)이 가능한가요?", "english": "Is tax refund available in this store?"},
            {"role": "Clerk", "korean": "네, 가능합니다. 50유로 이상 구매하셔야 신청할 수 있습니다.", "english": "Yes, it is. You need to purchase over 50 euros to apply."},
            {"role": "Customer", "korean": "텍스 리펀 서류를 좀 작성해 주실 수 있나요?", "english": "Could you prepare the tax refund documents for me?"},
            {"role": "Clerk", "korean": "물론입니다. 신청을 완료하려면 여권이 필요하니 보여주세요.", "english": "Certainly. I need your passport to complete the application, please."}
        ],
        "expressions": [
            {"korean": "세금 환급(면세)", "english": "tax refund / tax back"},
            {"korean": "면세 서류", "english": "tax refund document / form"},
            {"korean": "~이상 구매하다", "english": "purchase over / spend more than"}
        ]
    },
    56: {
        "title": "선물용 포장",
        "dialogue": [
            {"role": "Customer", "korean": "이 지갑을 선물용으로 포장해 주실 수 있나요?", "english": "Can you wrap this wallet as a gift?"},
            {"role": "Clerk", "korean": "네, 선물 포장은 3달러의 추가 요금이 부과되는데 괜찮으신가요?", "english": "Yes, but there is an extra charge of 3 dollars for gift wrapping. Is that okay?"},
            {"role": "Customer", "korean": "괜찮습니다. 선물 카드도 하나 같이 넣어 주시겠어요?", "english": "That's fine. Could you also include a gift card?"},
            {"role": "Clerk", "korean": "네, 흰색과 분홍색 카드 중 어떤 것으로 원하시나요?", "english": "Sure, would you prefer a white card or a pink one?"}
        ],
        "expressions": [
            {"korean": "선물용 포장", "english": "gift wrapping / wrap as a gift"},
            {"korean": "추가 요금이 부과되다", "english": "extra charge is applied"},
            {"korean": "메시지 카드", "english": "gift card / greeting card"}
        ]
    },
    57: {
        "title": "결제 및 할부",
        "dialogue": [
            {"role": "Clerk", "korean": "결제는 무엇으로 도와드릴까요?", "english": "How would you like to pay?"},
            {"role": "Customer", "korean": "카드로 결제하겠습니다. 혹시 해외 카드로 할부 결제도 되나요?", "english": "I'll pay by card. Can I pay in installments with an international card?"},
            {"role": "Clerk", "korean": "외국 신용카드는 보통 일시불로만 승인 가능하며, 할부는 본인 카드사에 직접 신청하셔야 합니다.", "english": "Foreign credit cards are usually processed as a single payment, and you must apply for installments directly with your card company."},
            {"role": "Customer", "korean": "그럼 그냥 일시불로 결제해 주세요.", "english": "Then please just charge it as a single payment."}
        ],
        "expressions": [
            {"korean": "할부 결제", "english": "payment in installments"},
            {"korean": "일시불 결제", "english": "single payment / lump sum payment"},
            {"korean": "카드사에 신청하다", "english": "apply to the card company"}
        ]
    },
    58: {
        "title": "교환 및 환불 규정",
        "dialogue": [
            {"role": "Customer", "korean": "만약 사이즈가 맞지 않으면 교환이나 환불이 가능한가요?", "english": "If the size doesn't fit, can I exchange or refund it?"},
            {"role": "Clerk", "korean": "네, 구매일로부터 14일 이내에 영수증과 가격표를 지참하시면 가능합니다.", "english": "Yes, you can within 14 days from the purchase date, provided you bring the receipt and the price tag."},
            {"role": "Customer", "korean": "이미 옷을 입었거나 세탁한 제품도 환불이 되나요?", "english": "Can I get a refund even if the item has been worn or washed?"},
            {"role": "Clerk", "korean": "아니요, 착용 흔적이나 세탁한 상품은 규정상 절대 불가합니다.", "english": "No, worn or washed items cannot be refunded under our policy."}
        ],
        "expressions": [
            {"korean": "영수증을 지참하다", "english": "bring the receipt"},
            {"korean": "환불 정책(규정)", "english": "refund policy"},
            {"korean": "착용 흔적", "english": "signs of wear / worn"}
        ]
    },
    59: {
        "title": "물건 하자로 인한 환불",
        "dialogue": [
            {"role": "Customer", "korean": "어제 이 재킷을 샀는데, 소매 지퍼 부분이 고장 나 있어요.", "english": "I bought this jacket yesterday, but the sleeve zipper is broken."},
            {"role": "Clerk", "korean": "정말 죄송합니다. 새 상품으로 교환해 드릴까요, 아니면 환불을 원하시나요?", "english": "I'm very sorry. Would you like to exchange it for a new one, or would you prefer a refund?"},
            {"role": "Customer", "korean": "같은 사이즈의 새 상품이 있다면 교환하고 싶습니다.", "english": "I'd like to exchange it if you have a new one in the same size."},
            {"role": "Clerk", "korean": "확인해 보니 마침 하나 더 있네요. 이것으로 바꾸어 드리겠습니다.", "english": "Checking the back... Yes, we have one more. Let me swap it for you."}
        ],
        "expressions": [
            {"korean": "고장 난 지퍼", "english": "broken zipper"},
            {"korean": "새 것으로 교환하다", "english": "exchange for a new one"},
            {"korean": "죄송합니다", "english": "I'm very sorry / apologize"}
        ]
    },
    60: {
        "title": "쇼핑백 구매",
        "dialogue": [
            {"role": "Clerk", "korean": "물건을 담아갈 쇼핑백이나 종이 봉투가 필요하신가요?", "english": "Do you need a shopping bag or a paper bag for your items?"},
            {"role": "Customer", "korean": "네, 종이 쇼핑백 하나 주세요. 요금이 있나요?", "english": "Yes, please. One paper shopping bag. Is there a charge for it?"},
            {"role": "Clerk", "korean": "네, 봉투 값은 20센트가 청구서에 추가됩니다.", "english": "Yes, 20 cents will be added to your bill for the bag."},
            {"role": "Customer", "korean": "괜찮습니다. 한꺼번에 같이 결제해 주세요.", "english": "That's fine. Please charge it all together."}
        ],
        "expressions": [
            {"korean": "종이 봉투", "english": "paper bag"},
            {"korean": "쇼핑백", "english": "shopping bag"},
            {"korean": "한꺼번에(같이)", "english": "all together"}
        ]
    },

    # 테마 7: 관광 및 매표소 (61~70)
    61: {
        "title": "관광 안내소 지도 받기",
        "dialogue": [
            {"role": "Tourist", "korean": "실례합니다, 근처에 유명한 로컬 맛집 지도가 있나요?", "english": "Excuse me, do you have a map of famous local restaurants?"},
            {"role": "Staff", "korean": "네, 관광객을 위한 먹거리 지도와 도보 여행 추천 코스 브로셔가 있습니다.", "english": "Yes, we have a food map for tourists and a brochure of recommended walking tours."},
            {"role": "Tourist", "korean": "무료로 가져가도 되나요?", "english": "Can I take these for free?"},
            {"role": "Staff", "korean": "네, 자유롭게 가져가셔서 여행을 즐기시면 됩니다.", "english": "Yes, feel free to take them and enjoy your trip."}
        ],
        "expressions": [
            {"korean": "브로셔/안내서", "english": "brochure / pamphlet"},
            {"korean": "도보 투어", "english": "walking tour"},
            {"korean": "마음대로 가져가세요", "english": "feel free to take"}
        ]
    },
    62: {
        "title": "입장권 구매 및 할인",
        "dialogue": [
            {"role": "Tourist", "korean": "성인 두 명 입장권은 얼마인가요?", "english": "How much are the tickets for two adults?"},
            {"role": "Cashier", "korean": "성인은 인당 20달러씩 총 40달러입니다.", "english": "It's 20 dollars per adult, so 40 dollars in total."},
            {"role": "Tourist", "korean": "국제 학생증(ISIC)이 있으면 할인이 되나요?", "english": "Can we get a discount with an International Student Identity Card?"},
            {"role": "Cashier", "korean": "네, 학생증을 제시하시면 인당 15달러로 25% 할인 혜택이 적용됩니다.", "english": "Yes, showing your student ID gets you a 25% discount, making it 15 dollars per person."}
        ],
        "expressions": [
            {"korean": "입장권", "english": "admission ticket / entrance ticket"},
            {"korean": "총액", "english": "in total / total amount"},
            {"korean": "학생 할인", "english": "student discount"}
        ]
    },
    63: {
        "title": "오디오 가이드 대여",
        "dialogue": [
            {"role": "Tourist", "korean": "여기 한국어 오디오 가이드 기기가 있나요?", "english": "Do you have Korean audio guide devices here?"},
            {"role": "Staff", "korean": "네, 있습니다. 대여 요금은 기기당 5달러이며 신분증을 맡겨주셔야 합니다.", "english": "Yes, we do. The rental fee is 5 dollars per device, and you need to leave your ID card."},
            {"role": "Tourist", "korean": "신분증 대신 여권 사본을 맡겨도 될까요?", "english": "Can I leave a copy of my passport instead of my original ID?"},
            {"role": "Staff", "korean": "아니요, 주민등록증, 운전면허증 등 실물 신분증만 보증용으로 가능합니다.", "english": "No, we only accept original physical IDs like a driver's license or ID card for deposit."}
        ],
        "expressions": [
            {"korean": "오디오 가이드", "english": "audio guide"},
            {"korean": "실물 신분증", "english": "original ID card"},
            {"korean": "대여하다", "english": "rent / hire"}
        ]
    },
    64: {
        "title": "사진 촬영 요청",
        "dialogue": [
            {"role": "Tourist", "korean": "실례지만 저희 사진 한 장만 찍어주실 수 있나요?", "english": "Excuse me, could you take a picture of us, please?"},
            {"role": "Passerby", "korean": "물론이죠. 가로나 세로 중 어떤 구도로 찍어드릴까요?", "english": "Sure. Would you like it in landscape or portrait?"},
            {"role": "Tourist", "korean": "에펠탑이 배경으로 다 나오게 세로로 부탁드립니다.", "english": "Portrait, please, so that the Eiffel Tower is fully visible in the background."},
            {"role": "Passerby", "korean": "알겠습니다. 하나, 둘, 셋 하면 찍을게요. 치즈~!", "english": "Alright. I'll shoot on the count of three. One, two, three, cheese!"}
        ],
        "expressions": [
            {"korean": "사진을 찍어주다", "english": "take a picture / photo"},
            {"korean": "가로(풍경) 구도", "english": "landscape mode"},
            {"korean": "세로(인물) 구도", "english": "portrait mode"}
        ]
    },
    65: {
        "title": "시티 투어 버스 탑승",
        "dialogue": [
            {"role": "Tourist", "korean": "이 시티 투어 버스표는 하루 종일 무제한으로 탈 수 있는 표인가요?", "english": "Is this city tour bus ticket unlimited for the whole day?"},
            {"role": "Driver", "korean": "네, 24시간 동안 정류장 어디서든 자유롭게 타고 내릴 수 있습니다.", "english": "Yes, you can hop on and hop off at any designated stop for 24 hours."},
            {"role": "Tourist", "korean": "배차 간격은 얼마나 되나요?", "english": "How often does the bus run?"},
            {"role": "Driver", "korean": "매 15분마다 정류장에 버스가 도착합니다.", "english": "A bus arrives at the stops every 15 minutes."}
        ],
        "expressions": [
            {"korean": "자유롭게 타고 내리다", "english": "hop-on hop-off"},
            {"korean": "배차 간격", "english": "bus interval / how often does it run"},
            {"korean": "지정된 정류장", "english": "designated stop"}
        ]
    },
    66: {
        "title": "미술관 운영 시간",
        "dialogue": [
            {"role": "Tourist", "korean": "오늘 미술관은 몇 시에 문을 닫나요?", "english": "What time does the art museum close today?"},
            {"role": "Staff", "korean": "평일은 오후 6시에 닫고, 목요일은 야간 개장으로 오후 9시까지 운영합니다.", "english": "It closes at 6 PM on weekdays, but on Thursdays it is open until 9 PM for late-night viewing."},
            {"role": "Tourist", "korean": "마지막 입장 마감 시간은 언제인가요?", "english": "When is the last admission?"},
            {"role": "Staff", "korean": "폐관 45분 전인 오후 5시 15분까지는 입장하셔야 합니다.", "english": "You must enter by 5:15 PM, which is 45 minutes before closing time."}
        ],
        "expressions": [
            {"korean": "야간 개장", "english": "late-night opening / open late"},
            {"korean": "마지막 입장", "english": "last admission"},
            {"korean": "폐관 시간", "english": "closing time"}
        ]
    },
    67: {
        "title": "추천 투어 코스 문의",
        "dialogue": [
            {"role": "Tourist", "korean": "반나절 만에 둘러볼 수 있는 추천 코스가 있을까요?", "english": "Is there a recommended itinerary that we can see in half a day?"},
            {"role": "Staff", "korean": "오전에는 고성을 방문하시고, 오후에는 구시가지 광장을 걷는 것을 추천합니다.", "english": "I recommend visiting the historic castle in the morning and walking around the Old Town Square in the afternoon."},
            {"role": "Tourist", "korean": "두 장소 이동 시 대중교통으로 가기 쉽나요?", "english": "Is it easy to travel between the two places by public transport?"},
            {"role": "Staff", "korean": "네, 성 바로 앞 정류장에서 구시가지로 직행하는 트램이 있습니다.", "english": "Yes, there is a direct tram to the Old Town from the stop right in front of the castle."}
        ],
        "expressions": [
            {"korean": "반나절 코스", "english": "half-day itinerary / course"},
            {"korean": "구시가지 광장", "english": "Old Town Square"},
            {"korean": "직행하는", "english": "direct / non-stop"}
        ]
    },
    68: {
        "title": "기념품 샵 위치",
        "dialogue": [
            {"role": "Tourist", "korean": "박물관 내에 공식 기념품 가게가 있나요?", "english": "Is there an official souvenir shop inside the museum?"},
            {"role": "Staff", "korean": "네, 1층 중앙 로비와 3층 출구 근처에 각각 하나씩 있습니다.", "english": "Yes, there is one in the main lobby on the 1st floor, and another near the exit on the 3rd floor."},
            {"role": "Tourist", "korean": "기념품 가게만 티켓 없이 들어갈 수 있나요?", "english": "Can I enter the souvenir shop without a museum ticket?"},
            {"role": "Staff", "korean": "1층 로비 샵은 무료입장이 되지만, 3층 샵은 입장 티켓이 있어야 합니다.", "english": "The lobby shop on the 1st floor is accessible without a ticket, but the 3rd-floor shop requires one."}
        ],
        "expressions": [
            {"korean": "기념품 가게", "english": "souvenir shop / gift shop"},
            {"korean": "중앙 로비", "english": "main lobby"},
            {"korean": "입장권 없이 들어갈 수 있는", "english": "accessible without a ticket"}
        ]
    },
    69: {
        "title": "자유 시간 및 미팅 포인트",
        "dialogue": [
            {"role": "Tourist", "korean": "가이드님, 저희 쇼핑할 자유 시간이 얼마나 주어지나요?", "english": "Excuse me guide, how much free time do we have for shopping?"},
            {"role": "Guide", "korean": "지금부터 정확히 1시간 동안 쇼핑을 하실 수 있습니다.", "english": "You will have exactly one hour of free time starting from now."},
            {"role": "Tourist", "korean": "몇 시까지, 어디로 모여야 하나요?", "english": "By what time and where should we gather?"},
            {"role": "Guide", "korean": "오후 4시 반까지 버스가 주차되어 있는 버스 전용 주차장 앞에 모여주세요.", "english": "Please gather in front of the tour bus parking lot by 4:30 PM."}
        ],
        "expressions": [
            {"korean": "자유 시간", "english": "free time"},
            {"korean": "모이다 / 집합하다", "english": "gather / meet up"},
            {"korean": "투어 버스 주차장", "english": "bus parking lot"}
        ]
    },
    70: {
        "title": "관광지 금지 규정",
        "dialogue": [
            {"role": "Tourist", "korean": "성당 안에서 플래시를 켜고 사진을 찍어도 되나요?", "english": "Is it okay to take photos with a flash inside the cathedral?"},
            {"role": "Staff", "korean": "죄송하지만, 예술품 보호를 위해 플래시 촬영 및 비디오 녹화는 금지되어 있습니다.", "english": "Sorry, but flash photography and video recording are prohibited to protect the artwork."},
            {"role": "Tourist", "korean": "아, 알겠습니다. 혹시 모자나 선글라스를 쓴 채로 입장하는 건 되나요?", "english": "Oh, I see. Is it allowed to enter wearing a hat or sunglasses?"},
            {"role": "Staff", "korean": "예의를 위해 성당 안에서는 모자를 벗어주셔야 합니다.", "english": "To show respect, you must take off your hat inside the cathedral."}
        ],
        "expressions": [
            {"korean": "금지된", "english": "prohibited / forbidden"},
            {"korean": "경의를 표하다", "english": "show respect"},
            {"korean": "플래시 촬영", "english": "flash photography"}
        ]
    },

    # 테마 8: 문제 및 긴급 상황 (71~80)
    71: {
        "title": "지갑/소지품 분실 신고",
        "dialogue": [
            {"role": "Victim", "korean": "도와주세요! 누군가 제 핸드백과 지갑을 훔쳐갔어요.", "english": "Help! Someone stole my handbag and wallet."},
            {"role": "Officer", "korean": "침착하세요. 어디서 잃어버리셨는지 기억하시나요?", "english": "Calm down, please. Do you remember where you lost it?"},
            {"role": "Victim", "korean": "기차역 매표소 앞 줄 서 있는 동안 소매치기를 당한 것 같아요.", "english": "I think I was pickpocketed while standing in line at the train station ticket office."},
            {"role": "Officer", "korean": "피해 조사 보고서를 작성해 드릴 테니 카드 분실 신고부터 하세요.", "english": "I'll fill out a police report for you, but please freeze your credit cards first."}
        ],
        "expressions": [
            {"korean": "물건을 도둑맞다", "english": "stole / pickpocketed"},
            {"korean": "도난/분실 신고서", "english": "police report / theft report"},
            {"korean": "카드를 분실/정지시키다", "english": "freeze credit cards"}
        ]
    },
    72: {
        "title": "여권 분실 및 대사관",
        "dialogue": [
            {"role": "Victim", "korean": "여권을 분실했습니다. 여행증명서를 발급받고 싶습니다.", "english": "I lost my passport. I'd like to get an emergency travel certificate."},
            {"role": "Embassy Staff", "korean": "네, 여권용 사진 두 장과 신분증, 그리고 여권 번호가 있으신가요?", "english": "Alright. Do you have two passport-sized photos, your ID card, and your passport number?"},
            {"role": "Victim", "korean": "다행히 폰에 찍어둔 여권 사진 사본과 한국 운전면허증이 있습니다.", "english": "Fortunately, I have a photo copy of my passport on my phone and my Korean driver's license."},
            {"role": "Embassy Staff", "korean": "좋습니다. 도난 신고서 증명서와 함께 신청서를 작성해 주세요.", "english": "Great. Please fill out the application form along with your police report certificate."}
        ],
        "expressions": [
            {"korean": "여권을 잃어버리다", "english": "lost my passport"},
            {"korean": "긴급 여행증명서", "english": "emergency travel certificate"},
            {"korean": "여권 사본", "english": "copy of passport"}
        ]
    },
    73: {
        "title": "길에서 소매치기",
        "dialogue": [
            {"role": "Victim", "korean": "저기요! 도둑이야! 내 가방을 가지고 도망치고 있어요!", "english": "Hey! Thief! He's running away with my bag!"},
            {"role": "Passerby", "korean": "무슨 일인가요? 경찰을 불러 드릴까요?", "english": "What happened? Should I call the police?"},
            {"role": "Victim", "korean": "네, 제발 911에 바로 전화해 주세요! 저 빨간 후드티를 입은 남자예요.", "english": "Yes, please call 911 right now! It's that man in the red hoodie."},
            {"role": "Passerby", "korean": "경찰에 신고했습니다. 곧 출동할 겁니다.", "english": "I've called the police. They will be here shortly."}
        ],
        "expressions": [
            {"korean": "도둑이다!", "english": "Thief! / Stop, thief!"},
            {"korean": "경찰을 부르다", "english": "call the police / dial 911"},
            {"korean": "도망치다", "english": "run away / flee"}
        ]
    },
    74: {
        "title": "신체 통증 설명",
        "dialogue": [
            {"role": "Patient", "korean": "어젯밤부터 배가 너무 아프고 열이 납니다.", "english": "My stomach hurts terribly, and I've had a fever since last night."},
            {"role": "Pharmacist", "korean": "식중독(Food poisoning) 증상일 수 있습니다. 설사도 동반하시나요?", "english": "It could be food poisoning. Do you also have diarrhea?"},
            {"role": "Patient", "korean": "네, 심한 설사와 구토도 하고 있습니다.", "english": "Yes, I have severe diarrhea and vomiting too."},
            {"role": "Pharmacist", "korean": "이 약들을 드시고, 상태가 좋아지지 않으면 큰 병원 응급실로 가보세요.", "english": "Take these medicines, and if it doesn't get better, go to the hospital emergency room."}
        ],
        "expressions": [
            {"korean": "배탈 / 식중독", "english": "stomachache / food poisoning"},
            {"korean": "구토 및 설사", "english": "vomiting and diarrhea"},
            {"korean": "응급실", "english": "emergency room (ER)"}
        ]
    },
    75: {
        "title": "병원 진료 및 의사",
        "dialogue": [
            {"role": "Doctor", "korean": "어디가 아프신가요? 한국어 통역이 필요하신가요?", "english": "Where does it hurt? Do you need a Korean interpreter?"},
            {"role": "Patient", "korean": "계단을 내려오다 발목을 접질렸어요. 걷지를 못하겠습니다.", "english": "I sprained my ankle while walking down the stairs. I cannot walk."},
            {"role": "Doctor", "korean": "뼈가 부러졌는지 확인하기 위해 엑스레이를 촬영해 봐야겠습니다.", "english": "We need to take an X-ray to check if the bone is broken."},
            {"role": "Patient", "korean": "여행자 보험 청구용 진단서와 의료비 영수증을 끊어 주실 수 있나요?", "english": "Can you issue a medical certificate and itemized bill for my travel insurance claim?"}
        ],
        "expressions": [
            {"korean": "발목을 삐다", "english": "sprain one's ankle"},
            {"korean": "엑스레이를 찍다", "english": "take an X-ray"},
            {"korean": "여행자 보험 청구 서류", "english": "medical certificate for travel insurance"}
        ]
    },
    76: {
        "title": "처방전으로 약 구매",
        "dialogue": [
            {"role": "Patient", "korean": "병원에서 받은 처방전이 있습니다. 약을 지어주세요.", "english": "I have a prescription from the hospital. Please fill this prescription."},
            {"role": "Pharmacist", "korean": "네, 처방 약을 준비해 드리겠습니다. 복용법을 아시나요?", "english": "Okay, I will prepare your medicine. Do you know how to take it?"},
            {"role": "Patient", "korean": "아니요, 어떻게 먹어야 하나요?", "english": "No, how should I take it?"},
            {"role": "Pharmacist", "korean": "하루 세 번, 식후 30분에 한 알씩 따뜻한 물과 함께 드세요.", "english": "Take one pill three times a day, 30 minutes after meals, with warm water."}
        ],
        "expressions": [
            {"korean": "처방전", "english": "prescription"},
            {"korean": "약을 조제하다", "english": "fill a prescription"},
            {"korean": "식사 후에 복용하다", "english": "take after meals"}
        ]
    },
    77: {
        "title": "교통사고 발생",
        "dialogue": [
            {"role": "Driver", "korean": "차끼리 부딪혔습니다! 뒤에서 제 차를 들이받으셨어요.", "english": "We've crashed! You rear-ended my car from behind."},
            {"role": "Passenger", "korean": "정말 죄송합니다. 다치신 분은 없나요?", "english": "I'm so sorry. Is anyone injured?"},
            {"role": "Driver", "korean": "목이 뻐근하네요. 일단 보험사(Insurance)와 경찰을 부릅시다.", "english": "My neck feels stiff. Let's call the insurance company and the police first."},
            {"role": "Passenger", "korean": "네, 렌터카 업체에도 바로 연락해서 사고 접수를 하겠습니다.", "english": "Yes, I will also contact the rental car company to report the accident immediately."}
        ],
        "expressions": [
            {"korean": "뒤에서 차를 들이받다", "english": "rear-end a car"},
            {"korean": "부상을 입은", "english": "injured / hurt"},
            {"korean": "사고 보고서 접수", "english": "report the accident / claim"}
        ]
    },
    78: {
        "title": "화재 발생 대피",
        "dialogue": [
            {"role": "Guest", "korean": "불이야! 연기가 복도에 가득 차 있어요. 비상구는 어디에 있나요?", "english": "Fire! The hallway is filled with smoke. Where is the emergency exit?"},
            {"role": "Staff", "korean": "엘리베이터를 타지 마시고 복도 끝 계단을 이용해 내려가세요!", "english": "Do not take the elevator! Use the stairs at the end of the hallway to go down!"},
            {"role": "Guest", "korean": "방 안에 중요한 여권과 소지품이 들어있는데 두고 가야 하나요?", "english": "My passport and valuables are in the room. Should I leave them behind?"},
            {"role": "Staff", "korean": "생명이 먼저입니다! 아무것도 챙기지 마시고 즉시 대피하세요!", "english": "Life comes first! Leave everything and evacuate immediately!"}
        ],
        "expressions": [
            {"korean": "비상 탈출구", "english": "emergency exit"},
            {"korean": "즉시 대피하다", "english": "evacuate immediately"},
            {"korean": "연기로 가득 찬", "english": "filled with smoke"}
        ]
    },
    79: {
        "title": "동행을 잃어버림",
        "dialogue": [
            {"role": "Tourist", "korean": "실례합니다, 제 아이가 군중 속에서 보이지 않아요. 미아가 되었습니다.", "english": "Excuse me, I can't find my child in the crowd. My child is lost."},
            {"role": "Officer", "korean": "진정하시고 아이의 인상착의를 말씀해 주실래요?", "english": "Calm down and tell me what your child looks like, please."},
            {"role": "Tourist", "korean": "7살 남아이고 노란색 티셔츠에 파란색 반바지를 입고 있어요. 이름은 민우입니다.", "english": "He's a 7-year-old boy, wearing a yellow t-shirt and blue shorts. His name is Minwoo."},
            {"role": "Officer", "korean": "안내 방송(Announcement)을 즉시 띄우고 근처 요원들에게 수색을 지시하겠습니다.", "english": "I'll make an announcement immediately and instruct security officers nearby to search."}
        ],
        "expressions": [
            {"korean": "미아 / 아이를 잃다", "english": "lost child / missing child"},
            {"korean": "인상착의", "english": "description / what someone looks like"},
            {"korean": "안내 방송", "english": "public announcement / broadcast"}
        ]
    },
    80: {
        "title": "긴급 경찰 호출",
        "dialogue": [
            {"role": "Caller", "korean": "도와주세요! 낯선 남자가 호텔 문을 강제로 열려고 합니다.", "english": "Help! A stranger is trying to force open my hotel room door."},
            {"role": "Dispatcher", "korean": "긴급 상황이군요. 현재 호텔 이름과 호실 번호가 어떻게 되나요?", "english": "This is an emergency. What is your hotel name and room number?"},
            {"role": "Caller", "korean": "그랜드 쉐라톤 호텔 1204호입니다! 문고리를 마구 흔들고 있어요.", "english": "Grand Sheraton Hotel, room 1204! He is shaking the doorknob violently."},
            {"role": "Dispatcher", "korean": "가장 가까운 순찰차를 즉시 보냈습니다. 절대로 문을 열지 마세요.", "english": "I've dispatched the nearest patrol car. Under no circumstances open the door."}
        ],
        "expressions": [
            {"korean": "강제로 문을 열다", "english": "force open the door"},
            {"korean": "경찰차를 출동시키다", "english": "dispatch a patrol car"},
            {"korean": "어떤 일이 있어도(절대로)", "english": "under no circumstances"}
        ]
    },

    # 테마 9: 일상 대화 및 친교 (81~90)
    81: {
        "title": "가벼운 인사 및 자기소개",
        "dialogue": [
            {"role": "Stranger", "korean": "안녕하세요, 날씨가 정말 화창하죠? 저는 톰이라고 합니다.", "english": "Hello, beautiful weather, isn't it? I'm Tom."},
            {"role": "Me", "korean": "반갑습니다, 톰. 저는 한국에서 온 김재우라고 합니다.", "english": "Nice to meet you, Tom. I'm Jaewoo Kim from Korea."},
            {"role": "Stranger", "korean": "한국이군요! 여기에 여행하러 오신 건가요?", "english": "Oh, Korea! Are you here for traveling?"},
            {"role": "Me", "korean": "네, 첫 배낭여행이라 무척 신납니다.", "english": "Yes, this is my first backpacking trip, so I'm very excited."}
        ],
        "expressions": [
            {"korean": "처음 뵙겠습니다", "english": "Nice to meet you"},
            {"korean": "배낭여행", "english": "backpacking trip"},
            {"korean": "무척 신나는", "english": "very excited"}
        ]
    },
    82: {
        "title": "출신 국가 및 여행 기간",
        "dialogue": [
            {"role": "Friend", "korean": "여기 머문 지 얼마나 되셨어요?", "english": "How long have you been staying here?"},
            {"role": "Me", "korean": "사흘째입니다. 다음 주 수요일에 다른 도시로 떠나요.", "english": "It's my third day. I'm leaving for another city next Wednesday."},
            {"role": "Friend", "korean": "이 도시 마음에 드시나요? 어디가 가장 인상 깊었나요?", "english": "Do you like this city? What has been the most impressive place?"},
            {"role": "Me", "korean": "야경이 정말 멋져요. 특히 어젯밤에 본 강가 뷰가 잊히지 않네요.", "english": "The night view is wonderful. Especially, the river view I saw last night is unforgettable."}
        ],
        "expressions": [
            {"korean": "사흘 동안", "english": "for three days / my third day"},
            {"korean": "인상 깊은", "english": "impressive"},
            {"korean": "잊을 수 없는", "english": "unforgettable"}
        ]
    },
    83: {
        "title": "직업 및 관심사",
        "dialogue": [
            {"role": "Friend", "korean": "한국에서는 무슨 일을 하시나요?", "english": "What do you do for a living in Korea?"},
            {"role": "Me", "korean": "저는 IT 회사에서 소프트웨어 엔지니어로 일하고 있습니다. 당신은요?", "english": "I work as a software engineer at an IT company. How about you?"},
            {"role": "Friend", "korean": "저는 대학에서 디자인을 공부하고 있는 학생입니다.", "english": "I'm a student studying design at university."},
            {"role": "Me", "korean": "멋지네요! 저도 디자인이나 미술 전시회 관람을 무척 좋아합니다.", "english": "Cool! I also love visiting design and art exhibitions."}
        ],
        "expressions": [
            {"korean": "무슨 일 하세요?(직업)", "english": "What do you do for a living? / What is your job?"},
            {"korean": "전시회를 관람하다", "english": "visit / view exhibitions"},
            {"korean": "소프트웨어 개발자", "english": "software engineer / developer"}
        ]
    },
    84: {
        "title": "날씨 이야기",
        "dialogue": [
            {"role": "Friend", "korean": "오늘 일기예보를 보니 오후에 비가 올 확률이 높대요.", "english": "According to the weather forecast, there's a high chance of rain this afternoon."},
            {"role": "Me", "korean": "정말요? 우산을 챙기지 않았는데 빌려야겠네요.", "english": "Really? I didn't bring an umbrella, so I should borrow one."},
            {"role": "Friend", "korean": "제가 여분의 우산이 차에 있으니 필요하면 빌려 드릴게요.", "english": "I have a spare umbrella in my car, so I can lend it to you if you need."},
            {"role": "Me", "korean": "와, 구세주 같네요! 빌려 주시면 유용하게 쓰고 돌려드릴게요.", "english": "Wow, you're a lifesaver! I'll make good use of it and return it."}
        ],
        "expressions": [
            {"korean": "일기예보", "english": "weather forecast"},
            {"korean": "우산을 빌려주다", "english": "lend an umbrella"},
            {"korean": "여분의(남는)", "english": "spare / extra"}
        ]
    },
    85: {
        "title": "맛집 정보 교환",
        "dialogue": [
            {"role": "Me", "korean": "이 근처에 현지인들이 자주 가는 숨겨진 맛집을 아시나요?", "english": "Do you know any hidden gem restaurants near here that locals frequent?"},
            {"role": "Friend", "korean": "골목 뒤편에 끝내주는 파스타 집이 있어요. 관광객은 거의 없고 가격도 저렴합니다.", "english": "There's an amazing pasta place right behind the alley. Hard to find tourists and it's cheap."},
            {"role": "Me", "korean": "거기 이름이 무엇인가요? 메뉴판은 영어로 되어 있나요?", "english": "What is the name of the place? Is the menu available in English?"},
            {"role": "Friend", "korean": "이름은 '라 파스타'이고 영어 메뉴판도 구비되어 있습니다.", "english": "It's called 'La Pasta' and they do have English menus."}
        ],
        "expressions": [
            {"korean": "숨겨진 맛집", "english": "hidden gem restaurant"},
            {"korean": "현지인 단골집", "english": "locals' favorite / frequent"},
            {"korean": "영어 메뉴판이 구비된", "english": "English menu is available"}
        ]
    },
    86: {
        "title": "연락처/SNS 교환",
        "dialogue": [
            {"role": "Me", "korean": "즐거운 시간이었어요. 혹시 실례가 안 된다면 SNS 계정을 공유해 주실 수 있나요?", "english": "I had a great time. If you don't mind, could we exchange SNS accounts?"},
            {"role": "Friend", "korean": "좋죠! 제 인스타그램 계정은 @travel_tom 입니다. 맞팔해요.", "english": "Sure! My Instagram handle is @travel_tom. Let's follow each other."},
            {"role": "Me", "korean": "네, 방금 팔로우했습니다. 나중에 한국에 오시면 제가 꼭 가이드 해드릴게요.", "english": "Great, I just followed you. If you visit Korea later, I'll definitely show you around."},
            {"role": "Friend", "korean": "기대할게요! 연락 계속 주고받아요.", "english": "I look forward to it! Let's keep in touch."}
        ],
        "expressions": [
            {"korean": "SNS 계정(아이디)", "english": "Instagram handle / social media account"},
            {"korean": "서로 맞팔로우하다", "english": "follow each other / follow back"},
            {"korean": "연락하며 지내다", "english": "keep in touch"}
        ]
    },
    87: {
        "title": "약속 잡기 및 조율",
        "dialogue": [
            {"role": "Friend", "korean": "내일 저녁 같이 먹는 건 어때요? 시간 비어 있으신가요?", "english": "How about having dinner together tomorrow night? Are you free?"},
            {"role": "Me", "korean": "좋습니다! 오후 6시 이후에는 언제든 괜찮아요. 어디서 만날까요?", "english": "Sounds good! I'm free anytime after 6 PM. Where should we meet?"},
            {"role": "Friend", "korean": "시내 광장 분수대 앞에서 만나서 같이 식당으로 이동하시죠.", "english": "Let's meet in front of the downtown square fountain and walk to the restaurant together."},
            {"role": "Me", "korean": "완벽하네요. 내일 6시 반에 분수대 앞에서 뵙겠습니다.", "english": "Perfect. I'll see you at the fountain at 6:30 PM tomorrow."}
        ],
        "expressions": [
            {"korean": "시간이 비어 있는", "english": "free / available"},
            {"korean": "광장 분수대", "english": "square fountain"},
            {"korean": "내일 만나요", "english": "I'll see you tomorrow"}
        ]
    },
    88: {
        "title": "감사 인사 및 작별",
        "dialogue": [
            {"role": "Me", "korean": "도와주셔서 정말 감사합니다. 당신 덕분에 여행이 한결 수월했습니다.", "english": "Thank you so much for your help. You made my trip a lot easier."},
            {"role": "Friend", "korean": "천만에요. 저도 좋은 친구를 사귀어 매우 기뻤습니다.", "english": "My pleasure. I was also very glad to make a good friend."},
            {"role": "Me", "korean": "이제 비행기 탑승 시간이 다 되었네요. 몸 조심하고 잘 지내세요.", "english": "Now it's time to board my flight. Take care and stay well."},
            {"role": "Friend", "korean": "조심히 들어가세요! 좋은 여행이 되었기를 바랍니다.", "english": "Have a safe flight! I hope you had a wonderful trip."}
        ],
        "expressions": [
            {"korean": "여행이 한결 수월한", "english": "made my trip a lot easier"},
            {"korean": "천만에요(기쁨)", "english": "My pleasure / Don't mention it"},
            {"korean": "몸 조심해(잘 가)", "english": "Take care / Have a safe flight"}
        ]
    },
    89: {
        "title": "칭찬하기",
        "dialogue": [
            {"role": "Me", "korean": "그 재킷 정말 멋지네요! 어디서 구매하셨나요?", "english": "That jacket looks amazing on you! Where did you get it?"},
            {"role": "Friend", "korean": "감사합니다! 빈티지 샵에서 저렴하게 구했어요.", "english": "Thank you! I got it cheap at a local vintage shop."},
            {"role": "Me", "korean": "정말 센스가 있으시네요. 당신의 스타일이 아주 잘 어울립니다.", "english": "You have a great sense of style. It suits you really well."},
            {"role": "Friend", "korean": "과찬이십니다. 재우 씨도 오늘 패션이 깔끔하고 좋아 보여요.", "english": "I'm flattered. You also look neat and sharp today, Jaewoo."}
        ],
        "expressions": [
            {"korean": "아주 잘 어울리다", "english": "looks amazing / suits you well"},
            {"korean": "빈티지 샵", "english": "vintage shop"},
            {"korean": "센스가 있는", "english": "great sense of style / fashionable"}
        ]
    },
    90: {
        "title": "도움 제안 및 사양",
        "dialogue": [
            {"role": "Passerby", "korean": "가방이 아주 무거워 보이네요. 계단 올라가는데 도와드릴까요?", "english": "Your bag looks very heavy. Shall I help you carry it up the stairs?"},
            {"role": "Me", "korean": "아, 괜찮습니다. 혼자서도 충분히 들 수 있어요. 마음만 감사히 받겠습니다.", "english": "Oh, no thank you. I can manage by myself. I appreciate your kindness."},
            {"role": "Passerby", "korean": "정말 괜찮으신가요? 꽤 가파른 계단인데요.", "english": "Are you sure? These stairs are quite steep."},
            {"role": "Me", "korean": "천천히 가며 쉬어가면 됩니다. 호의를 베풀어 주셔서 고맙습니다.", "english": "I'll just take it slow. Thank you for offering your help."}
        ],
        "expressions": [
            {"korean": "혼자서 감당하다", "english": "manage by myself / do it myself"},
            {"korean": "친절에 감사하다", "english": "appreciate your kindness / offer"},
            {"korean": "가파른 계단", "english": "steep stairs"}
        ]
    },

    # 테마 10: 귀국 및 면세 신고 (91~100)
    91: {
        "title": "항공편 일정 변경 문의",
        "dialogue": [
            {"role": "Passenger", "korean": "서울행 비행기 좌석을 하루 연기하여 변경하고 싶습니다.", "english": "I'd like to postpone my flight to Seoul by one day."},
            {"role": "Agent", "korean": "확인해 보니 변경 가능한 자리가 있습니다만, 수수료가 발생합니다.", "english": "Checking the system... Yes, there is a seat available, but a change fee will apply."},
            {"role": "Passenger", "korean": "날짜 변경 수수료는 얼마인가요?", "english": "How much is the date change fee?"},
            {"role": "Agent", "korean": "수수료는 100달러이며 차액 지불이 추가로 필요할 수 있습니다.", "english": "The fee is 100 dollars, and additional fare difference may be required."}
        ],
        "expressions": [
            {"korean": "항공편을 연기하다", "english": "postpone a flight / delay flight"},
            {"korean": "날짜 변경 수수료", "english": "change fee"},
            {"korean": "항공 운임 차액", "english": "fare difference"}
        ]
    },
    92: {
        "title": "공항 샌딩 서비스 예약",
        "dialogue": [
            {"role": "Guest", "korean": "호텔에서 공항까지 샌딩 서비스를 제공하나요?", "english": "Does the hotel provide a transfer service to the airport?"},
            {"role": "Receptionist", "korean": "네, 프라이빗 셔틀밴 서비스를 예약해 드릴 수 있습니다. 요금은 50달러입니다.", "english": "Yes, we can book a private shuttle van service for you. The fare is 50 dollars."},
            {"role": "Guest", "korean": "비행기가 아침 9시 출발인데, 몇 시에 출발하는 밴을 타야 할까요?", "english": "My flight departs at 9 AM. What time should the van pick me up?"},
            {"role": "Receptionist", "korean": "국제선은 3시간 전 도착이 권장되므로, 새벽 5시 반에 탑승하시는 것이 좋습니다.", "english": "As international flights recommend arriving 3 hours early, boarding at 5:30 AM is advised."}
        ],
        "expressions": [
            {"korean": "공항 픽업/샌딩", "english": "airport transfer / shuttle service"},
            {"korean": "차량을 타다", "english": "pick up / board"},
            {"korean": "국제선 노선", "english": "international flight"}
        ]
    },
    93: {
        "title": "공항 카운터 체크인 및 위탁 수하물",
        "dialogue": [
            {"role": "Agent", "korean": "안녕하세요, 여권과 예약 정보를 주시겠어요?", "english": "Hello, may I have your passport and booking reference, please?"},
            {"role": "Passenger", "korean": "네, 여기 있습니다. 보내는 수하물(위탁 가방)은 두 개입니다.", "english": "Yes, here they are. I have two bags to check in."},
            {"role": "Agent", "korean": "가방을 저울 위에 하나씩 올려주세요. 깨질 위험이 있는 물건이나 배터리가 들어있나요?", "english": "Please place your bags on the scale one by one. Do they contain fragile items or batteries?"},
            {"role": "Passenger", "korean": "없습니다. 모두 일반 의류와 세면도구입니다.", "english": "No, they don't. Everything is just clothing and toiletries."}
        ],
        "expressions": [
            {"korean": "예약 번호(정보)", "english": "booking reference / reservation code"},
            {"korean": "가방을 부치다", "english": "check in bags / checked luggage"},
            {"korean": "깨지기 쉬운 물건", "english": "fragile items"}
        ]
    },
    94: {
        "title": "위탁 수하물 무게 초과",
        "dialogue": [
            {"role": "Agent", "korean": "죄송하지만, 이 가방은 무료 허용 한도인 23kg을 3kg 초과했습니다.", "english": "Sorry, but this bag exceeds the free limit of 23kg by 3kg."},
            {"role": "Passenger", "korean": "초과 요금은 얼마인가요? 꽤 많이 비싼가요?", "english": "How much is the excess baggage fee? Is it very expensive?"},
            {"role": "Agent", "korean": "추가로 50달러를 내셔야 합니다. 혹은 짐을 기내용 가방으로 옮기셔도 됩니다.", "english": "You'll need to pay an extra 50 dollars. Or you can transfer some items to your carry-on bag."},
            {"role": "Passenger", "korean": "그럼 가방을 열어 무거운 책 몇 권을 기내 가방으로 옮겨 담겠습니다.", "english": "Then I'll open the suitcase and move some heavy books to my carry-on."}
        ],
        "expressions": [
            {"korean": "무게를 초과하다", "english": "exceed the limit / overweight"},
            {"korean": "수하물 초과 요금", "english": "excess baggage fee"},
            {"korean": "기내 휴대용 가방", "english": "carry-on bag / hand luggage"}
        ]
    },
    95: {
        "title": "출국 심사 및 보안 검색",
        "dialogue": [
            {"role": "Officer", "korean": "자켓을 벗으시고 주머니의 모든 물건을 바구니에 담아주세요.", "english": "Please take off your jacket and put all items from your pockets into the bin."},
            {"role": "Passenger", "korean": "노트북 컴퓨터와 액체류도 가방에서 꺼내야 하나요?", "english": "Do I need to take out my laptop and liquids from the bag?"},
            {"role": "Officer", "korean": "네, 노트북은 가방에서 꺼내 별도 바구니에 담고, 액체류는 지퍼백에 넣어 꺼내주세요.", "english": "Yes, take the laptop out of the bag into a separate bin, and put liquids in a clear plastic bag."},
            {"role": "Passenger", "korean": "알겠습니다. 벨트도 풀어야 하나요?", "english": "Understood. Should I take off my belt too?"}
        ],
        "expressions": [
            {"korean": "보안 검색 바구니", "english": "bin / tray"},
            {"korean": "가방에서 꺼내다", "english": "take out of / extract"},
            {"korean": "보안 요원", "english": "security officer"}
        ]
    },
    96: {
        "title": "공항 내 택스 리펀 창구",
        "dialogue": [
            {"role": "Passenger", "korean": "텍스 리펀을 받으려면 어디로 가야 하나요?", "english": "Where should I go to get my tax refund?"},
            {"role": "Officer", "korean": "보안 검색을 통과하기 전, 12번 게이트 옆 세관 데스크로 도장을 먼저 받으러 가세요.", "english": "Before passing security, go to the customs desk next to Gate 12 to get a stamp first."},
            {"role": "Passenger", "korean": "환급은 현금으로 받나요, 카드로 받나요?", "english": "Do I get the refund in cash or back to my credit card?"},
            {"role": "Officer", "korean": "원하시는 형태로 신청 서류에 체크하시면 처리해 드립니다.", "english": "Just check your preferred option on the form, and they will process it."}
        ],
        "expressions": [
            {"korean": "세관 세관 도장", "english": "customs stamp"},
            {"korean": "세금 환급 데스크", "english": "tax refund desk / office"},
            {"korean": "카드로 환급 받다", "english": "refund back to credit card"}
        ]
    },
    97: {
        "title": "면세점 및 인도장 찾기",
        "dialogue": [
            {"role": "Passenger", "korean": "인터넷 면세점에서 미리 구매한 물건의 인도장은 어디에 있나요?", "english": "Where is the duty-free pick-up desk for items purchased online?"},
            {"role": "Staff", "korean": "26번 게이트 맞은편 에스컬레이터를 타고 4층으로 올라가시면 인도장이 있습니다.", "english": "Take the escalator opposite Gate 26 up to the 4th floor, and you'll find the pick-up desk."},
            {"role": "Passenger", "korean": "교환권을 보여주면 바로 수령할 수 있나요?", "english": "Can I pick it up immediately if I show the exchange voucher?"},
            {"role": "Staff", "korean": "네, 교환권 번호표와 여권을 직원에게 보여주시면 인도해 드립니다.", "english": "Yes, show the exchange voucher number and your passport to the staff, and they will hand it over."}
        ],
        "expressions": [
            {"korean": "면세품 인도장", "english": "duty-free pick-up desk / counter"},
            {"korean": "교환권(영수증)", "english": "exchange voucher / receipt"},
            {"korean": "면세점", "english": "duty-free shop"}
        ]
    },
    98: {
        "title": "비행기 탑승 게이트 변경",
        "dialogue": [
            {"role": "Passenger", "korean": "실례합니다, KE082편의 탑승 게이트가 변경되었다는 안내 방송을 들었는데요.", "english": "Excuse me, I heard an announcement that the boarding gate for flight KE082 has changed."},
            {"role": "Staff", "korean": "네, 기상 악화로 게이트가 기존 15번에서 42번으로 변경되었습니다.", "english": "Yes, due to bad weather, the gate has been changed from 15 to 42."},
            {"role": "Passenger", "korean": "탑승 시간도 연기되었나요?", "english": "Has the boarding time been delayed as well?"},
            {"role": "Staff", "korean": "아니요, 탑승 시간은 원래대로 5시 40분부터 시작되니 서둘러 가시는 것이 좋습니다.", "english": "No, boarding will start at 5:40 PM as scheduled, so you'd better hurry there."}
        ],
        "expressions": [
            {"korean": "탑승 게이트 변경", "english": "gate change"},
            {"korean": "기상 악화", "english": "bad weather / severe weather"},
            {"korean": "예정대로", "english": "as scheduled / on time"}
        ]
    },
    99: {
        "title": "기내 휴대 수하물 정리",
        "dialogue": [
            {"role": "Passenger", "korean": "이 가방을 좌석 위 선반(overhead bin)에 넣어주실 수 있나요?", "english": "Could you help me put this bag in the overhead bin?"},
            {"role": "Flight Attendant", "korean": "물론입니다. 가방이 꽤 무거우니 조심해서 올려드리겠습니다.", "english": "Certainly. The bag is quite heavy, so I'll lift it carefully for you."},
            {"role": "Passenger", "korean": "감사합니다. 비행 중 필요한 책 한 권은 미리 꺼내 놓았어요.", "english": "Thank you. I've already taken out a book I need during the flight."},
            {"role": "Flight Attendant", "korean": "좋습니다. 통로에 짐이 튀어나오지 않도록 선반 문을 닫아두겠습니다.", "english": "Great. I will close the bin door to make sure no bags protrude into the aisle."}
        ],
        "expressions": [
            {"korean": "머리 위 선반", "english": "overhead bin / compartment"},
            {"korean": "통로 쪽으로 튀어나오다", "english": "protrude into the aisle"},
            {"korean": "~을 꺼내놓다", "english": "take out"}
        ]
    },
    100: {
        "title": "한국 입국 및 세관 자진 신고",
        "dialogue": [
            {"role": "Customs Officer", "korean": "해외에서 구매하신 물품 중 면세 한도 800달러를 초과하는 품목이 있으십니까?", "english": "Do you have any items purchased abroad that exceed the duty-free limit of 800 dollars?"},
            {"role": "Passenger", "korean": "네, 프랑스에서 1,200달러짜리 가방을 사서 자진 신고서에 작성했습니다.", "english": "Yes, I bought a bag for 1,200 dollars in France and declared it on this form."},
            {"role": "Customs Officer", "korean": "자진 신고해 주셔서 감사합니다. 세금 감면 혜택을 적용해서 고지서를 발급해 드리겠습니다.", "english": "Thank you for declaring. We will apply a tax reduction and issue the bill."},
            {"role": "Passenger", "korean": "감사합니다. 납부는 모바일로 해도 되나요?", "english": "Thank you. Can I pay the tax online via mobile?"}
        ],
        "expressions": [
            {"korean": "면세 한도", "english": "duty-free limit / allowance"},
            {"korean": "자진 신고하다", "english": "declare voluntarily"},
            {"korean": "세금 감면", "english": "tax reduction / deduction"}
        ]
    }
}

# 긴급 상황용 검색 데이터 (emergency_phrases)
emergency_phrases = [
    {
        "id": 1,
        "category": "여권/신분증 분실",
        "korean": "여권을 잃어버렸어요. 한국 대사관은 어디인가요?",
        "english": "I lost my passport. Where is the Korean embassy?",
        "keywords": "여권 분실 패스포트 대사관 한국 영사관 잃어버림"
    },
    {
        "id": 2,
        "category": "길 잃음/교통",
        "korean": "여기가 어디인지 모르겠어요. 길을 잃었습니다.",
        "english": "I don't know where I am. I am lost.",
        "keywords": "길 헤맴 미아 길치 지도 길잃음 어디"
    },
    {
        "id": 3,
        "category": "건강/의료",
        "korean": "배가 아파서 죽겠어요. 근처에 병원이나 약국이 있나요?",
        "english": "My stomach hurts so much. Is there a hospital or pharmacy nearby?",
        "keywords": "아픔 아파 배탈 병원 약국 약 메스꺼움 두통 열"
    },
    {
        "id": 4,
        "category": "도난/범죄",
        "korean": "누군가 내 지갑을 훔쳐갔어요! 도둑 잡아주세요!",
        "english": "Someone stole my wallet! Stop the thief!",
        "keywords": "지갑 도둑 소매치기 강도 털림 백 지갑 잃어버림 분실 훔쳐"
    },
    {
        "id": 5,
        "category": "긴급 구조",
        "korean": "도와주세요! 119/911을 불러주세요! 응급 상황입니다.",
        "english": "Help me! Please call 911! It's an emergency.",
        "keywords": "도움 헬프 응급 구조 경찰 화재 불 구급차"
    },
    {
        "id": 6,
        "category": "숙소 문제",
        "korean": "방에 에어컨(히터)이 켜지지 않아요. 고장 났습니다.",
        "english": "The air conditioner (heater) won't turn on in my room. It is broken.",
        "keywords": "에어컨 히터 고장 춥다 덥다 방 숙소 수리 안돼"
    },
    {
        "id": 7,
        "category": "식사 결제",
        "korean": "계산서에 잘못 청구된 금액이 있는 것 같습니다.",
        "english": "I think there is a mistake on the bill.",
        "keywords": "계산 빌지 영수증 잘못 청구 에러 실수 금액"
    },
    {
        "id": 8,
        "category": "교통편 놓침",
        "korean": "비행기/기차를 놓쳤어요. 다음 편으로 바꿀 수 있나요?",
        "english": "I missed my flight/train. Can I reschedule for the next one?",
        "keywords": "비행기 기차 놓침 늦음 딜레이 취소 지연 티켓 변경"
    },
    {
        "id": 9,
        "category": "알레르기",
        "korean": "땅콩/견과류 알레르기가 있어요. 음식에 빼주세요.",
        "english": "I have a peanut/nut allergy. Please exclude it from my food.",
        "keywords": "알레르기 땅콩 견과류 못먹음 알러지 음식 제외"
    },
    {
        "id": 10,
        "category": "통역 요청",
        "korean": "한국어 통역관이나 한국어가 가능한 직원을 불러주실 수 있나요?",
        "english": "Could you call a Korean interpreter or someone who speaks Korean?",
        "keywords": "통역 한국어 번역 소통 직원 도움"
    }
]

# 100일 분량으로 시나리오 매핑하여 days 배열 만들기
# 1~100일까지 테마 10개를 순서대로 10일씩 분배
for i in range(1, 101):
    theme_idx = (i - 1) // 10
    theme_title = themes[theme_idx]
    
    # 시나리오 매칭 (정의된 100일 시나리오가 있으면 그것을 사용, 
    # 만약 시나리오 정의 과정에 구멍이 있거나 하면 디폴트 데이터 생성)
    if i in scenarios:
        sc = scenarios[i]
        day_entry = {
            "day_id": i,
            "theme": theme_title,
            "title": f"Day {i}: {sc['title']}",
            "dialogue": sc["dialogue"],
            "expressions": sc["expressions"]
        }
    else:
        # 대비용 백업 생성 로직 (혹시나 에러 방지)
        day_entry = {
            "day_id": i,
            "theme": theme_title,
            "title": f"Day {i}: 여행 상황 대화 {i}",
            "dialogue": [
                {"role": "A", "korean": "안녕하세요, 여행 중 사용할 영어를 배우고 있습니다.", "english": "Hello, I am learning English to use during travel."},
                {"role": "B", "korean": "좋습니다. 매일 연습하면 큰 도움이 될 것입니다.", "english": "That's great. Practicing every day will help a lot."}
            ],
            "expressions": [
                {"korean": "연습하다", "english": "practice"},
                {"korean": "매일", "english": "every day"}
            ]
        }
    days_data.append(day_entry)

# 결과 묶기
final_data = {
    "days": days_data,
    "emergency_phrases": emergency_phrases
}

# 파일 저장 경로 설정 및 생성
output_dir = "/Users/marco/Documents/workspacke/travel-english/backend/data"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "travel_data.json")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print(f"travel_data.json successfully generated at: {output_path}")
