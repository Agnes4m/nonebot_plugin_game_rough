from pydantic import BaseModel,Field
from typing import List,Optional,Dict
from enum import Enum
import random




# 玩家信息
class Player(BaseModel):
    name: str = Field("无名小辈" ,alias="玩家名称")
    max_hp: int = Field(None ,alias="生命上限")
    now_hp: int = Field(None ,alias="生命值")
    max_mp: int = Field(None ,alias="法力上限")
    now_mp: int = Field(None ,alias="法力值")
    buff: List(str) = Field([] ,alias="增益buff")
    debuff: List(str) = Field([] ,alias="减益buff")
    backage: Dict(str,int) = Field({} ,alias="背包")
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

