import os
import sys
import requests
from llm.deeplseek_llm import DeepSeekLLM
from config import env_config

# 测试DeepSeek LLM模型
def test_deeplseek_llm():
    print("开始测试DeepSeek LLM模型...")
    
    try:
        # 创建DeepSeek LLM实例
        llm = DeepSeekLLM()
        
        print(f"成功创建DeepSeek LLM实例")
        print(f"使用的模型: {env_config.DEEPSEEK_MODEL}")
        print(f"默认温度: {env_config.DEEPSEEK_TEMPERATURE}")
        
        # 测试简单的生成响应
        prompt = "你好，你能介绍一下自己吗？"
        print(f"\n测试提示: {prompt}")
        
        print("正在生成响应...")
        response = llm.generate_response(prompt=prompt)
        
        print(f"\n模型响应:\n{response}")
        print(f"\n响应长度: {len(response)} 字符")
        
        # 测试带角色上下文的生成响应
        print("\n测试带角色上下文的响应生成...")
        character_context = {
            "name": "助手",
            "description": "你是一个友好、专业的AI助手。"
        }
        
        response_with_context = llm.generate_response(
            prompt="你好，你是谁？",
            character_context=character_context
        )
        
        print(f"\n带角色上下文的模型响应:\n{response_with_context}")
        
        print("\nDeepSeek LLM模型测试成功！")
        return True
        
    except Exception as e:
        print(f"\nDeepSeek LLM模型测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

# 测试直接API调用（用户提供的示例代码风格）
def test_deeplseek_direct_api():
    print("\n开始测试直接API调用...")
    
    try:
        # 获取配置
        api_key = env_config.DEEPSEEK_API_KEY
        base_url = env_config.DEEPSEEK_BASE_URL
        model = env_config.DEEPSEEK_MODEL
        
        if not api_key:
            print("DeepSeek API密钥未配置，无法测试直接API调用")
            return False
        
        print(f"使用的基础URL: {base_url}")
        print(f"使用的模型: {model}")
        
        # 构建请求参数
        url = f"{base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "stream": False,
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": "Hello!"
                }
            ]
        }
        
        print(f"\n请求URL: {url}")
        print(f"请求模型: {payload['model']}")
        print("正在发送API请求...")
        
        # 发送请求
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        # 检查响应状态
        response.raise_for_status()
        
        # 解析响应
        response_json = response.json()
        print(f"\nAPI响应状态码: {response.status_code}")
        print(f"API响应内容:\n{response_json}")
        
        # 提取并打印生成的文本
        if "choices" in response_json and response_json["choices"]:
            generated_text = response_json["choices"][0]["message"]["content"]
            print(f"\n生成的文本:\n{generated_text}")
        
        print("\n直接API调用测试成功！")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"\n直接API调用失败: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                print(f"错误详情: {error_data}")
            except:
                print(f"响应内容: {e.response.text}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n直接API调用测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # 确保环境变量已加载
    print(f"当前默认模型提供商: {env_config.DEFAULT_LLM_PROVIDER}")
    print(f"DeepSeek API密钥配置: {env_config.DEEPSEEK_API_KEY is not None}")
    
    # 运行两个测试
    llm_test_success = test_deeplseek_llm()
    direct_api_success = test_deeplseek_direct_api()
    
    # 根据测试结果设置退出码
    if llm_test_success and direct_api_success:
        print("\n所有测试都成功通过！")
        sys.exit(0)
    else:
        print("\n某些测试失败！")
        sys.exit(1)