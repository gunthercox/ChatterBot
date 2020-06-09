
all:
	$(MAKE) -f work/features/recursion.mk foo
foo:
	@echo $(MAKE)
	@echo MAKELEVEL = $(MAKELEVEL)
	$(MAKE) -f work/features/recursion.mk last
last:
	@echo $(MAKE)
	@echo MAKELEVEL = $(MAKELEVEL)
	@echo THE END
