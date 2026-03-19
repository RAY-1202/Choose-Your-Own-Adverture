from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# 定义配置类，继承自 BaseSettings
class Settings(BaseSettings):
    API_PREFIX: str = "/api"

    DEBUG: bool = False

    DATABASE_URL: str

    ALLOWED_ORIGINS: str = ""

    OPENAI_API_KEY: str

    OPENAI_API_BASE: str = "https://api.moonshot.cn/v1"  # Moonshot API base URL

    # 字段验证，将逗号分隔的字符串转换为列表
    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v:  str) -> List[str]:
        return v.split(",") if v else []

    # 让 python 知道如何加载环境变量
    class Config:
        env_file = str(BASE_DIR / ".env")
        env_file_encoding = "utf-8"
        case_sensitive = True

# 创建设置实例
# 当我们创建这个类时， 它会自动加载环境变量文件，进行字段验证，并提供一个方便的接口来访问配置值
settings = Settings()