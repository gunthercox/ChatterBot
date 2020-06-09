
ifneq ($(realpath $(abspath .)),$(CURDIR))
  $(warning .: abs="$(abspath .)" real="$(realpath $(abspath .))" curdir="$(CURDIR)")
endif

ifneq ($(realpath $(abspath ./)),$(CURDIR))
  $(warning ./: abs="$(abspath ./)" real="$(realpath $(abspath ./))" curdir="$(CURDIR)")
endif

ifneq ($(realpath $(abspath .///)),$(CURDIR))
  $(warning .///: abs="$(abspath .///)" real="$(realpath $(abspath .///))" curdir="$(CURDIR)")
endif

ifneq ($(abspath /),/)
  $(warning /: abspath="$(abspath /)")
endif

ifneq ($(abspath ///),/)
  $(warning ///: abspath="$(abspath ///)")
endif

ifneq ($(abspath /.),/)
  $(warning /.: abspath="$(abspath /.)")
endif

ifneq ($(abspath ///.),/)
  $(warning ///.: abspath="$(abspath ///.)")
endif

ifneq ($(abspath /./),/)
  $(warning /./: abspath="$(abspath /./)")
endif

ifneq ($(abspath /.///),/)
  $(warning /.///: abspath="$(abspath /.///)")
endif

ifneq ($(abspath /..),/)
  $(warning /..: abspath="$(abspath /..)")
endif

ifneq ($(abspath ///..),/)
  $(warning ///..: abspath="$(abspath ///..)")
endif

ifneq ($(abspath /../),/)
  $(warning /../: abspath="$(abspath /../)")
endif

ifneq ($(abspath /..///),/)
  $(warning /..///: abspath="$(abspath /..///)")
endif


ifneq ($(abspath /foo/bar/..),/foo)
  $(warning /foo/bar/..: abspath="$(abspath /foo/bar/..)")
endif

ifneq ($(abspath /foo/bar/../../../baz),/baz)
  $(warning /foo/bar/../../../baz: abspath="$(abspath /foo/bar/../../../baz)")
endif

ifneq ($(abspath /foo/bar/../ /..),/foo /)
  $(warning /foo/bar/../ /..: abspath="$(abspath /foo/bar/../ /..)")
endif


.PHONY: all
all: ; @:
