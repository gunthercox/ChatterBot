#                                                                    -*-perl-*-

$description = "Test the MAKEFILES variable.";

$makefile2 = &get_tmpfile;
$makefile3 = &get_tmpfile;

open(MAKEFILE,"> $makefile");
print MAKEFILE 'all: ; @echo DEFAULT RULE: M2=$(M2) M3=$(M3)', "\n";
close(MAKEFILE);


open(MAKEFILE,"> $makefile2");
print MAKEFILE <<EOF;
M2 = m2
NDEF: ; \@echo RULE FROM MAKEFILE 2
EOF
close(MAKEFILE);


open(MAKEFILE,"> $makefile3");
print MAKEFILE <<EOF;
M3 = m3
NDEF3: ; \@echo RULE FROM MAKEFILE 3
EOF
close(MAKEFILE);


&run_make_with_options($makefile, "MAKEFILES='$makefile2 $makefile3'",
                       &get_logfile);
$answer = "DEFAULT RULE: M2=m2 M3=m3\n";
&compare_output($answer,&get_logfile(1));

1;
