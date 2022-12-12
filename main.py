import datetime
import json
import os.path
import time

from fastapi import FastAPI
from fastapi import APIRouter

# router = APIRouter()
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
data = {}


def dumps():
    with open('data.txt', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, indent=4))


def loads():
    with open('data.txt', 'r', encoding='utf-8') as f:
        global data
        data = json.loads(f.read())

def isFile():
    if not os.path.isfile('data.txt'):
        f = open('data.txt', 'w', encoding='utf-8')
        f.write('{}')
        f.close()

isFile()
# loads()

def printer():
    print(data)



def storeData(id, gameID,  key, content):
    try:
        data[id]
    except:
        data[id] = {}

    data[id][key] = content
    pushHistory(id, key, gameID)
    dumps()
able = True
def pushHistory(id, key, gameID):
    try:
        # able = False
        for i in data[id]['pushHistory']:
            # print(i)
            if (i['gameID'] == gameID):
                global able
                able = False
                break
            else:
                pass
        if able:
            data[id]['pushHistory'].append({
                'key': key,
                'gameID': gameID
            })
    except:
        data[id]['pushHistory'] = [{
            'key': key,
            'gameID': gameID
        }]


def getHistory(id):
    try:
        return data[id]['pushHistory']
    except:
        return []

def getData(id, key):
    try:
        return data[id][key]
    except:
        return None

def isData(id, key):
    try:
        data[id][key]

    except:
        return False
    return True

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get('//storetime/{userid}')
async def storetime(userid):
    printer()
    if not isData(userid, 'expire'):
        now = datetime.datetime.now()
        expire = now + datetime.timedelta(minutes=20)
        storeData(userid, userid, 'expire', time.mktime(expire.timetuple()))

    return getData(userid, 'expire')

@app.get('//reloaded/{userid}')
async def reloaded(userid):
    his = getHistory(userid)
    print(his)
    return his

ADREV1 = {
            'timeline': "PD",
            'DO': "선생의 감기약을 처방하러 방에 방문하였습니다",
            'PO': "응접실에서 저택 방문을 기념하여 도미노 게임을 진행하였습니다",
            'DE': "응접실에서 저택 방문을 기념하여 도미노 게임을 진행하였습니다",
            'NO': "응접실에서 저택 방문을 기념하여 도미노 게임을 진행하였습니다",
            'EN': "선생의 방 앞에서 선생과 이야기를 나누었습니다",
            'DU': "딸의 교육 방식에 대하여 선생을 문책하였습니다",
            'CA': "기술자와 선생이 선생의 방 앞에서 언성을 높여 이야기하는 것을 보았습니다",
            'TE': False,
        }

ADREV2 = {
            'timeline': 'PN',
            'DO': "선생에게 카드게임을 같이 할 것을 권유하러 방문하였지만, 선생은 창문을 열어 냉기가 가득한 방에서 자고 있었습니다",
            'PO': "공작이 선생의 방문 앞에서 서성거리는 모습을 목격하였습니다",
            'DE': "추리 소설을 읽기 위해 도서관에서 책을 빌리고, 방에서 읽었습니다",
            'NO': "선생에게 카드게임을 같이 할 것을 권유하러 방문하였지만, 선생은 창문을 열어 냉기가 가득한 방에서 자고 있었습니다",
            'EN': "선생에게 카드게임을 같이 할 것을 권유하러 방문하였지만, 선생은 창문을 열어 냉기가 가득한 방에서 자고 있었습니다",
            'DU': "아침에 이야기한 교육 방식에 대한 논의를 마무리하려고 방문하려 하였으나 돌아갔습니다",
            'CA': "집안을 돌아다녔지만, 선생을 목격하지 못하였습니다",
            'TE': False,
        }

