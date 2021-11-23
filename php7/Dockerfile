FROM php:7.4-fpm

ARG APCU_VERSION=5.1.20

ARG CONTAINER_GID
ARG CONTAINER_UID
ARG CONTAINER_USER
ARG CONTAINER_GROUP

ARG BX_XDEBUG_IP
ARG BX_XDEBUG_PORT
ARG BX_DEFAULT_CHARSET

COPY ./conf.d /usr/local/etc/php/conf.d/
COPY ./php-fpm.d /usr/local/etc/php-fpm.d/
COPY ./exim/update-exim4.conf.conf /etc/exim4/




# Install dependencies

RUN apt-get update && apt-get install -y \

    cron \

    build-essential \

    locales \

    libmcrypt-dev \

    libonig-dev \

    zip \

    jpegoptim optipng pngquant gifsicle \

    vim \

    unzip \

    git \

    graphviz \

    curl \

    supervisor




RUN apt-get update \
    && apt-get install -y vim exim4 \
    && echo "syntax on" > ~/.vimrc \
    && apt-get -y install \
        libmagickwand-dev \
        libjpeg62-turbo-dev \
        libfreetype6-dev \
        libmemcached-dev \
        libicu-dev \
        libzip-dev \
        curl\
        zlib1g-dev \
        libpng-dev \
        libxml2-dev \
        --no-install-recommends \
    && pecl install imagick apcu-${APCU_VERSION} memcached \
    && docker-php-ext-enable imagick \
    && docker-php-ext-enable apcu \
    && docker-php-ext-enable memcached \
    && docker-php-ext-configure gd --with-freetype=/usr/include/ --with-jpeg=/usr/include/ \
    && docker-php-ext-install -j$(nproc) gd \
    && docker-php-ext-install mysqli pdo_mysql opcache exif intl sockets bz2 zip \
    && docker-php-ext-configure opcache --enable-opcache \
#    && pecl install -o -f redis \
#    && docker-php-ext-enable redis \
    && rm -rf /tmp/* /var/cache/apk/* /var/lib/apt/lists/* \
    && pecl install xdebug && docker-php-ext-enable xdebug



RUN apt-get update


#install mail
#RUN curl -Lsf 'https://storage.googleapis.com/golang/go1.8.3.linux-amd64.tar.gz' | tar -C '/usr/local' -xvzf -

RUN apt install -y golang
ENV PATH /usr/local/go/bin:$PATH
RUN go get github.com/mailhog/mhsendmail
RUN cp /root/go/bin/mhsendmail /usr/bin/mhsendmail
RUN echo 'sendmail_path = /usr/bin/mhsendmail --smtp-addr mailhog:1025' > /usr/local/etc/php/php.ini    


RUN apt-get install -y vim less


RUN apt-get install libldap2-dev
#rm -rf /var/lib/apt/lists/* && \
#docker-php-ext-configure ldap --with-libdir=lib/x86_64-linux-gnu/ && \

RUN docker-php-ext-configure ldap
RUN docker-php-ext-install ldap


RUN cd /tmp && \
    git clone https://github.com/Imagick/imagick && \
    cd imagick && \
    phpize && \
    ./configure && \
    make && make install && \
    docker-php-ext-enable imagick && \
    cd /tmp && rm -rf imagick


RUN groupadd -g ${CONTAINER_GID} ${CONTAINER_GROUP} \
    && useradd -u ${CONTAINER_UID} -g ${CONTAINER_GID} ${CONTAINER_USER}


RUN chmod -R 777 /usr/local/etc/php/ \
    && chown -R ${CONTAINER_USER} /usr/local/etc/php/ \
    && curl -sS https://getcomposer.org/installer | php ; mv composer.phar /usr/bin/composer \
    && update-exim4.conf -v

RUN sed -i "$ a xdebug.client_host="${BX_XDEBUG_IP} /usr/local/etc/php/conf.d/xdebug.ini \
    && sed -i "$ a xdebug.client_port="${BX_XDEBUG_PORT} /usr/local/etc/php/conf.d/xdebug.ini \
    && sed -i "$ a default_charset="${BX_DEFAULT_CHARSET} /usr/local/etc/php/conf.d/php.ini \
    && sed -i "$ a mbstring.internal_encoding="${BX_DEFAULT_CHARSET} /usr/local/etc/php/conf.d/mbstring.ini

#ENTRYPOINT php-fpm -F
CMD bash -c "cron && php-fpm"