
FOO = foo
BAR = bar
BOZ = boz

export BAZ = baz
export BOZ

BITZ = bitz
BOTZ = botz

export BITZ BOTZ
unexport BOTZ

ifdef EXPORT_ALL
export
endif

ifdef UNEXPORT_ALL
unexport
endif

ifdef EXPORT_ALL_PSEUDO
.EXPORT_ALL_VARIABLES:
endif

all:
	@echo "FOO=$(FOO) BAR=$(BAR) BAZ=$(BAZ) BOZ=$(BOZ) BITZ=$(BITZ) BOTZ=$(BOTZ)"
	@echo "FOO=$$FOO BAR=$$BAR BAZ=$$BAZ BOZ=$$BOZ BITZ=$$BITZ BOTZ=$$BOTZ"

