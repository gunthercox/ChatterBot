TMP  := $(MAKE)
MAKE := $(subst X=$(X),,$(MAKE))

all:
	@echo $(TMP)
	$(MAKE) -f work/variables/MAKE.mk foo

foo:
	@echo $(MAKE)
