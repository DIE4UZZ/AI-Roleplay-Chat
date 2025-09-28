from typing import Dict, Any, List, Optional
import logging
from llm.base import LLMBase
from api.models import CharacterContext

# 配置日志
logger = logging.getLogger("ai_chat_service.llm.agent")

class Agent:
    """AI角色Agent，用于增强角色的自主性和互动能力"""
    
    def __init__(self, llm: LLMBase, character_context: CharacterContext):
        """
        初始化Agent
        
        参数:
            llm: LLM模型实例
            character_context: 角色上下文信息
        """
        self.llm = llm
        self.character_context = character_context
        
        # 增强的角色属性
        self.memory: List[Dict[str, Any]] = []  # 角色记忆
        self.goals: List[str] = []  # 角色目标
        self.behavior_patterns: Dict[str, str] = {}  # 行为模式
        self.emotional_state: Dict[str, float] = {}  # 情感状态
        self.background_story: str = ""  # 背景故事
        
        # 从角色上下文初始化
        self._initialize_from_context()
        
    def _initialize_from_context(self):
        """从角色上下文初始化Agent的属性"""
        if hasattr(self.character_context, 'other_info') and self.character_context.other_info:
            other_info = self.character_context.other_info
            self.memory = other_info.get('memory', [])
            self.goals = other_info.get('goals', [])
            self.behavior_patterns = other_info.get('behavior_patterns', {})
            self.emotional_state = other_info.get('emotional_state', {})
            self.background_story = other_info.get('background_story', '')
    
    def generate_response(self, prompt: str, chat_history: List[Dict[str, str]] = None) -> str:
        """
        生成角色响应，融合Agent特性
        
        参数:
            prompt: 用户输入的提示文本
            chat_history: 聊天历史记录
        
        返回:
            角色的响应文本
        """
        # 构建增强的提示，确保角色身份完全融入响应
        enhanced_prompt = f"""
你现在需要完全扮演{self.character_context.name}这个角色，用{self.character_context.name}的身份、语气和思维方式来回应。

角色背景：{self.character_context.description}

请记住，你的所有回应都必须严格符合这个角色的特点，不要以任何方式偏离角色设定。

用户的问题：{prompt}

请以{self.character_context.name}的身份直接回答，不要添加任何额外的解释或说明。
"""
        
        logger.info(f"生成{self.character_context.name}的响应")
        
        # 将CharacterContext对象转换为字典格式，以便LLM模型使用
        character_context_dict = {
            'name': self.character_context.name,
            'description': self.character_context.description,
            'avatar': self.character_context.avatar,
            'category': self.character_context.category
        }
        
        # 调用LLM生成响应
        response = self.llm.generate_response(
            prompt=enhanced_prompt,
            character_context=character_context_dict,
            chat_history=chat_history
        )
        
        # 更新记忆
        self._update_memory(prompt, response)
        
        return response
    
    def autonomous_action(self, situation: str = "") -> str:
        """
        角色自主行动，不需要用户直接输入
        
        参数:
            situation: 当前情境描述
        
        返回:
            角色的自主行动描述或思考
        """
        # 构建自主行动的提示
        action_prompt = self._build_autonomous_prompt(situation)
        
        logger.info(f"{self.character_context.name}正在进行自主行动")
        
        # 生成自主行动
        action = self.llm.generate_response(
            prompt=action_prompt,
            character_context={
                "name": self.character_context.name,
                "description": self.character_context.description,
                "background_story": self.background_story,
                "behavior_patterns": self.behavior_patterns,
                "current_emotion": self._get_current_emotion(),
                "goals": self.goals,
                "memory": self.memory[-5:]  # 最近的几条记忆
            }
        )
        
        # 更新记忆
        self._update_memory("[自主行动]", action)
        
        return action
    
    def _build_autonomous_prompt(self, situation: str) -> str:
        """构建自主行动的提示文本"""
        prompt_parts = []
        
        prompt_parts.append(f"作为{self.character_context.name}，")
        
        if situation:
            prompt_parts.append(f"在当前情境下：{situation}，")
        
        prompt_parts.append("你会主动做什么或想什么？")
        prompt_parts.append("请用符合你性格和背景的方式表达。")
        
        return "".join(prompt_parts)
    
    def _update_memory(self, user_input: str, agent_response: str):
        """更新角色记忆"""
        memory_item = {
            "timestamp": "now",
            "user_input": user_input,
            "agent_response": agent_response
        }
        
        self.memory.append(memory_item)
        
        # 限制记忆长度，避免过多消耗
        if len(self.memory) > 50:
            self.memory = self.memory[-50:]
    
    def _get_current_emotion(self) -> str:
        """获取角色当前的情感状态描述"""
        if not self.emotional_state:
            return "无特定情感"
        
        # 找出最强烈的情感
        strongest_emotion = max(self.emotional_state.items(), key=lambda x: x[1], default=("平静", 0))
        
        if strongest_emotion[1] < 0.3:
            return "平静"
        
        intensity_map = {
            (0.3, 0.5): "有些",
            (0.5, 0.7): "比较",
            (0.7, 1.0): "非常"
        }
        
        intensity = ""
        for (low, high), desc in intensity_map.items():
            if low <= strongest_emotion[1] < high:
                intensity = desc
                break
        
        return f"{intensity}{strongest_emotion[0]}"

class AgentManager:
    """管理多个Agent实例"""
    _instance = None
    _agents = {}
    
    @classmethod
    def get_instance(cls):
        """单例模式获取实例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def get_agent(self, llm: LLMBase, character_context: CharacterContext) -> Agent:
        """
        获取或创建Agent实例
        
        参数:
            llm: LLM模型实例
            character_context: 角色上下文信息
        
        返回:
            Agent实例
        """
        # 使用角色名称作为标识，因为CharacterContext没有id属性
        agent_key = f"{character_context.name}:{id(llm)}"
        
        if agent_key not in self._agents:
            self._agents[agent_key] = Agent(llm, character_context)
        
        return self._agents[agent_key]
    
    def clear_agent(self, character_name: str):
        """清除指定角色的Agent实例
        
        参数:
            character_name: 角色名称
        """
        keys_to_remove = [key for key in self._agents.keys() if key.startswith(f"{character_name}:")]
        for key in keys_to_remove:
            del self._agents[key]
    
    def clear_all_agents(self):
        """清除所有Agent实例"""
        self._agents.clear()