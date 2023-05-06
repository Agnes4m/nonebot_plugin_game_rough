from nonebot import on_command

from .classes import Player




# 整体思路
# 1、读取当前个人信息，地图信息
# 2、个人信息buff机制
# 3、敌人类型能力机制
# 4、战斗系统
# 5、宝箱系统（固定获取宝物）
# 6、随机事件系统
# 7、boss战斗系统

start_tower = on_command('start_tower',aliases="开始游戏")