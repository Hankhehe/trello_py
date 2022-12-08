from trello import TrelloClient
import json,time

def GetTrelloID() -> dict:
    Data = {}
    boards = client.list_boards()
    for board in boards :
        Data[board.name] = {'ID':board.id}
        Data[board.name]['Lists'] = []
        Data[board.name]['Members'] = []
        for member in board.all_members() :
            Data[board.name]['Members'].append({'FullName':member.full_name,'Username':member.username,'ID':member.id})
        for list in board.list_lists() :
            Data[board.name]['Lists'].append({'Name':list.name,'ID':list.id})  
    return Data

def SumCardScore(Cards:list) ->int:
    score = 0
    for card in Cards :
        plugindata = json.loads(card.plugin_data[0]['value'])
        if '__CFT_DATA__' in plugindata:
            for i in plugindata['__CFT_DATA__'] :
                if str.isdigit(i) :
                    score += plugindata['__CFT_DATA__'][i]['v']
    return score

salesboardID = '5996b01969c3b441685697eb'
afterboardID = '5ade989000aa0143ea3d0c67'
list_POC_ID = {'ID':'5d80b7ff69198078833b5d1e'} # POC 測試中
list_accepting = {'ID':'5b3da4d0b80d8e299de0b03e'} # 待驗收
warranty = {'ID':'5ade98a0bbbd00102d082db1'} # 保固中
field_plugin_ID = '5e2212c3ba57415ef2ef9352'
cardDatas, memberDatas = {},{}
querypaths = {'sales':{'boardID':salesboardID,'listIDs':[list_POC_ID]},'after':{'boardID':afterboardID,'listIDs':[list_accepting,warranty]}}

with open('APIkey.json','r',encoding='UTF-8') as f: 
    APIData = json.load(f)   
client = TrelloClient(api_key = APIData['api_key'],api_secret = APIData['api_secret'],token = APIData['token'])

# with open('TrelloData.json','w',encoding='utf-8') as f : 
#     f.write(json.dumps(GetTrelloID(),indent=4,ensure_ascii=False))

for queryName in querypaths :
    board = client.get_board(querypaths[queryName]['boardID'])
    for member in board.all_members() :
        memberDatas[member.id] = {'fullname':member.full_name,'username':member.username,'cards':[],'score':0}
    for listID in querypaths[queryName]['listIDs']:
        listtemp = board.get_list(listID['ID'])
        cards = listtemp.list_cards()
        cardDatas[listID['ID']] = cards

for listID in cardDatas :
    for card in cardDatas[listID]:
        for member in card.idMembers:
            memberDatas[member]['cards'].append(card)

for member in memberDatas:
    memberDatas[member]['score'] =  SumCardScore(memberDatas[member]['cards'])
    memberDatas[member]['count'] = len(memberDatas[member]['cards'])
    print(f'{memberDatas[member]["fullname"]} : {memberDatas[member]["score"]} 分, 客戶數 : {memberDatas[member]["count"]}')