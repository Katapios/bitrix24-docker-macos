FROM grafana/grafana-oss:10.2.3

# Установка плагина OpenSearch
RUN grafana-cli plugins install grafana-opensearch-datasource

# Копирование provisioning-конфигов
COPY provisioning /etc/grafana/provisioning

# Фикс прав
USER root
RUN chmod -R 755 /etc/grafana/provisioning
USER grafana

EXPOSE 3000