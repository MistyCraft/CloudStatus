"""
管理配置的文件
"""
import json
from enum import Enum
from os.path import exists
from typing import Any, Callable

from lib.log import logger


class DataSaveFmt(Enum):
    NORMAL = 0
    PLAYER_LIST_MAPPING = 1
    PLAYER_MAPPING = 2

class SkinLoadWay(Enum):
    MOJANG = 0
    OFFLINE = 1
    LITTLE_SKIN = 2
    CUSTOM_SERVER = 63
    FAILED = 64

class PlayerColorPickWay(Enum):
    """玩家头颅颜色选择方式"""
    EYE_COLOR = 0
    MAIN_COLOR = 1
    SECOND_COLOR = 2
    CUSTOM_COLOR_INDEX = 3
    FIXED_EYE_POS = 4


class Configer:
    """配置文件管理器"""
    addr: str = "127.0.0.1:25565"
    server_name: str = "MC服务器"
    check_inv: int = 60.0
    points_per_file: int = 1200
    saved_per_points: int = 10
    fix_sep: float = 300.0
    min_online_time: int = 60
    data_load_threads: int = 8
    data_dir: str = "./data"
    enable_data_save: bool = True
    data_save_fmt: DataSaveFmt = DataSaveFmt.NORMAL
    time_out: float = 3.0
    retry_times: int = 3
    enable_full_players: bool = False
    fp_re_status_inv: float = 4.0
    fp_max_try: int = 5
    status_ping: bool = True
    today_player_calc_way: int = 1
    tcw_custom_hours: int = 24
    tcw_custom_start: int = 4
    skin_load_way: SkinLoadWay = SkinLoadWay.MOJANG
    custom_skin_server: str = ""
    custom_skin_root: str = ""
    player_content_cache_inv: int = 4
    debug_output_skin_color_pick_log: bool = False
    gui_use_online_range_list: bool = True
    player_card_pick_way: PlayerColorPickWay = PlayerColorPickWay.EYE_COLOR
    player_win_pick_way: PlayerColorPickWay = PlayerColorPickWay.EYE_COLOR
    color_extract_num: int = 3
    color_extract_quality: int = 10
    extracted_color_index: int = 1
    extracted_color_index2: int = 2
    eye_fixed_pos_x: int = 2
    eye_fixed_pos_y: int = 5

    def __init__(self):
        self.config_vars = {}
        # 查找类下所有配置项
        for key in dir(self):
            value = getattr(self, key)
            if not key.startswith("_") and not key.startswith("config_vars") and not isinstance(value, Callable):
                self.config_vars[key] = value
        self.load()

    def load(self):
        """加载配置文件"""
        if exists("./config.json"):
            logger.info("读取配置文件...")
            with open("./config.json", "r", encoding="utf-8") as f:
                cfg_dict: dict = json.load(f)
                for key, value in cfg_dict.items():
                    if not hasattr(self, key):
                        logger.warning(f"配置文件存在未知配置项 -> {key}: {value}")
                        continue
                    now_value = getattr(self, key)
                    if isinstance(now_value, Enum):
                        value = now_value.__class__(value)
                    self.config_vars[key] = value
                    setattr(self, key, value)

    def save(self) -> None | str:
        """保存配置文件, 成功保存返回None, 出错返回错误信息"""
        logger.info("保存配置文件...")
        config_vars_cov = {}
        for key, value in self.config_vars.items():
            if isinstance(value, Enum):
                config_vars_cov[key] = value.value
            else:
                config_vars_cov[key] = value
        try:
            content = json.dumps(config_vars_cov, indent=2)
        except TypeError as e:
            logger.error(f"保存配置时出错: 无法转换此数据类型至json -> {e}")
            return f"无法转换数据类型至json -> {e}"
        try:
            with open("./config.json", "w") as f:
                f.write(content)
        except OSError as e:
            logger.error(f"保存配置时出错: 无法打开文件 -> {e}")
            return f"无法打开文件 -> {e}"
        return None

    def set_value(self, key: str, value: Any):
        """设置配置项的值"""
        self.config_vars[key] = value
        setattr(self, key, value)


config = Configer()
