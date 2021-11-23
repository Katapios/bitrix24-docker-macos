# Bitrix24 docker-compose (bitrixVm - только на докер)
:warning: Сборка содержит все необходимые контейнеры и полностью адаптирована под запуск **Bitrix24** на операционной системе *MacOS*.


## О продукте:
bitrix24-docker-macos запускает аналог bitrix-vm как микросервисы в docker.

### Преимущества данной сборки:
- Все работает из коробки
- Можно ничего не настраивать
- Локальное использование почты
- Локальное использование папок
- Не требует возни с сертификатами и bash-скриптами
- Наличие xdebug
- Заводится на M1

### Настройка окружения:

Настройки можно изменить в файле ```.env```.


```
BX_PUBLIC_HTML_PATH     # путь к директории public_html, в которой содержатся директории хостов
BX_MODULES_PATH         # путь к репозиторию modules
BX_LOGS_PATH            # путь к директории в которой контейнеры должны хранить логи
BX_MYSQL_PATH           # путь DB volume
BX_PHP_VERSION          # версия php 7|8

```

### Как запустить?
```
docker-compose up -d
```

### Важный момент!
Установка продукта через скрипт ["bitrixsetup.php"](https://www.1c-bitrix.ru/download/scripts/bitrixsetup.php) производится довольно долго,  
но ее можно ускорить, если дождаться процесса распаковки скачанных архивов  
и остановить процесс распаковки в браузере.  
Затем зайти в домашний каталог и запустить в терминале команду распаковки:  

```
cat *$(ls -v *tar.gz*) | tar xzf -
```

Команда склеит все части архивов и распакует их (для сжатых архивов).  
Подходит и для установки из backup при помощи "restore" 

## Как заполнять подключение к БД?
- DB-HOST: mysql
- DB-USER: bitrix
- DB-NAME: sitemanager
- DB-PASS: находится в docker-compose файле(не секьюрно, но для локальной разработки пойдет)

## Примечание:
- По умолчанию стоит папка ```var/www/public_html``` но это легко поменять
- не забудьте подпихнуть файлик cron_events.php из корня проекта в ./var/www/public_html/bitrix/php_interface/  - чтобы завелась почта на cron
- Почтовый клииент доступен по адресу: (ваш ip):8025


## Если захотите подключать папки BITRIX и UPLOADS по simlink:
- На мастер-сайте необходимо настроить nfs-server и дать доступ к данным папкам
- В конец docker-compose добавьте блок с mount папками(ip- мастер-сайта)

```
 upload-mount:
    driver: local
    driver_opts:
      type: nfs4
      o: nfsvers=4,addr=192.168.0.100,rw
      device: ":/public_html/upload"
  bitrix-mount:
    driver: local
    driver_opts:
      type: nfs4
      o: nfsvers=4,addr=192.168.0.100,rw
      device: ":/public_html/bitrix"

```
- подключите их в php и nginx контейнерах как volumes

      - "upload-mount:/var/www/public_html/upload"
      - "bitrix-mount:/var/www/public_html/bitrix"

## Если вдруг захотите маунтить папки с другого докера:
-разместите в нем контейнер c nfs сервером

```
  nfs:
    image: itsthenetwork/nfs-server-alpine:12
    container_name: nfs
    restart: unless-stopped
    privileged: true
    environment:
      - SHARED_DIRECTORY=/data
    volumes:

      - ./var/www:/data

    ports:
      - 2049:2049
    networks:
      bx:
        aliases:
          - nfs

```


**PS** Благодарю за труд авторов, выкладывающих в gitlab примеры bitrix контейнеров - без Вас я бы не справился!

:warning: **Не скупимся на звездочки на github, форкаем, даем советы по улучшению и оптимизации (всегда рад).**
