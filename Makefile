image=chatterbot:latest

run:
	@docker run --read-only -v `pwd`:/app -ti --rm $(image) /bin/bash

build:
	@docker build . -t $(image)

test:
	@nosetests

.PHONY: test build run
