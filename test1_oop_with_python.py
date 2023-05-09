class Player:
    def __init__(self, name, exp):
        self.name = name
        self.exp = exp
    def say_hi(self, saying):
        print(saying+self.name)
# 메서드 정의를 할 때, 좋든 싫든 첫번째 parameter로 self를 적어주어야 한다.
# 안그러면 에러가 난다.
# 메서드 호출을 할 때 첫 번째의 argument는 첫 번째 parameter에 self가 있으므로 자연스럽게 두 번째 parameter자리로 들어간다.
person = Player("한웅", 100)
print(person.name)
print(type(person))
person.say_hi("안녕하세요.")