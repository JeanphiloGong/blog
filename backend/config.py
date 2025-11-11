import os
from pathlib import Path
from dotenv import load_dotenv

#############################
# ROOT APPLICATION PATH
###############################

ROOT_PATH =  Path(__file__).resolve().parent

###########################
# Load .env file
############################
ENV_FILE_PATH = ROOT_PATH / ".env"

load_dotenv(dotenv_path=ENV_FILE_PATH)

###################################
# OPENAI_API_KEY
####################################

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.chatanywhere.tech/v1")

####################################
# DATABASE
################################
DB_TYPE = os.getenv("DB_TYPE")

if DB_TYPE:
    print(f"环境变量加载成功，数据库类型为{DB_TYPE}, 项目根目录为{ROOT_PATH}")
else:
    print("环境变量加载失败, DB_TYPE没有设置或文件加载失败")


########################################
# DATA
#########################################
DATA_PATH = ROOT_PATH / "data"



####################################
# REDIS
####################################

REDIS_URL = os.environ.get("REDIS_URL", "")
REDIS_CLUSTER = os.environ.get("REDIS_CLUSTER", "False").lower() == "true"

REDIS_KEY_PREFIX = os.environ.get("REDIS_KEY_PREFIX", "open-webui")

REDIS_SENTINEL_HOSTS = os.environ.get("REDIS_SENTINEL_HOSTS", "")
REDIS_SENTINEL_PORT = os.environ.get("REDIS_SENTINEL_PORT", "26379")

# Maximum number of retries for Redis operations when using Sentinel fail-over
REDIS_SENTINEL_MAX_RETRY_COUNT = os.environ.get("REDIS_SENTINEL_MAX_RETRY_COUNT", "2")
try:
    REDIS_SENTINEL_MAX_RETRY_COUNT = int(REDIS_SENTINEL_MAX_RETRY_COUNT)
    if REDIS_SENTINEL_MAX_RETRY_COUNT < 1:
        REDIS_SENTINEL_MAX_RETRY_COUNT = 2
except ValueError:
    REDIS_SENTINEL_MAX_RETRY_COUNT = 2



####################################
# WEBSOCKET SUPPORT
####################################

ENABLE_WEBSOCKET_SUPPORT = (
    os.environ.get("ENABLE_WEBSOCKET_SUPPORT", "True").lower() == "true"
)


WEBSOCKET_MANAGER = os.environ.get("WEBSOCKET_MANAGER", "")

WEBSOCKET_REDIS_URL = os.environ.get("WEBSOCKET_REDIS_URL", REDIS_URL)
WEBSOCKET_REDIS_CLUSTER = (
    os.environ.get("WEBSOCKET_REDIS_CLUSTER", str(REDIS_CLUSTER)).lower() == "true"
)

websocket_redis_lock_timeout = os.environ.get("WEBSOCKET_REDIS_LOCK_TIMEOUT", "60")

try:
    WEBSOCKET_REDIS_LOCK_TIMEOUT = int(websocket_redis_lock_timeout)
except ValueError:
    WEBSOCKET_REDIS_LOCK_TIMEOUT = 60

WEBSOCKET_SENTINEL_HOSTS = os.environ.get("WEBSOCKET_SENTINEL_HOSTS", "")
WEBSOCKET_SENTINEL_PORT = os.environ.get("WEBSOCKET_SENTINEL_PORT", "26379")
