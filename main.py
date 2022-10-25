# Казино777
import random
import time


def getInput(digit, message):
    # функция выбора пункта меню
    ret = -1
    while not ret in range(digit + 1):
        st = input(message)
        if st.isdigit():
            ret = int(st)
        else:
            print("    Введи целое число!")
    return ret


def getIntInput(minimum, maximum, message):
    # Функция ввода ставок с проверкой целого числа в разрешенном диапозоне
    ret = -1
    while minimum > ret or ret > maximum:
        st = input(message)
        if st.isdigit():
            ret = int(st)
        else:
            print("    Введи целое число!")
    return ret


def colorLine(message):
    # Вывод на экран цветного текста, обрамленного звездочками
  #  print('\n' * 30)
    print("*" * (len(message) + 2))
    print(" " + message)
    print("*" * (len(message) + 2))


def loadMoney():
    # Загрузка баланса из файла
    try:
        f = open("money.dat", "r")
        balance = int(f.readline())
        f.close()
    except FileNotFoundError:
        print(f"Сохранения не найдено. Стартовая сумма {defaultMoney} {currency}")
        balance = defaultMoney
    if balance <= 0:
        print(f"Баланс равен нулю. Стартовая сумма {defaultMoney} {currency}")
        balance = defaultMoney
    return balance


def saveMoney():
    # Запись баланса в файл
    try:
        f = open("money.dat", 'w')
        f.write(str(money))
        f.close()
    except:
        print("Ошибка создания файла")
        quit(0)


