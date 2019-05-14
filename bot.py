from telegram.ext import Updater, CommandHandler, Filters, ConversationHandler, CallbackQueryHandler

import random


QUESTIONS = {
    1: '''Melovin 
    [Eurovision 2018 song]
    Шукайте завдання там''',
    2: '''Бізн. школа
    К
    3440
    .А9
    Р83
    2007
    176 - 27 - ІІ - 6 - 3
    205 - 4 - 1 - 7
    419 - 112 - 1 - 2 - 1
    ''',
    3: ['pics/ceasar.jpg',
        ''' шифр
        ipx ep zpw mjlf vibv, fmpo nwtl?'''],
    4: '255.0.0',
    5: 'Шукайте відповідь у 110010100',
    6: '''Бізн. школа
    HC
    340
    .19
    .O35
    1971
        
    %d{4}
        ''',
    7: '''Вид-ва
    ND
    955
    .U473
    B48
    P4813
    2018
    [UKR.]
        
    \"Лише дурням потрібен ПОРЯДОК, геній же панує над хаосом\"
        А. Енштейн
        ''',
    8: ['pics/elon-musk.jpg', 'pics/ada-lavleys', 'pics/steve-jobs.jpg',
        'pics/alan-turing.jpg', 'pics/bill-gates.jpg', 'pics/mark-cukerberg.jpg',
        '''Воно належить мені, але інші вживають його частіше за мене
        01
        '''],
    9: 'pics/car-pussle.jpg',
    10: '''Прийнамні одне із тверджень є правдою, проте прийнамні одне є неправдивим.
    Отже, перстень захований в...
        
    золота коробка: Перстень лежить не у срібній коробці.
    срібна коробка: Перстень лежить не тут.
    бронзова коробка: Перстень лкжить тут.
    ''',
    11: '''
    Старому професорі (п), охоронцю (о), асистентці(а) та її хлопцеві (х) потрібно перейти міст.
    Вони мають лише один ліхтарик на чотирьох.
    Переходити міст можна лише із ліхтариком, так як на дворі ніч і міст без перил.
    Водночас на мості може бути не більше 2 осіб, тому що міст старий і більшу кількість не витримає.
    Кожен перехожить через міст за сталий час:
    - охоронець переходить міст за 1 хв
    - хлопець асистентки — за 2 хв
    - асистентка — за 5 хв
    - старий професор — за 10 хв.
    Коли на мості двоє людей, вони йдуть йдуть зі швидкістю повільнішого із них двох.
    У якому порядку їм слід переходити міст, щоб за 17 хв усім бути на іншій його стороні?
    
    Маленькі букви, через пробіли. Пара позначається двома буквами без пробілів у алфавітному порядку.
    Приклад: ао о хс х ох
    ''',
    12: '''
    початок шляху: 01
        
    відповідь: AVG()
        ''',
}

USED_QUESTIONS = {
    1: False,
    2: False,
    3: False,
    4: False,
    5: False,
    6: False,
    7: False,
    8: False,
    9: False,
    10: False,
    11: False,
    12: False,
}

ANSWERS = {
    1: 'may the power of it be with you!',
    2: 'термін угода звільнення',
    3: 'how do you like that, elon musk?',
    4: 'червоний',
    5: 'clean code',
    6: '1971',
    7: '03265741',
    8: 'easabm',
    9: '87',
    10: 'golden box',
    11: 'ох о ас а ао',
    12: '256'
}

KEYWORD = ['p', 'u', 'z', 'z', 'l', 'e', 'h', 'e', 'a', 'd', 'e', 'd']

TRIALS = 0
QUESTION_COUNTER = 0


def start(bot, update):
    update.message.reply_text(
        '''Привіт {}!
        Тебе вітає QuestBot від НТПН Luminos
        
        Тебе чекає 12 завдань, доступ до якиї ти зможеш отримати через цього бота.
        Щоб отримати доступ до наступного завдання тобі потрібно увести правильну відповідь для попереднього завдання
        або увести команду /skip для того щоб пропустити завдання.
        
        На кожне завдання у тебе є 3 спроби.
        Відповіді потрібно вводити маленькими літерами.
        
        Після правтльної відповіді ти отримуватимеш букву, які згодом складеш у ключове слово.
        Це ключове слово стане твоїм паролем для отрмання приємних подаруночків наприкінці квесту.
        
        Успіхів!
        '''.format(update.message.from_user.first_name))
    generate_question(bot, update)


def generate_question(bot, update):
    no = random.randint(1, 13)
    if USED_QUESTIONS[no] is True:
        while USED_QUESTIONS[no] is True:
            no = random.randint(1, 13)
    USED_QUESTIONS[no] = True
    global QUESTION_COUNTER
    QUESTION_COUNTER += 1
    if no in [3, 4, 8, 9]:
        send_img_question(bot, update, no)
    else:
        send_question(bot, update, no)


def send_question(bot, update, no):
    if no in [3, 4, 8, 9]:
        quest = QUESTIONS[no][-1]
    else:
        quest = QUESTIONS[no]
    update.message.reply_text(quest)


def send_img_question(bot, update, no):
    for img in QUESTIONS[no][:-1]:
        bot.sendPhoto(chat_id=update.message.chat_id,
                      photo=open((img), 'rb'))
    send_question(bot, update, no)

# To Do
def answer_input(update, bot, no):
    cv_handler = ConversationHandler(per_user=True,
                                     entry_points=[CommandHandler('start', start)],
                                     states={

                                         CHOOSE_TEST: [CallbackQueryHandler(choose_test)],

                                         ANSWER: [CallbackQueryHandler(button)],

                                         QUESTION: [MessageHandler(Filters.text, send_question),
                                                    CommandHandler('start', start)],

                                     },
                                     fallbacks=[ConversationHandler.END]
                                     )
    # answer = MessageHandler(Filters.text, check_answer(bot, update, no))
    print(answer)
    # check_answer(bot, update, no, answer)


def check_answer(bot, update, no, answer):
    print('here')
    global TRIALS, QUESTION_COUNTER
    if ANSWERS[no] == answer and TRIALS < 3:
        if QUESTION_COUNTER < 12:
            TRIALS = 0
            update.message.reply_text('''Чудово!
                                         {}
                                         Наступне питання'''.format(KEYWORD[QUESTION_COUNTER - 1]))

            generate_question(bot, update)
        else:
            update.message.reply_text('''Вітаємо!
            Квест заверщений!
            Твій приз чекає тебе у стартовій точці. І не забудь про пароль!''')
    else:
        TRIALS += 1
        update.message.reply_text('''Хм...
                                     Чому б тобі не спробувати ще раз?
                                     Залишилось спроб: {}'''.format(str(3 - TRIALS)))


def skip(bot, update):
    generate_question(bot, update)


updater = Updater('TOKEN')

updater.dispatcher.add_handler(CommandHandler('hello', start))
updater.dispatcher.add_handler(CommandHandler('skip', skip))
updater.dispatcher.add_handler(CommandHandler('ans', answer_input))

updater.start_polling()
updater.idle()
