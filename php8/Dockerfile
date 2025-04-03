FROM php:8.2-fpm

ARG APCU_VERSION=5.1.22
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

RUN apt-get update && apt-get install -y \
    cron \
    build-essential \
    locales \
    libonig-dev \
    zip \
    jpegoptim \
    optipng \
    pngquant \
    gifsicle \
    vim \
    unzip \
    git \
    graphviz \
    curl \
    supervisor \
    exim4 \
    default-mysql-client \
    default-libmysqlclient-dev \
    libmagickwand-dev \
    libjpeg62-turbo-dev \
    libfreetype6-dev \
    libmemcached-dev \
    libicu-dev \
    libzip-dev \
    zlib1g-dev \
    libpng-dev \
    libwebp-dev \
    libxml2-dev \
    libldap2-dev \
    golang \
    && rm -rf /var/lib/apt/lists/*

RUN docker-php-ext-configure gd \
    --with-freetype \
    --with-jpeg \
    --with-webp \
    && docker-php-ext-install -j$(nproc) gd

RUN docker-php-ext-install mysqli pdo_mysql

RUN docker-php-ext-install \
    opcache \
    exif \
    intl \
    sockets \
    bz2 \
    zip \
    ldap \
    && docker-php-ext-configure opcache --enable-opcache \
    && pecl install \
        apcu-${APCU_VERSION} \
        memcached \
        xdebug \
        imagick \
    && docker-php-ext-enable \
        apcu \
        memcached \
        xdebug \
        imagick

RUN go install github.com/mailhog/mhsendmail@latest \
    && cp /root/go/bin/mhsendmail /usr/bin/mhsendmail \
    && echo 'sendmail_path = /usr/bin/mhsendmail --smtp-addr mailhog:1025' > /usr/local/etc/php/conf.d/mailhog.ini

RUN groupadd -g ${CONTAINER_GID} ${CONTAINER_GROUP} \
    && useradd -u ${CONTAINER_UID} -g ${CONTAINER_GID} ${CONTAINER_USER} \
    && chown -R ${CONTAINER_USER}:${CONTAINER_GROUP} /usr/local/etc/php/ \
    && chmod -R 775 /usr/local/etc/php/

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

RUN echo "xdebug.client_host=${BX_XDEBUG_IP}" >> /usr/local/etc/php/conf.d/xdebug.ini \
    && echo "xdebug.client_port=${BX_XDEBUG_PORT}" >> /usr/local/etc/php/conf.d/xdebug.ini \
    && echo "default_charset=${BX_DEFAULT_CHARSET}" >> /usr/local/etc/php/conf.d/php.ini \
    && echo "mbstring.internal_encoding=${BX_DEFAULT_CHARSET}" >> /usr/local/etc/php/conf.d/mbstring.ini

RUN update-exim4.conf -v

CMD ["sh", "-c", "cron && php-fpm"]