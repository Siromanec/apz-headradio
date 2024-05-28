FROM consul:1.15.4 as consul

EXPOSE 8500

COPY consul.sh /consul.sh
COPY config.json /consul/config/config.json 

CMD ["/consul.sh"]