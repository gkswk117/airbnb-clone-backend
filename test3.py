def my_function(c,b,a):
    print(f"a is {a}")
    print(f"b is {b}")
    print(f"c is {c}")
my_dict = {'a': 1, 'b': 2, 'c': 3}
my_function(**my_dict)
my_function(3,2,1)