import random
import json
from typing import List,Optional,Dict

from pydantic import BaseModel,Field

from enum import Enum
from pathlib import Path

# 角色buff
class PEBuff(BaseModel):
    atk : int = Field(0 ,alias="攻击力修正")
    defense : int = Field(0 ,alias="防御力修正")
    max_hp : int = Field(0 ,alias="生命上限修正")
    now_hp : int = Field(0 ,alias="当前生命修正")
    keep_rough : int = Field(0 ,alias="持续回合（0为持续到战斗结束，1为持续一回合）")

class Treasure(BaseModel):
    

# 玩家信息
class Player(BaseModel):
    name: str = Field("无名小辈" ,alias="玩家名称")
    max_hp: int = Field(None ,alias="生命上限")
    now_hp: int = Field(None ,alias="生命值")
    # max_mp: int = Field(None ,alias="法力上限")
    # now_mp: int = Field(None ,alias="法力值")
    buff: Dict[str,PEBuff] = Field({} ,alias="当前buff")
    backage: Dict(str,int) = Field({} ,alias="当前宝物")
    # 判断物品是否存在于背包中
    def has_item(self, item_name: str) -> bool:
        return item_name in self.backage

    # 添加物品到背包中
    def add_item(self, item_name: str):
        self.backage[item_name] = True

    # 从背包中移除物品
    def remove_item(self, item_name: str):
        if item_name in self.backage:
            del self.backage[item_name]



# 事件
class SomeEvent(str, Enum):
    NE = "普通敌人"
    EE = "精英敌人"
    RE = "随机事件"
    TC = "宝箱"
    SE = "安全事件"
    BOSS = "Boss"

# 地图对象
class MapObject(BaseModel):
    object_type: SomeEvent
    description: str

# 地图类
class Map(BaseModel):
    floor_objects: List[MapObject]

    # 生成地图
    @classmethod
    def generate_map(cls ,weights = None):
        if weights is None:
            weights = {
                SomeEvent.NE: 30,
                SomeEvent.EE: 20,
                SomeEvent.RE: 10,
                SomeEvent.TC: 15,
            }
        floor_objects = []
        floor_objects = []
        for floor in range(1, 25):
            if floor in [12,24]:
                # 第12, 24层一定是Boss
                floor_objects.append(MapObject(object_type=SomeEvent.BOSS, description=f"第{floor}层Boss"))
            elif floor in [11,23]:
                # 前一关是安全屋
                floor_objects.append(MapObject(object_type=SomeEvent.SE, description=f"第{floor}层 安全屋"))
            elif floor in [1,13]:
                floor_objects.append(MapObject(object_type=SomeEvent.NE, description=f"第{floor}层 普通敌人"))
            else:
                # 其他层随机生成对象类型
                object_type = random.choices(list(weights.keys()), list(weights.values()))[0]
                floor_objects.append(MapObject(object_type=object_type, description=f"第{floor}层 {object_type}"))
        return cls(floor_objects=floor_objects)

# 生成地图
# map = Map.generate_map()
# for floor, obj in enumerate(map.floor_objects, start=1):
#     print(f"第{floor}层: {obj.description}")




class atk(BaseModel):
    current_hp: int
    attack_power: int
    defense_power: int

    def attack(self, enemy):
        log = ""
        damage = self.attack_power - enemy.defense_power
        if damage > 0:
            enemy.current_hp -= damage
            log += f"{self.name}攻击了{enemy.name}，造成了{damage}点伤害！"
        else:
            log += f"{self.name}攻击了{enemy.name}，但是没有造成伤害！"

    def heal(self, amount):
        self.current_hp = min(self.current_hp + amount, self.max_hp)



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