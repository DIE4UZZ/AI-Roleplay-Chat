import requests
import json

# 测试角色聊天接口
def test_character_chat():
    url = 'http://localhost:8000/api/chat/character/send'
    headers = {'Content-Type': 'application/json'}
    data = {
        'characterId': 1,
        'message': '你好，哈利波特！'
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"请求失败: {str(e)}")

# 测试角色列表接口
def test_get_characters():
    url = 'http://localhost:8000/api/characters'
    
    try:
        response = requests.get(url)
        print(f"角色列表接口状态码: {response.status_code}")
        print(f"角色列表响应内容: {response.text}")
    except Exception as e:
        print(f"请求失败: {str(e)}")

if __name__ == "__main__":
    print("测试角色聊天接口...")
    test_character_chat()
    
    print("\n测试角色列表接口...")
    test_get_characters()