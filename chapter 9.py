import re
def match_regex(filename, regex): # СОЗДАЕМ КОРУТИНУ, В КОТОРУЮ БУДЕМ ПЕРЕДАВАТЬ РЕГУЛЯРНЫЕ ВЫРАЖЕНИЯ
    with open(filename) as file:
        lines = file.readlines()    # СЧИТЫВАЕМ ВСЕ СТРОКИ
    for line in reversed(lines):    # И БЕЖИМ ПО НИМ В ОБРАТНОМ ПОРЯДКЕ
        match = re.match(regex, line)   # ПРИМЕНЯЯ К НИМ РЕГУЛЯРКУ
        if match:                       # ЕСЛИ НАШЛИ СОВПАДЕНИЕ, ВОЗВРАЩАЕМ СОХРАНЕННУЮ ГРУППУ, И ГОТОВИМСЯ
            regex = yield match.groups()[0] # ПРИНЯТЬ НОВУЮ РЕГУЛЯРКУ

def get_serials(filename):
    ERROR_RE = 'XFS ERROR (\[sd[a-z]\])'    # ГОТОВИМ РЕГУЛЯРКУ ДЛЯ КОРУТИНЫ. В НЕЙ МЫ ИЩЕМ ОШИБКУ XFS ERROR В ФАЙЛЕ
    matcher = match_regex(filename, ERROR_RE)   # ПОДГОТАВЛИВАЕМ КОРУТИНУ
    device = next(matcher)                      # И ИНИЦИАЛИЗИРУЕМ ЕЕ. В ПЕРЕМЕННОЙ device - ПЕРВОЕ СООБЩЕНИЕ ОБ ОШИБКЕ
    while True:                                 # XFS ERROR. ТОЧНЕЕ - ИМЯ УСТРОЙСТВА
        bus = matcher.send('(sd \S+) {}.*'.format(re.escape(device))) # ОТПРАВЛЯЕМ В КОРУТИНУ НОВУЮ РЕГУЛЯРКУ, КОТОРАЯ
                                                                      # ИЩЕТ ШИНУ НА КОТОРОЙ ПРОИЗОШЛА ОШИБКА. МЫ
                                                                      # ПРОДОЛЖАЕМ БЕЖАТЬ НАЗАД ПО ФАЙЛУ В КОРУТИНЕ
                                                                      # ТОЛЬКО ПРИМЕНЯЕМ К СТРОКАМ УЖЕ ЭТУ РЕГУЛЯРКУ!

        serial = matcher.send('{} \(SERIAL=([^)]*)\)'.format(bus))  # ТАК ЖЕ, КАК В ПРЕДЫДУЩЕЙ СТРОКЕ ОТПРАВЛЯЕМ НОВУЮ
                                                                    # РЕГУЛЯРКУ, ОСНОВЫВАЯСЬ НА РЕЗУЛЬТАТАХ ПОИСКА
                                                                    # ПРЕДЫДУЩЕЙ. В ПЕРЕМЕННОЙ serial - ИСКОМЫЙ СЕРИЙНЫЙ
                                                                    # НОМЕР ДИСКА

        yield serial    # ВОЗВРАЩАЕМ ЭТОТ СЕРИЙНЫЙ НОМЕР
        device = matcher.send(ERROR_RE) # ВОССТАНАВЛИВАЕМ ПЕРВУЮ РЕГУЛЯРКУ, И ПРОДОЛЖАЕМ БЕЖАТЬ ПО ФАЙЛУ

for serial_number in get_serials('EXAMPLE_LOG.log'):    # БЕЖИМ ПО ИТЕРАТОРУ И ПЕЧАТАЕМ СЕРИЙНЫЙ НОМЕР
    print(serial_number)