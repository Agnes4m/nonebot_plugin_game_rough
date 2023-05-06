from pydantic import BaseModel

class Character(BaseModel):
    name: str
    speed: int
    max_hp: int
    hp: int
    atk: int

class Battle:
    def __init__(self, character_a, character_b):
        self.character_a = character_a
        self.character_b = character_b
        self.progress_a = 0
        self.progress_b = 0

    def start_battle(self):
        while True:
            self.progress_a += self.character_a.speed
            if self.progress_a >= 100:
                print(f"{self.character_a.name} 获得回合机会！")
                self.progress_a = 0
                self.player_turn(self.character_a, self.character_b)

            self.progress_b += self.character_b.speed
            if self.progress_b >= 100:
                print(f"{self.character_b.name} 获得回合机会！")
                self.progress_b = 0
                self.player_turn(self.character_b, self.character_a)

    def player_turn(self, attacker, defender):
        print(f"当前血量：{self.character_a.name} - {self.character_a.hp}，{self.character_b.name} - {self.character_b.hp}")
        action = input("请输入攻击指令（输入 ttk 进行攻击，按回车跳过回合）：")
        if action == "ttk":
            defender.hp -= attacker.atk
            print(f"{attacker.name} 发动攻击！")
            if defender.hp <= 0:
                defender.hp = 0
                print(f"{attacker.name} 获胜！")
                exit()
        else:
            print(f"{attacker.name} 跳过回合！")

def fight():
    player = {
        "name": "角色A",
        "speed": 15,
        "max_hp": 100,
        "hp": 100,
        "atk": 20
    }
    monster = {
        "name": "角色B",
        "speed": 20,
        "max_hp": 100,
        "hp": 100,
        "atk": 20
    }

    character_a = Character(**player)
    character_b = Character(**monster)

    battle = Battle(character_a, character_b)
    battle.start_battle()

fight()
