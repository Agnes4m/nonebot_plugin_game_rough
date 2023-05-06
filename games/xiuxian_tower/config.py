from pathlib import Path

import json

from .classes import *



CONFIG_PATH = Path() / 'data' / 'game_rough' / 'xiuxian_tower.yml'

# 用户整体信息储存
class UserConfig:
    def __init__(self, user_id: int):
        self.file_path = CONFIG_PATH
        if self.file_path.exists():
            with self.file_path.open('r', encoding='utf-8') as f:
                self.config = json.load(f)
            # self.config = UserMessage.parse_obj(
            #     self.config = json.load(f)
        else:
            self.config = UserMessage()
        
        # 只有当传入 user_id 参数时才进行实例化和生成文件
        if user_id is not None:
            self.config.user_id = user_id
            self.save()

    @property
    def config_list(self) -> List[str]:
        return list(self.config.dict(by_alias=True).keys())

    def save(self):
        with self.file_path.open('w', encoding='utf-8') as f:
            self.config = json.load(f)
test = UserConfig(user_id=114514)
test.config._player

# 整体信息
class UserMessage(BaseModel):
    _player: Player = Field("" ,alias="角色信息")
    _map: Map = Field("" ,alias="地图信息")