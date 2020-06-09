
all : def_1 def_2 def_3
def_1 : ; @echo ONE; sleep 3 ; echo TWO
def_2 : ; @sleep 2 ; echo THREE
def_3 : ; @sleep 1 ; echo FOUR