def rulette():
    # Запуск игры "рулетка"
    global money

    def startRulette(visible):
        # Запуск генерации выпавшего числа
        number = random.randint(0, 38)
        tickTime = random.randint(100, 200) / 10000
        mainTime = 0
        increaseTickTime = random.randint(100, 110) / 100

        if visible:  # Условие отображения анимации
            while mainTime < 0.7:
                mainTime += tickTime
                tickTime *= increaseTickTime

                number += 1
                if number > 38:
                    number = 0
                    # print()
                printNumber = number
                if number == 37:
                    printNumber = '00'
                elif number == 38:
                    printNumber = '000'

                print(' Число >',
                      printNumber,
                      '*' * number,
                      )
                time.sleep(mainTime)
        return number

    def win(bet, result):
        # Вывод информации о выйгрыше
        print(f"    Выпало {result}")
        print(f"    Победа за тобой! Выигрыш составил: {bet} {currency}")
        print(f"    У тебя на счету: {money} {currency}")
        input()

    def losing(bet, result):
        # Вывод информации о проигрыше
        if result == 37:
            result = '00'
        elif result == 38:
            result = '000'
        if money <= 0:
            exitGame()
        else:
            print(f"    Выпало {result}")
            print(f"    Пфф, ты проиграл: {bet} {currency}")
            print(f"    У тебя на счету: {money} {currency}")
            print("    Еще разок попробуешь?")
            input()

    def getBet():
        # Запрос ставки
        nonlocal playRulette

        bet = getIntInput(0, money, "Вам доступно " + str(money) + ' ' + currency + " Ваша ставка... ")
        if bet == 0:
            playRulette = False
        return bet

    playGame = True
    while playGame and money > 0:
        colorLine("ДОБРО ПОЖАЛОВАТЬ В РУЛЕТКУ")
        print(f"На твоем счету {money} {currency}")
        print(" Ставлю на...\n"
              "    1. Четное (выигрыш 1:1)\n"
              "    2. Нечетное (выигрыш 1:1)\n"
              "    3. Дюжина (выигрыш 3:1)\n"
              "    4. Число (выигрыш 36:1)\n"
              "    0. Возврат в предыдущее меню")

        mode = getInput(4, "Твой выбор... ")
        playRulette = True
        if mode == 0:
            playGame = False
            return 0

        # Режим ставки на четное
        elif mode == 1:
            print("Вы ставите на четное")
            bet = getBet()
            if playRulette:
                result = startRulette(True)
                if not result % 2:
                    money += bet
                    win(bet, result)
                else:
                    money -= bet
                    losing(bet, result)

        # Режим ставки на нечетное
        elif mode == 2:
            print("Вы ставите на нечетное")
            bet = getBet()
            if playRulette:
                result = startRulette(True)
                if result % 2:
                    money += bet
                    win(bet, result)
                else:
                    money -= bet
                    losing(bet, result)

        # Режим выбора дюжины
        elif mode == 3:
            dozen = ["От 1 до 12", "От 13 до 24", "От 25 до 36"]
            print("Выбери диапазон:...\n"
                  f"    1. {dozen[0]}\n"
                  f"    2. {dozen[1]}\n"
                  f"    3. {dozen[2]}\n"
                  "    0. Назад")
            modeDozen = getInput(3, 'Твой выбор... ')
            if modeDozen == 0:
                playRulette = False
            else:
                print(f"Вы ставите на дюжину {dozen[modeDozen - 1]}")
                bet = getBet()
            if playRulette:
                result = startRulette(True)
                if result in (0, 37, 38):
                    money -= bet
                    losing(bet, result)
                elif ((result - 1) // 12) == (modeDozen - 1):
                    money += bet * 3
                    win(bet * 2, result)
                else:
                    money -= bet
                    losing(bet, result)

        # Режим выбора числа
        elif mode == 4:
            print("Выбери число от 0 до 36")
            number = getIntInput(0, 36, "Твой выбор... ")
            print(f"Вы ставите на число {number}")
            bet = getBet()
            if playRulette:
                result = startRulette(True)
                if number == result:
                    money += bet * 36
                    win(bet * 35, result)
                else:
                    money -= bet
                    losing(bet, result)


def dice():
    global money

    def getResult():
        res1 = random.randint(1, 6)
        res2 = random.randint(1, 6)
        return res1, res2

    def win(balance):
        pass


    def losing(balance):
        pass

    def exitDice(balance):
        global money
        nonlocal startGame
        print(f"\n"
              f"    Ты забрал {balance - 500} {currency}")
        money += balance
        startGame = False


    playDice = True
    colorLine("ДОБРО ПОЖАЛОВАТЬ В ИГРУ 'КОСТИ'")
    while playDice:

        if money < 500:
            print(f"У тебя недостаточно денег для ставки. У тебя только {money} {currency}")
            return 0
        print(f"У тебя на счету {money} {currency}. Ставка 500 {currency}")
        print("    Чтобы начать нажми Enter"
              "    0. Назад ")
        if input() == '0':
            playDice = False
            return 0
        startGame = True
        firstGame = True
        balance = 500
        money -= balance
        while startGame:
            dices = getResult()
            result = dices[0] + dices[1]
            print(f"    Кости брошены... Выпало {dices[0]}:{dices[1]}\n")
            if not firstGame :
                if ((oldResult - result > 0) and bet == 1 ) or ((result - oldResult) and bet == 2):
                    balance = int(balance * 1.2)
                    print(f"Ты угадал, теперь ставка {balance} {currency}")
                else:
                    startGame = False
                    print("Ты ошибся. Ставка списалась")
            if startGame:
                print(f"    Следующий результат будет:\n"
                      f"    1. Меньше\n"
                      f"    2. Больше\n"
                      f"    0. Выйти из игры и забрать деньги")


                bet = getInput(2, 'Что ты выберешь?')
                if bet == 0:
                    if firstGame:
                        balance = 0
                    exitDice(balance)
                oldResult = result
                firstGame = False



def oneHandBandit():
    pass


def exitGame():
    # Выход из игры и вывод резульатов
    global playGame
    playGame = False
    print()
    # print("Спасибо за игру. Возвращайся еще!")
    if money <= 0:
        print(f"Как жаль, но ты проиграл {startMoney - money} {currency} \n"
              f"У тебя ничего не осталось...")
    elif money >= startMoney:
        print(f"Поздравляю, тебе удалось выиграть {money - startMoney} {currency} \n"
              f"Теперь у тебя {money} {currency}\n"
              f"Продолжай и скоро сможешь открыть свое казино!")
    elif money < startMoney:
        print(f"Как жаль, но ты проиграл {startMoney - money} {currency} \n"
              f"У тебя осталось {money} {currency}\n"
              f"Возвращайся и верни свои деньги ")
    saveMoney()


def main():
    global money, playGame

    while playGame and money > 0:
        print('Приветствую тебя в нашем казино, счастливчик!')
        print(f'У тебя на счету: {money} {currency}')

        print(""" Во что будем играть сегодня?
    1. Рулетка
    2. Кости
    3. Однорукий бандит
    0. Выход. Ставка 0 в игре - выход. """)

        game = getInput(4, "Твой выбор? ")
        games[game]()


defaultMoney = 10000
currency = 'руб.'
playGame = True
money = loadMoney()
startMoney = money
games = [exitGame, rulette, dice, oneHandBandit]
main()
