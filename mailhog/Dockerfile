FROM php:7.3-apache

RUN apt-get update

# install minimal command
RUN apt-get install -y vim less

# install php module
RUN docker-php-ext-install pdo mbstring

# setup php.ini
COPY ./php.ini /usr/local/etc/php/

# setup config mail for php 
RUN curl -sSLO https://github.com/mailhog/mhsendmail/releases/download/v0.2.0/mhsendmail_linux_amd64 \
    && chmod +x mhsendmail_linux_amd64 \
    && mv mhsendmail_linux_amd64 /usr/local/bin/mhsendmail \
    && echo 'sendmail_path = "/usr/local/bin/mhsendmail --smtp-addr=mailhog:1025"' > /usr/local/etc/php/conf.d/sendmail.ini
