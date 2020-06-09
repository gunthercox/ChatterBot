
all: ; @:
$(info MAKE_RESTARTS=$(MAKE_RESTARTS))
include foo.x
foo.x: ; @touch $@
