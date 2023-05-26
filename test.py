# test1_oop_with_python.py
class Human:
    rlahWl = 0
    def __init__(self, name):
        self.name = name
        print(type(self))
        type(self).rlahWl += 1
    
    def say_hi(self, saying):
        print(saying+self.name)
    def say_test(self):
        print("say hoho")

class Player(Human):
    def __init__(self, name, exp):
        super().__init__(name)
        # 항상 다른 클래스를 상속할때면, 그 클래스(부모 클래스, Human)의 constructor를 호출해야된다.
        # python의 방식은 위와 같다.
        Human.rlahWl+=1
        self.exp = exp
        

# 메서드 정의를 할 때, 좋든 싫든 첫번째 parameter로 self를 적어주어야 한다.
# 안그러면 에러가 난다.
# 메서드 호출을 할 때 첫 번째의 argument는 첫 번째 parameter에 self가 있으므로 자연스럽게 두 번째 parameter자리로 들어간다.
print(Human.rlahWl)
inst0 = Human("한웅")
print(Human.rlahWl)
inst1 = Player("명민", 500)
print(Human.rlahWl)
inst2 = Human("한웅")
inst3 = Human("한웅")
inst4 = Human("한웅")
inst5 = Human("한웅")
inst6 = Player("한웅", 5000)
print(Human.rlahWl)
Human.rlahWl="Tlqkf"
print(Human.rlahWl)
inst1.say_test()
print(inst1.exp)
print(inst1.name)
inst1.say_hi("안녕하세요.")

class Fan(Human):
    def __init__(self, name, fav_team):
        super().__init__(name)
        self.fav_team=fav_team

class Dog():
    def woof(self):
        print("woof")
    def say_hi(self):
        print("hi")

class Beagle(Dog):
    def woof(self):
        print("WOOF")
    # 오버라이딩
    def say_new_hi(self):
        super().woof()
        super().say_hi()


# beagle = Beagle()
# beagle.woof()
# beagle.say_hi()
# beagle.say_new_hi()
# 인스턴스에서 부모 클래스의 메서드는 걍 마음대로 쓸 수 있다
# 자식 클래스에서 부모 클래스의 메서드를 쓸 때는 super(). 으로 쓸 수 있다.