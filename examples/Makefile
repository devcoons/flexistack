cnf ?= Makefile.env
include $(cnf)

ifeq ($(OS), Windows_NT)
	CATCH=2>NUL || VER>NUL
else
	CATCH=2>/dev/null ; true
endif

ifeq (, $(shell where podman))
	DOCKER := $(shell where docker)
	ifeq (, $(DOCKER))
		$(error "Neither Docker nor Podman is installed. Please install one of them.")
	endif
	CONTAINER_ENGINE := docker
else
	CONTAINER_ENGINE := podman
endif

build:  
	-$(CONTAINER_ENGINE) build --no-cache -f Dockerfile -t $(APP_IMG):$(APP_VERSION) "$(CURDIR)/"
		
run:
	-$(CONTAINER_ENGINE) start $(APP_NAME) $(CATCH)
	-$(CONTAINER_ENGINE) run -d --name $(APP_NAME) $(APP_IMG):$(APP_VERSION) $(CATCH)
	
connect:
	-$(CONTAINER_ENGINE) exec -w /home -it $(APP_NAME) /bin/bash $(CATCH)
	
stop:
	-$(CONTAINER_ENGINE) kill $(APP_NAME) $(CATCH)

remove:	
	-$(CONTAINER_ENGINE) rm $(APP_NAME) $(CATCH)

discard:
	-$(CONTAINER_ENGINE) kill $(APP_NAME) $(CATCH)
	-$(CONTAINER_ENGINE) rm $(APP_NAME) $(CATCH)
	
delete:
	-$(CONTAINER_ENGINE) image rm $(APP_IMG):$(APP_VERSION) $(CATCH)
	-$(CONTAINER_ENGINE) system prune -f $(CATCH)
