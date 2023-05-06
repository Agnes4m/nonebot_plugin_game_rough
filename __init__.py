from nonebot import on_command, on_regex,get_driver
from nonebot.params import CommandArg, EventMessage
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.plugin import PluginMetadata

try:
    import ujson as json
except:
    import json

driver = get_driver()
nickname = list(driver.config.nickname)[0]

__version__ = "0.0.1"
__plugin_meta__ = PluginMetadata(
    name="肉鸽小游戏",
    description='一些肉鸽类小游戏',
    usage='肉鸽游戏列表',
    extra={
        "version": __version__,
        "author": "Umamusume-Agnes-Digital <Z735803792@163.com>",
    },
)

