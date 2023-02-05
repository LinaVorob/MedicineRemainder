from config import COMMAND

MESSAGE_HELP = "\n".join([f"{v}: {k}" for k, v in COMMAND.items()])

MESSAGE_START = f"{'Бот, никогда не забывающий о лекарствах :)'}\n\n{MESSAGE_HELP}"

MESSAGE_ADDING_COMPLETED = "Лекарство {} добавлено в ваше расписание. Напомнинание о приеме будет приходить в {}:{} " \
                           "кажды{} {} в течении {}."

MESSAGE_GET_NAME = 'Как называется ваше лекартсво?'
MESSAGE_GET_CATEGORY = 'С таким лекарством я пока не знаком.\n\nК какой категории его можно отнести:\nантибиотик, ' \
                       'антисептик, БАД или что-то иное?'
MESSAGE_GET_CONDITION_OF_INTAKE = 'Укажите есть ли особенности приема лекарства, как например, перед едой или на тощак.'
MESSAGE_COMMON_PERIOD = 'Как долго вы будете принимать лекарство? Прошу прислать сообщение в формате:\n ' \
                        '00г 00м 00д 00ч 00м 00с. Если все нули - бессрочный приём.'
MESSAGE_HAS_BREAK = 'Предполагаются ли для лекарства перерывы в приёме (например, его нужно принимать 3 дня, 3 дня ' \
                    'не принимать, а потом снова 3 дня и так в течение, например, года)?'
MESSAGE_ONE_PERIOD = 'Укажите длительность одного непрерывного приема лекарства в формате ' \
                     '00г 00м 00д 00ч 00м 00с.'
MESSAGE_BREAK = 'Теперь укажите длительность перерыва в таком же формате.'
MESSAGE_COUNT_IN_DAY = 'Укажите количество приемов для одного дня (просто число)'
MESSAGE_TIME = 'Укажите время приема'
MESSAGE_TIME_STEP = 'Укажите время между приемами в день в формате 00ч 00м'
MESSAGE_DOZE = 'Укажите количество доз лекарства, необходимое для единовременного приема (прочто число)'
MESSAGE_DOZE_IN_PACKAGE = 'Укажите количество имеющихся доз лекарства на данный момент (просто число). Я буду сам отсчитывать остаток' \
                          ' и напоминать вам о необходимости докупки лекарства.'

if __name__ == '__main__':
    print(MESSAGE_HELP)
