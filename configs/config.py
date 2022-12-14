from modules import Json
from os.path import isfile
from datetime import timedelta, timezone, time
from logging import getLevelName

# CRITICAL
# ERROR
# WARNING
# INFO
# DEBUG
# NOTSET

class _ARKTimeData:
    TIME: time
    CLEAR_DINO: bool
    def __init__(self, time_isoformat: str, clear_dino: bool) -> None:
        self.TIME = time.fromisoformat(time_isoformat)
        self.CLEAR_DINO = clear_dino

class ARKServerConfig:
    UNIQUE_KEY: str
    DIR_PATH: str
    FILE_NAME: str
    DISPLAY_NAME: str
    RCON_ADDRESS: str
    RCON_PORT: int
    RCON_PASSWORD: str
    RCON_TIMEOUT: int
    DISCORD_TEXT_CHANNEL: int
    DISCORD_STATE_CHANNEL: int
    SAVE_TIME: list[_ARKTimeData]
    RESTART_TIME: list[_ARKTimeData]
    def __init__(self, config_path: str) -> None:
        data = Json.load(config_path)
        self.UNIQUE_KEY = data["unique-key"]
        self.DIR_PATH = data["dir_path"]
        self.FILE_NAME = data["file_name"]
        self.DISPLAY_NAME = data["display_name"]
        self.RCON_ADDRESS = data["rcon"]["address"]
        self.RCON_PORT = data["rcon"]["port"]
        self.RCON_PASSWORD = data["rcon"]["password"]
        self.RCON_TIMEOUT = data["rcon"]["timeout"]
        self.DISCORD_TEXT_CHANNEL = data["discord"]["text_channel_id"]
        self.DISCORD_STATE_CHANNEL = data["discord"]["state_channel_id"]
        self.SAVE_TIME = [_ARKTimeData(*dict_.values()) for dict_ in data["save_time"]]
        self.RESTART_TIME = [_ARKTimeData(*dict_.values()) for dict_ in data["restart_time"]]

class LoggingConfig:
    STREAM_LEVEL: int = 20
    FILE_LEVEL: int = 20
    BACKUP_COUNT: int
    FILE_NAME: str
    DIR_PATH: str
    def __init__(self, data: dict) -> None:
        if type(getLevelName(data["stream_level"])) == int:
            self.STREAM_LEVEL = data["stream_level"]
        if type(getLevelName(data["file_level"])) == int:
            self.FILE_LEVEL = data["file_level"]
        self.BACKUP_COUNT = abs(data["backup_count"])
        self.FILE_NAME = data["file_name"]
        self.DIR_PATH = data["dir_path"]

CONFIG = {
    "web": {
        "host": "0.0.0.0",
        "port": 5000,
        "debug": True,
    },
    "sql": {
        "mysql": False,
        "host": "",
        "port": 0,
        "user": "",
        "password": "",
        "database": "data"
    },
    "servers": [
        # "servers-config/Server1.json",
    ],
    "ark_message_filter": {
        "startswith": [
            "SERVER:",
            "???????????????",
        ],
        "include": [
            "?????????????????????",
            "has entered your zone.",
            "????????? ??????",
            "Souls were destroyed by ",
            "Soul was destroyed by ",
            "??????!",
            "?????????!",
            "killed!",
            "???????????? killed",
            "killed ???????????????",
            "?????????",
            "???????????????",
            "?????????",
            "?????????'",
            "???????????????????????????",
            "?????????",
            "??????????????????",
        ],
        "endswith": []
    },
    "discord": {
        "token": "",
        "prefixs": [],
        "admin_role": 0
    },
    "broadcast": {
        "save": "??????????????? $TIME ??????????????????\nServer will save in $TIME min.",
        "stop": "??????????????? $TIME ??????????????????\nServer will shutdown in $TIME min.",
        "restart": "??????????????? $TIME ??????????????????\nServer will restart in $TIME min.",
        "saving": "?????????...\nSaving..."
    },
    "state_message": {
        "running": "???? ?????????",
        "stopped": "???? ?????????",
        "starting": "???? ???????????????",
        "rcon_disconnect": "???? RCON????????????",
        "network_disconnect": "???? ??????????????????"
    },
    "logging": {
        "main": {
            "stream_level": "INFO",
            "file_level": "INFO",
            "backup_count": 3,
            "file_name": "main",
            "dir_path": "logs",
        },
        "discord": {
            "stream_level": "WARNING",
            "file_level": "INFO",
            "backup_count": 3,
            "file_name": "discord",
            "dir_path": "logs",
        },
        "web": {
            "stream_level": "INFO",
            "file_level": "INFO",
            "backup_count": 3,
            "file_name": "web",
            "dir_path": "logs",
        },
        "rcon": {
            "stream_level": "INFO",
            "file_level": "INFO",
            "backup_count": 3,
            "file_name": "rcon",
            "dir_path": "logs",
        },
    },
    "low_battery": 30,
    "timezone": 8,
}

