foo:
	@echo Executing rule FOO

.DEFAULT:
	@$(MAKE) -f work/targets/DEFAULT.mk.1 $@ 
