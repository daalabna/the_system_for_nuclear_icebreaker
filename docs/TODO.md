TODO:

[-] сделать выкатку на стенд из новой репы
[-] добавить возможность добавления судов и ледоколов
[-] сделать цветные геотиффы 4 цвета
[-] сделать ручку на получение тифа по дате
[-](F) попробовать отобразить тифф
[-](F) сделать выбор тифа по времени
[-](F) вывести оценку алгоритма
[-](F) пофиксить багу с снятием выбора при групповом снятии с заявок и ледоколов (когда снимаешь чекбокс со всей группы то с карты пути удаляются а из списка нет)
[-] потюнить параметры алгоритмов
[-](А) презентация и доки
[-] попробовать сделать граф прям из сетки?
[-](А) презентация и доки
[-](F) сделать отдельную кнопку "посмотреть сохраненные результаты", при заходе на экран с просмотром темплейта делать GET calculation_request/vessel если пришло [] то кнопка неактивна. Если что-то пришло, то активна. При нажатии на кнопку получить результаты и перейти к их просмотру.


[-] сделать проверку на правильность сохраненного в файл графа? может быть не надо так как этот файл все равно заливается на гит (сейчас при смене графа надо удалять его руками)
[-] Добавить возможность сохранения алгоритма (со списком используемых параметров) + выбора алгоритма в темплейт и context.
[-] сделать вычисление наилучшего результата в дереве решений

DONE:
[+] добавить в решение оценку максимального достижимого времени с идеальным ледоколом
[+] Понять, почему все равно разрешается иногда долгое ожидение
[+] Добавить метрику максимальное время ожидания судов, суммарное время ожидания судов
[+] ручка get_tiff 
[+] добавить идентификатор каравана
[+] бага с расчетом шаблонов при старте
[+] не отображается изначальное ожидание - переделал опять на ожидание в море
[+] waybill - задваивается formation при старте каравана не из порта, пофикшено
[+] waybill - неверный расчет времен событий в convert_simple_path_to_waybill, пофикшено
[+] руками расчистить устья (Лена, Архангельск, еще мб что, проставить там 20-ку) + еще помельчить граф (+) не уверен расчет двадцатки там все-таки проводка дизельными ледоколами, так что ХЗ надо обсудить (в зависимости от режима расчета) 