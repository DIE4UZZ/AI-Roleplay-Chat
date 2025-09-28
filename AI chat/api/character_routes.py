from fastapi import APIRouter, HTTPException
import logging

# 创建路由实例
router = APIRouter()

# 配置日志
logger = logging.getLogger("ai_chat_service.api.character")

# 角色数据（实际应用中应该从数据库获取）
characters_data = [
    {"id": 1, "name": "哈利波特", "avatar": "🧙‍♂️", "description": "魔法世界的传奇巫师", "category": "fiction"},
    {"id": 2, "name": "苏格拉底", "avatar": "👨‍🏫", "description": "古希腊著名哲学家", "category": "historical"},
    {"id": 3, "name": "爱因斯坦", "avatar": "🧠", "description": "著名物理学家，相对论提出者", "category": "historical"},
    {"id": 4, "name": "林黛玉", "avatar": "💃", "description": "《红楼梦》中的经典人物", "category": "fiction"},
    {"id": 5, "name": "莎士比亚", "avatar": "📝", "description": "英国著名剧作家和诗人", "category": "historical"},
    {"id": 6, "name": "哪吒", "avatar": "👶", "description": "中国古代神话中的神童", "category": "mythology"},
    {"id": 7, "name": "牛顿", "avatar": "🍎", "description": "万有引力定律的发现者", "category": "historical"},
    {"id": 8, "name": "孙悟空", "avatar": "🐒", "description": "《西游记》中的齐天大圣", "category": "mythology"},
]

# 角色相关接口
@router.get("/characters", tags=["角色"])
async def get_characters():
    """
    获取角色列表
    
    返回所有可用的AI角色
    """
    logger.info("获取角色列表")
    return characters_data

@router.get("/characters/search", tags=["角色"])
async def search_characters(q: str = None):
    """
    搜索角色
    
    - **q**: 搜索关键词
    """
    logger.info(f"搜索角色，关键词: {q}")
    
    if not q:
        return characters_data
    
    # 过滤角色列表
    filtered_characters = [
        char for char in characters_data
        if q.lower() in char["name"].lower() or q.lower() in char["description"].lower()
    ]
    
    return filtered_characters

@router.get("/characters/{character_id}", tags=["角色"])
async def get_character_by_id(character_id: int):
    """
    获取角色详情
    
    - **character_id**: 角色ID
    """
    logger.info(f"获取角色详情，角色ID: {character_id}")
    
    # 查找指定ID的角色
    character = next((char for char in characters_data if char["id"] == character_id), None)
    
    if not character:
        raise HTTPException(status_code=404, detail="角色不存在")
    
    return character