try:
    RAW_CONFIG: dict = Json.load("config.json")
    for key, value in RAW_CONFIG.items():
        if type(value) == dict:
            for s_key, s_value in value.items():
                CONFIG[key][s_key] = s_value
        else:
            CONFIG[key] = value
except: pass
finally:
    Json.dump("config.json", CONFIG)

WEB_HOST: str = CONFIG["web"]["host"]
WEB_PORT: int = CONFIG["web"]["port"]
WEB_DEBUG: bool = CONFIG["web"]["debug"]

SQL_MYSQL: bool = CONFIG["sql"]["mysql"]
SQL_CONFIG: dict = {}
if SQL_MYSQL:
    SQL_CONFIG = {
        "host": CONFIG["sql"]["host"],
        "port": CONFIG["sql"]["port"],
        "user": CONFIG["sql"]["user"],
        "password": CONFIG["sql"]["password"],
        "database": CONFIG["sql"]["database"],
        "charset": "utf-8"
    }
else:
    SQL_CONFIG = {
        "database": f"{CONFIG['sql']['database']}.db",
    }
SQL_PORT: int = CONFIG["sql"]["port"]

_server_list: list[ARKServerConfig] = [ARKServerConfig(config_path) for config_path in CONFIG["servers"]]
SERVERS: dict[str, ARKServerConfig] = {asc.UNIQUE_KEY: asc for asc in _server_list}

ARK_FILTER_S: list[str] = CONFIG["ark_message_filter"]["startswith"]
ARK_FILTER_I: list[str] = CONFIG["ark_message_filter"]["include"]
ARK_FILTER_E: list[str] = CONFIG["ark_message_filter"]["endswith"]

DISCORD_TOKEN: str = CONFIG["discord"]["token"]
DISCORD_PREFIXS: list[str] = CONFIG["discord"]["prefixs"]
DISCORD_ADMIN: int = CONFIG["discord"]["admin_role"]

BROADCAST_SAVE: str = CONFIG["broadcast"]["save"]
BROADCAST_STOP: str = CONFIG["broadcast"]["stop"]
BROADCAST_RESTART: str = CONFIG["broadcast"]["restart"]
BROADCAST_SAVING: str = CONFIG["broadcast"]["saving"]

STATE_RUNNING: str = CONFIG["state_message"]["running"]
STATE_STOPPEN: str = CONFIG["state_message"]["stopped"]
STATE_STARTING: str = CONFIG["state_message"]["starting"]
STATE_RCON: str = CONFIG["state_message"]["rcon_disconnect"]
STATE_NET: str = CONFIG["state_message"]["network_disconnect"]

LOGGING_CONFIG: dict[str, LoggingConfig] = {
    "main": LoggingConfig(CONFIG["logging"]["main"]),
    "discord": LoggingConfig(CONFIG["logging"]["discord"]),
    "web": LoggingConfig(CONFIG["logging"]["web"]),
    "rcon": LoggingConfig(CONFIG["logging"]["rcon"]),
}

LOW_BATTERY: int = CONFIG["low_battery"]
TIMEZONE: timezone = timezone(timedelta(hours=CONFIG["timezone"]))

if SQL_MYSQL: pass
else:
    from sqlite3 import connect
    if not isfile("data.db"):
        db = connect(**SQL_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE "Users" (
                "discord_id" INTEGER NOT NULL UNIQUE,
                "account" TEXT NOT NULL UNIQUE,
                "password" TEXT NOT NULL,
                "token"	TEXT UNIQUE,
                PRIMARY KEY("discord_id")
            );
        """)
        db.commit()
        cursor.close()
        db.close()
        