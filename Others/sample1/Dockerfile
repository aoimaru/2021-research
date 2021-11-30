FROM php:8-fpm

RUN apt-get update && apt-get install -y --no-install-recommends \
    --allow-downgrades --allow-remove-essential --allow-change-held-packages \
    && pecl install redis \
    && pecl install xdebug \
    && docker-php-ext-enable redis xdebug \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


###########

RUN apt-get update && apt-get install -y --no-install-recommends \
    --allow-downgrades --allow-remove-essential --allow-change-held-packages \
        libpspell-dev \
    && docker-php-ext-install -j$(nproc) pspell \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN apt-get update && apt-get install -y --no-install-recommends \
    --allow-downgrades --allow-remove-essential --allow-change-held-packages \
        libpng-dev \
    && docker-php-ext-install -j$(nproc) gd \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN apt-get update && apt-get install -y --no-install-recommends \
    --allow-downgrades --allow-remove-essential --allow-change-held-packages \
       libzip-dev \
    && docker-php-ext-install -j$(nproc) zip \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN apt-get update && apt-get install -y --no-install-recommends \
    --allow-downgrades --allow-remove-essential --allow-change-held-packages \
        \
    && docker-php-ext-install -j$(nproc) bcmath \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN apt-get update && apt-get install -y --no-install-recommends \
    --allow-downgrades --allow-remove-essential --allow-change-held-packages \
       libbz2-dev \
    && docker-php-ext-install -j$(nproc) bz2 \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN apt-get update && apt-get install -y --no-install-recommends \
    --allow-downgrades --allow-remove-essential --allow-change-held-packages \
        \
    && docker-php-ext-install -j$(nproc) calendar \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN apt-get update && apt-get install -y --no-install-recommends \
    --allow-downgrades --allow-remove-essential --allow-change-held-packages \
        \
    && docker-php-ext-install -j$(nproc) opcache \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN apt-get update && apt-get install -y --no-install-recommends \
    --allow-downgrades --allow-remove-essential --allow-change-held-packages \
        \
    && docker-php-ext-install -j$(nproc) gettext \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN apt-get update && apt-get install -y --no-install-recommends \
    --allow-downgrades --allow-remove-essential --allow-change-held-packages \
       libldap-dev \
    && docker-php-ext-install -j$(nproc) ldap \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN set -x && \
    apt-get update && apt-get install -y --no-install-recommends \
    --allow-downgrades --allow-remove-essential --allow-change-held-packages \
       unixodbc-dev \
    && docker-php-source extract \
    && cd /usr/src/php/ext/odbc \
    && phpize \
    && sed -ri 's@^ *test +"\$PHP_.*" *= *"no" *&& *PHP_.*=yes *$@#&@g' configure \
    && ./configure --with-unixODBC=shared,/usr \
    && docker-php-ext-install odbc \
    && docker-php-source delete \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN apt-get update && apt-get install -y --no-install-recommends \
    --allow-downgrades --allow-remove-essential --allow-change-held-packages \
       libmemcached-dev \
    && pecl install memcached \
    && docker-php-ext-enable memcached \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN apt-get update && apt-get install -y --no-install-recommends \
    --allow-downgrades --allow-remove-essential --allow-change-held-packages \
       libpq-dev \
    && docker-php-ext-install -j$(nproc) pgsql pdo_pgsql \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*



RUN mv "$PHP_INI_DIR/php.ini-development" "$PHP_INI_DIR/php.ini"


RUN sed -e 's/;error_log = php_errors.log/error_log = \/var\/log\/apache2\/php_error.log/' -i /usr/local/etc/php/php.ini
RUN sed -e 's/display_errors = Off/display_errors = On/' -i /usr/local/etc/php/php.ini
RUN sed -e 's/display_startup_errors = Off/display_startup_errors = On/' -i /usr/local/etc/php/php.ini

RUN apt-get update && apt-get install -y --no-install-recommends \
    --allow-downgrades --allow-remove-essential --allow-change-held-packages \
        \
    && apt-get install -y syslog-ng \
    && systemctl enable syslog-ng \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY ./syslog-ng /etc/default/syslog-ng
COPY ./syslogView.sh /usr/bin/syslogView.sh

COPY ./xdebug.ini /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini

RUN chmod 755 /usr/bin/syslogView.sh

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer
RUN composer self-update

WORKDIR /var/www

CMD ["php-fpm"]