
# provides HTTP_PORT, HTTPS_PORT, and DOMAIN
include ../.env

SOCKET := /run/uwsgi/$(DOMAIN)/socket.sock
WEBSOCKET := /run/uwsgi/$(DOMAIN)/socket_websocket.sock

export DOMAIN

ifeq ($(DOMAIN),)
	$(error DOMAIN must be set in enviroment or ../.env file)
endif

all:

.phony: install

clean:
	rm -rf objects
	rm -rf ../image/nginx

objects/:
	mkdir --parent objects

../image/nginx/config: ../image/config/nginx_config
	mkdir --parent $(@D)
	envsubst < $< > $@

objects/image_nginx_config: ../image/nginx/config objects/
	touch $@

objects/install: host_nginx_config objects/
	sed \
	-e "s/'{domain_name}'/$(DOMAIN)/g" \
	-e "s;'{SOCKET}';$(SOCKET);g" \
	-e "s;'{WEBSOCKET}';$(WEBSOCKET);g" \
	-e "s;'{PORT}';$(PORT);g" \
	$< > objects/_temp_test_config && \
	cp -f objects/_temp_test_config /etc/nginx/sites-enabled/$(DOMAIN)
	nginx -t
	systemctl restart nginx
	touch $@

objects/install_ssl: objects/install
	certbot --nginx -d $(DOMAIN) --redirect
	nginx -t
	systemctl restart nginx
	touch $@

install: objects/install

install_ssl: objects/install_ssl
