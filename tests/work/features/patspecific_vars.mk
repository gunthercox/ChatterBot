
/%: export foo := foo

/bar:
	@echo $(foo) $$foo