RDREV1 = {
            'timeline': 'TN',
            'type': "roomcheck",
            'DO': [
                {
                    'content': "가방 속에 많은 약들과 솜이 있다",
                    'photo': "",
                },
            ],
            'NO': [
                {
                    'content': "캐리어 속에 총기가 들어 있다",
                    'photo': "",
                },
            ],
            'EN': [
                {
                    'content': "아무런 이상이 없다",
                    'photo': "",
                },
            ],
            'PO': [
                {
                    'content': "책상 위에 우울증 약이 놓여 있다",
                    'photo': "",
                },
            ],
            'DE': [
                {
                    'content': "아무런 이상이 없다",
                    'photo': "",
                },
            ],
            'DU': [
                {
                    'content': "아무런 이상이 없다",
                    'photo': "",
                },
            ],
            'CA': [
                {
                    'content': "조사할 수 없다",
                    'photo': "",
                },
            ],
            'TE': [
                {
                    'content': "창문이 열려 있어 방 안으로 눈이 흩날리고 있으며, 매우 춥다",
                    'photo': "",
                },
                {
                    'content': "침대 위에 흩어진 젖은 옷가지들이 놓여있다",
                    'photo': "",
                },
            ]
        }

WDREV1 = {
    'timeline': 'PM',
    'type': "witness",
    'content': "CA가 TE의 시체를 공동에서 발견하였습니다",
    'target': 'CA'
}

@app.get('//verify/{userid}/{gameid}')
async def verify(userid, gameid):
    print(userid, gameid)
    # storeData(userid, 'domino', gameid)
    if str(gameid).startswith('DOM'):
        if gameid == 'DOMGT':
            storeData(
                userid,
                gameid,
                'domino',
                {
                    'type': 'domino',
                    'title': '도미노 게임 결과',
                    'content': '당신은 경찰, 일반인과 함께 도미노 게임을 진행하였으며, 당신은 1위를 하였습니다',
                    'timeline': 'PN',
                }
            )
        elif gameid == 'DOMGS':
            storeData(
                userid,
                gameid,
                'domino',
                {
                    'type': 'domino',
                    'title': '도미노 게임 결과',
                    'content': '당신은 경찰, 일반인과 함께 도미노 게임을 진행하였지만, 아쉽게도 다른 사람들이 너무 빨리 풀어버렸습니다',
                    'timeline': 'PN',
                }
            )
            # return
        elif gameid == 'DOMGN':
            storeData(
                userid,
                gameid,
                'domino',
                {
                    'type': 'domino',
                    'title': '도미노 게임 결과',
                    'content': '당신은 경찰, 일반인과 함께 도미노 게임을 진행하였지만, 아쉽게도 다른 사람들이 너무 빨리 풀어버렸습니다',
                    'timeline': 'PN',
                }
            )
            # return
        else:
            storeData(
                userid,
                gameid,
                'domino',
                {
                    'type': 'domino',
                    'title': '도미노 게임 결과',
                    'content': '당신은 경찰, 일반인과 함께 도미노 게임을 진행하였지만, 잘못된 방식으로 풀이를 진행하였습니다',
                    'timeline': 'PN',
                }
            )
            # return

        return getData(userid, 'domino')

    if str(gameid).startswith('A'):
        if str(gameid).startswith('ADR'):
            target = str(gameid).removeprefix('ADR')
            storeData(
                userid,
                gameid,
                'alibi',
                {
                    'type': 'alibi',
                    'title': f'{target}의 알리바이',
                    'content': '아침에는 ' + ADREV1[target] + '. 점심에는 ' + ADREV2[target],
                    'timeline': 'SD'
                }
            )
        return getData(userid, 'alibi')

    if str(gameid).startswith('R'):
        if str(gameid).startswith('RDR'):
            target = str(gameid).removeprefix('RDR')
            storeData(
                userid,
                gameid,
                'roomcheck',
                {
                    'type': 'roomcheck',
                    'title': f'{target}의 객실 조사 결과',
                    'content': RDREV1[target],
                    'timeline': 'TN'
                }
            )
        return getData(userid, 'roomcheck')

    if str(gameid).startswith('W'):
        if str(gameid).startswith('WDREV1'):
            target = WDREV1['target']
            storeData(
                userid,
                gameid,
                'witness',
                {
                    'type': 'witness',
                    'title': f'{target}의 사망 사건 목격',
                    'content': WDREV1['content'],
                    'timeline': WDREV1['timeline']
                }
            )
        return getData(userid, 'witness')



@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
