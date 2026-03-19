"""
故事生成器模块

该模块负责使用 LLM (大语言模型) 生成交互式故事的核心逻辑。
包含 StoryGenerator 类，用于创建故事及其分支节点结构。
"""

import json
from sqlalchemy.orm import Session

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from core.prompts import STORY_PROMPT
from models.story import Story, StoryNode
from core.models import StoryLLMResponse, StoryNodeLLM
from core.config import settings
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class StoryGenerator:
    """
    故事生成器类

    使用 Kimi 的模型生成交互式"选择你自己的冒险"类型故事。
    该类提供类方法来生成完整的故事结构，包括故事节点和选项分支。
    """

    @classmethod
    def _get_llm(cls):  # 方法名前加下划线表示私有方法
        """
        获取 LLM 实例

        Returns:
            ChatOpenAI: 配置好的模型实例
        """
        return ChatOpenAI(
            model="moonshot-v1-8k",
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_API_BASE
        )

    @classmethod
    def generate_story(cls, db: Session, session_id: str, theme: str = "fantasy") -> Story:
        """
        生成一个完整的交互式故事

        Args:
            db: SQLAlchemy 数据库会话对象
            session_id: 用户会话 ID，用于关联故事与用户
            theme: 故事主题，默认为 "fantasy"（奇幻主题）

        Returns:
            Story: 创建并保存到数据库的故事对象
        """
        # 获取 LLM 实例
        llm = cls._get_llm()

        # 构建聊天提示模板，包含系统提示和用户输入
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",  # 系统角色消息，包含故事生成的指令
                STORY_PROMPT
            ),
            (
                "human",  # 用户角色消息，指定故事主题
                f"Create the story with this theme: {theme}"
            )
        ])  # 不再使用 format_instructions

        # 调用 LLM 生成故事内容
        raw_response = llm.invoke(prompt.invoke({}))

        # 提取响应文本内容
        response_text = raw_response
        if hasattr(raw_response, "content"):
            response_text = raw_response.content

        # 检查响应是否为空
        if not response_text:
            raise ValueError("LLM 返回了空响应，请检查 API 密钥和模型配置")

        # 清理响应文本，移除 markdown 代码块标记
        cleaned_text = response_text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        elif cleaned_text.startswith("```"):
            cleaned_text = cleaned_text[3:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
        cleaned_text = cleaned_text.strip()

        # 直接使用 Pydantic 模型解析 JSON
        try:
            json_data = json.loads(cleaned_text)
            story_structure = StoryLLMResponse.model_validate(json_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM 返回的 JSON 格式无效: {e}")

        # 创建故事数据库记录
        story_db = Story(title=story_structure.title, session_id=session_id)
        db.add(story_db)
        db.flush()  # 刷新以获取 story_db.id

        # 获取根节点数据
        root_node_data = story_structure.rootNode

        # 如果根节点是字典格式，将其转换为 StoryNodeLLM 对象
        if isinstance(root_node_data, dict):
            root_node_data = StoryNodeLLM.model_validate(root_node_data)

        # 递归处理故事节点，从根节点开始
        cls._process_story_node(db, story_db.id, root_node_data, is_root=True)

        # 提交所有数据库更改
        db.commit()
        return story_db

    @classmethod
    def _process_story_node(cls, db: Session, story_id: int, node_data: StoryNodeLLM, is_root: bool = False) -> StoryNode:
        """
        递归处理并保存故事节点

        该方法会递归遍历整个故事树结构，为每个节点创建数据库记录，
        并建立节点之间的父子关系。

        Args:
            db: SQLAlchemy 数据库会话对象
            story_id: 所属故事的 ID
            node_data: 节点数据（来自 LLM 的响应）
            is_root: 是否为根节点，默认为 False

        Returns:
            StoryNode: 创建并保存到数据库的故事节点对象
        """
        # 创建故事节点对象
        # 使用 hasattr 检查以支持对象属性访问和字典键访问两种方式
        node = StoryNode(
            story_id=story_id,
            content=node_data.content if hasattr(node_data, "content") else node_data["content"],  # 节点内容文本
            is_root=is_root,  # 是否为根节点
            is_ending=node_data.isEnding if hasattr(node_data, "isEnding") else node_data["isEnding"],  # 是否为结局节点
            is_winning_ending=node_data.isWinningEnding if hasattr(node_data, "isWinningEnding") else node_data[
                "isWinningEnding"],  # 是否为胜利结局
            options=[]  # 初始化选项列表为空
        )
        db.add(node)
        db.flush()  # 刷新以获取 node.id

        # 如果不是结局节点且存在选项，则处理子节点
        if not node.is_ending and (hasattr(node_data, "options") and node_data.options):
            options_list = []

            # 遍历每个选项
            for option_data in node_data.options:
                # 获取下一个节点的数据
                next_node = option_data.nextNode

                # 如果下一个节点是字典格式，将其转换为 StoryNodeLLM 对象
                if isinstance(next_node, dict):
                    next_node = StoryNodeLLM.model_validate(next_node)

                # 递归处理子节点
                child_node = cls._process_story_node(db, story_id, next_node, False)

                # 将选项信息添加到列表中
                options_list.append({
                    "text": option_data.text,  # 选项显示文本
                    "node_id": child_node.id,  # 对应子节点的 ID
                })

            # 更新节点的选项列表
            node.options = options_list

        db.flush()  # 刷新以保存选项更新
        return node