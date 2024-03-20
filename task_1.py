while True:
    try:
        num = int(input("Введите целое число: "))
        if num > 0:
            el = 1
            rez = ""
            while el <= num:
                rez += el * str(el)
                el += 1
            print(rez)
            break
        else:
            print("Число должно быть больше 0")
    except ValueError:
        print("Неправильный тип данных")

