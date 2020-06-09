
# We want to allow both empty commands _and_ commands that resolve to empty.
EMPTY =

.PHONY: all a1 a2 a3 a4
all: a1 a2 a3 a4

a1:;
a2:
	
a3:;$(EMPTY)
a4:
	$(EMPTY)

# Non-empty lines that expand to nothing should also be ignored.
STR =     # Some spaces
TAB =   	  # A TAB and some spaces

$(STR)

$(STR) $(TAB)
