Добавил файл model.py в котором создается 2 класса таблиц "Таблица чемпионата" из прошлого кода, просто создана новым методом из урока и таблица "Игроки ЦСКА", информация вних спарсена с сайта Футбол на куличках с помощью файла из старого урока parse_and_insert.py и файла созданного по итогам текущего урока parse_and_add_player.py. Колонка команда в новой таблице игроков сделана внешним ключем к колонке ЦСКА в таблице чемпионата. Таким образом добавлая нового игрока в одну таблицу по связкам будет автоматически привязываться к команде во второй таблице.
