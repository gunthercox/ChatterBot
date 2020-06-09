#!/usr/bin/perl
# -*-perl-*-
#
# Modification history:
# Written 91-12-02 through 92-01-01 by Stephen McGee.
# Modified 92-02-11 through 92-02-22 by Chris Arthur to further generalize.
#
# Copyright (C) 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000,
# 2001, 2002, 2003, 2004, 2005, 2006 Free Software Foundation, Inc.
# This file is part of GNU Make.
#
# GNU Make is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2, or (at your option) any later version.
#
# GNU Make is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# GNU Make; see the file COPYING.  If not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.


# Test driver routines used by a number of test suites, including
# those for SCS, make, roll_dir, and scan_deps (?).
#
# this routine controls the whole mess; each test suite sets up a few
# variables and then calls &toplevel, which does all the real work.

# $Id: test_driver.pl,v 1.19 2006/03/10 02:20:45 psmith Exp $


# The number of test categories we've run
$categories_run = 0;
# The number of test categroies that have passed
$categories_passed = 0;
# The total number of individual tests that have been run
$total_tests_run = 0;
# The total number of individual tests that have passed
$total_tests_passed = 0;
# The number of tests in this category that have been run
$tests_run = 0;
# The number of tests in this category that have passed
$tests_passed = 0;


# Yeesh.  This whole test environment is such a hack!
$test_passed = 1;


# %makeENV is the cleaned-out environment.
%makeENV = ();

# %extraENV are any extra environment variables the tests might want to set.
# These are RESET AFTER EVERY TEST!
%extraENV = ();

# %origENV is the caller's original environment
%origENV = %ENV;

sub resetENV
{
  # We used to say "%ENV = ();" but this doesn't work in Perl 5.000
  # through Perl 5.004.  It was fixed in Perl 5.004_01, but we don't
  # want to require that here, so just delete each one individually.
  foreach $v (keys %ENV) {
    delete $ENV{$v};
  }

  %ENV = %makeENV;
  foreach $v (keys %extraENV) {
    $ENV{$v} = $extraENV{$v};
    delete $extraENV{$v};
  }
}

sub toplevel
{
  # Pull in benign variables from the user's environment
  #
  foreach (# UNIX-specific things
           'TZ', 'LANG', 'TMPDIR', 'HOME', 'USER', 'LOGNAME', 'PATH',
           # Purify things
           'PURIFYOPTIONS',
           # Windows NT-specific stuff
           'Path', 'SystemRoot',
           # DJGPP-specific stuff
           'DJDIR', 'DJGPP', 'SHELL', 'COMSPEC', 'HOSTNAME', 'LFN',
           'FNCASE', '387', 'EMU387', 'GROUP'
          ) {
    $makeENV{$_} = $ENV{$_} if $ENV{$_};
  }

  # Replace the environment with the new one
  #
  %origENV = %ENV;

  resetENV();

  $| = 1;                     # unbuffered output

  $debug = 0;                 # debug flag
  $profile = 0;               # profiling flag
  $verbose = 0;               # verbose mode flag
  $detail = 0;                # detailed verbosity
  $keep = 0;                  # keep temp files around
  $workdir = "work";          # The directory where the test will start running
  $scriptdir = "scripts";     # The directory where we find the test scripts
  $tmpfilesuffix = "t";       # the suffix used on tmpfiles
  $default_output_stack_level = 0;  # used by attach_default_output, etc.
  $default_input_stack_level = 0;   # used by attach_default_input, etc.
  $cwd = ".";                 # don't we wish we knew
  $cwdslash = "";             # $cwd . $pathsep, but "" rather than "./"

  &get_osname;  # sets $osname, $vos, $pathsep, and $short_filenames

  &set_defaults;  # suite-defined

  &parse_command_line (@ARGV);

  print "OS name = `$osname'\n" if $debug;

  $workpath = "$cwdslash$workdir";
  $scriptpath = "$cwdslash$scriptdir";

  &set_more_defaults;  # suite-defined

  &print_banner;

  if (-d $workpath)
  {
    print "Clearing $workpath...\n";
    &remove_directory_tree("$workpath/")
          || &error ("Couldn't wipe out $workpath\n");
  }
  else
  {
    mkdir ($workpath, 0777) || &error ("Couldn't mkdir $workpath: $!\n");
  }

  if (!-d $scriptpath)
  {
    &error ("Failed to find $scriptpath containing perl test scripts.\n");
  }

  if (@TESTS)
  {
    print "Making work dirs...\n";
    foreach $test (@TESTS)
    {
      if ($test =~ /^([^\/]+)\//)
      {
        $dir = $1;
        push (@rmdirs, $dir);
        -d "$workpath/$dir"
	   || mkdir ("$workpath/$dir", 0777)
           || &error ("Couldn't mkdir $workpath/$dir: $!\n");
      }
    }
  }
  else
  {
    print "Finding tests...\n";
    opendir (SCRIPTDIR, $scriptpath)
	|| &error ("Couldn't opendir $scriptpath: $!\n");
    @dirs = grep (!/^(\..*|CVS|RCS)$/, readdir (SCRIPTDIR) );
    closedir (SCRIPTDIR);
    foreach $dir (@dirs)
    {
      next if ($dir =~ /^(\..*|CVS|RCS)$/ || ! -d "$scriptpath/$dir");
      push (@rmdirs, $dir);
      mkdir ("$workpath/$dir", 0777)
           || &error ("Couldn't mkdir $workpath/$dir: $!\n");
      opendir (SCRIPTDIR, "$scriptpath/$dir")
	  || &error ("Couldn't opendir $scriptpath/$dir: $!\n");
      @files = grep (!/^(\..*|CVS|RCS|.*~)$/, readdir (SCRIPTDIR) );
      closedir (SCRIPTDIR);
      foreach $test (@files)
      {
        -d $test and next;
	push (@TESTS, "$dir/$test");
      }
    }
  }

  if (@TESTS == 0)
  {
    &error ("\nNo tests in $scriptpath, and none were specified.\n");
  }

  print "\n";

  &run_each_test;

  foreach $dir (@rmdirs)
  {
    rmdir ("$workpath/$dir");
  }

  $| = 1;

  $categories_failed = $categories_run - $categories_passed;
  $total_tests_failed = $total_tests_run - $total_tests_passed;

  if ($total_tests_failed)
  {
    print "\n$total_tests_failed Test";
    print "s" unless $total_tests_failed == 1;
    print " in $categories_failed Categor";
    print ($categories_failed == 1 ? "y" : "ies");
    print " Failed (See .$diffext files in $workdir dir for details) :-(\n\n";
    return 0;
  }
  else
  {
    print "\n$total_tests_passed Test";
    print "s" unless $total_tests_passed == 1;
    print " in $categories_passed Categor";
    print ($categories_passed == 1 ? "y" : "ies");
    print " Complete ... No Failures :-)\n\n";
    return 1;
  }
}

sub get_osname
{
  # Set up an initial value.  In perl5 we can do it the easy way.
  #
  $osname = defined($^O) ? $^O : '';

  # See if the filesystem supports long file names with multiple
  # dots.  DOS doesn't.
  $short_filenames = 0;
  (open (TOUCHFD, "> fancy.file.name") && close (TOUCHFD))
      || ($short_filenames = 1);
  unlink ("fancy.file.name") || ($short_filenames = 1);

  if (! $short_filenames) {
    # Thanks go to meyering@cs.utexas.edu (Jim Meyering) for suggesting a
    # better way of doing this.  (We used to test for existence of a /mnt
    # dir, but that apparently fails on an SGI Indigo (whatever that is).)
    # Because perl on VOS translates /'s to >'s, we need to test for
    # VOSness rather than testing for Unixness (ie, try > instead of /).

    mkdir (".ostest", 0777) || &error ("Couldn't create .ostest: $!\n", 1);
    open (TOUCHFD, "> .ostest>ick") && close (TOUCHFD);
    chdir (".ostest") || &error ("Couldn't chdir to .ostest: $!\n", 1);
  }

  if (! $short_filenames && -f "ick")
  {
    $osname = "vos";
    $vos = 1;
    $pathsep = ">";
  }
  else
  {
    # the following is regrettably knarly, but it seems to be the only way
    # to not get ugly error messages if uname can't be found.
    # Hmmm, BSD/OS 2.0's uname -a is excessively verbose.  Let's try it
    # with switches first.
    eval "chop (\$osname = `sh -c 'uname -nmsr 2>&1'`)";
    if ($osname =~ /not found/i)
    {
	$osname = "(something unixy with no uname)";
    }
    elsif ($@ ne "" || $?)
    {
        eval "chop (\$osname = `sh -c 'uname -a 2>&1'`)";
        if ($@ ne "" || $?)
        {
	    $osname = "(something unixy)";
	}
    }
    $vos = 0;
    $pathsep = "/";
  }

  if (! $short_filenames) {
    chdir ("..") || &error ("Couldn't chdir to ..: $!\n", 1);
    unlink (".ostest>ick");
    rmdir (".ostest") || &error ("Couldn't rmdir .ostest: $!\n", 1);
  }
}

sub parse_command_line
{
  @argv = @_;

  # use @ARGV if no args were passed in

  if (@argv == 0)
  {
    @argv = @ARGV;
  }

  # look at each option; if we don't recognize it, maybe the suite-specific
  # command line parsing code will...

  while (@argv)
  {
    $option = shift @argv;
    if ($option =~ /^-debug$/i)
    {
      print "\nDEBUG ON\n";
      $debug = 1;
    }
    elsif ($option =~ /^-usage$/i)
    {
      &print_usage;
      exit 0;
    }
    elsif ($option =~ /^-(h|help)$/i)
    {
      &print_help;
      exit 0;
    }
    elsif ($option =~ /^-profile$/i)
    {
      $profile = 1;
    }
    elsif ($option =~ /^-verbose$/i)
    {
      $verbose = 1;
    }
    elsif ($option =~ /^-detail$/i)
    {
      $detail = 1;
      $verbose = 1;
    }
    elsif ($option =~ /^-keep$/i)
    {
      $keep = 1;
    }
    elsif (&valid_option($option))
    {
      # The suite-defined subroutine takes care of the option
    }
    elsif ($option =~ /^-/)
    {
      print "Invalid option: $option\n";
      &print_usage;
      exit 0;
    }
    else # must be the name of a test
    {
      $option =~ s/\.pl$//;
      push(@TESTS,$option);
    }
  }
}

sub max
{
  local($num) = shift @_;
  local($newnum);

  while (@_)
  {
    $newnum = shift @_;
    if ($newnum > $num)
    {
      $num = $newnum;
    }
  }

  return $num;
}

sub print_centered
{
  local($width, $string) = @_;
  local($pad);

  if (length ($string))
  {
    $pad = " " x ( ($width - length ($string) + 1) / 2);
    print "$pad$string";
  }
}

sub print_banner
{
  local($info);
  local($line);
  local($len);

  $info = "Running tests for $testee on $osname\n";  # $testee is suite-defined
  $len = &max (length ($line), length ($testee_version),
               length ($banner_info), 73) + 5;
  $line = ("-" x $len) . "\n";
  if ($len < 78)
  {
    $len = 78;
  }

  &print_centered ($len, $line);
  &print_centered ($len, $info);
  &print_centered ($len, $testee_version);  # suite-defined
  &print_centered ($len, $banner_info);     # suite-defined
  &print_centered ($len, $line);
  print "\n";
}

sub run_each_test
{
  $categories_run = 0;

  foreach $testname (sort @TESTS)
  {
    ++$categories_run;
    $suite_passed = 1;       # reset by test on failure
    $num_of_logfiles = 0;
    $num_of_tmpfiles = 0;
    $description = "";
    $details = "";
    $old_makefile = undef;
    $testname =~ s/^$scriptpath$pathsep//;
    $perl_testname = "$scriptpath$pathsep$testname";
    $testname =~ s/(\.pl|\.perl)$//;
    $testpath = "$workpath$pathsep$testname";
    # Leave enough space in the extensions to append a number, even
    # though it needs to fit into 8+3 limits.
    if ($short_filenames) {
      $logext = 'l';
      $diffext = 'd';
      $baseext = 'b';
      $extext = '';
    } else {
      $logext = 'log';
      $diffext = 'diff';
      $baseext = 'base';
      $extext = '.';
    }
    $log_filename = "$testpath.$logext";
    $diff_filename = "$testpath.$diffext";
    $base_filename = "$testpath.$baseext";
    $tmp_filename = "$testpath.$tmpfilesuffix";

    &setup_for_test;          # suite-defined

    $output = "........................................................ ";

    substr($output,0,length($testname)) = "$testname ";

    print $output;

    # Run the actual test!
    $tests_run = 0;
    $tests_passed = 0;
    $code = do $perl_testname;

    $total_tests_run += $tests_run;
    $total_tests_passed += $tests_passed;

    # How did it go?
    if (!defined($code))
    {
      $suite_passed = 0;
      if (length ($@)) {
        warn "\n*** Test died ($testname): $@\n";
      } else {
        warn "\n*** Couldn't run $perl_testname\n";
      }
    }
    elsif ($code == -1) {
      $suite_passed = 0;
    }
    elsif ($code != 1 && $code != -1) {
      $suite_passed = 0;
      warn "\n*** Test returned $code\n";
    }

    if ($suite_passed) {
      ++$categories_passed;
      $status = "ok     ($tests_passed passed)";
      for ($i = $num_of_tmpfiles; $i; $i--)
      {
        &rmfiles ($tmp_filename . &num_suffix ($i) );
      }

      for ($i = $num_of_logfiles ? $num_of_logfiles : 1; $i; $i--)
      {
        &rmfiles ($log_filename . &num_suffix ($i) );
        &rmfiles ($base_filename . &num_suffix ($i) );
      }
    }
    elsif (!defined $code || $code > 0) {
      $status = "FAILED ($tests_passed/$tests_run passed)";
    }
    elsif ($code < 0) {
      $status = "N/A";
      --$categories_run;
    }

    # If the verbose option has been specified, then a short description
    # of each test is printed before displaying the results of each test
    # describing WHAT is being tested.

    if ($verbose)
    {
      if ($detail)
      {
        print "\nWHAT IS BEING TESTED\n";
        print "--------------------";
      }
      print "\n\n$description\n\n";
    }

    # If the detail option has been specified, then the details of HOW
    # the test is testing what it says it is testing in the verbose output
    # will be displayed here before the results of the test are displayed.

    if ($detail)
    {
      print "\nHOW IT IS TESTED\n";
      print "----------------";
      print "\n\n$details\n\n";
    }

    print "$status\n";
  }
}

# If the keep flag is not set, this subroutine deletes all filenames that
# are sent to it.

sub rmfiles
{
  local(@files) = @_;

  if (!$keep)
  {
    return (unlink @files);
  }

  return 1;
}

sub print_standard_usage
{
  local($plname,@moreusage) = @_;
  local($line);

  print "Usage:  perl $plname [testname] [-verbose] [-detail] [-keep]\n";
  print "                               [-profile] [-usage] [-help] "
      . "[-debug]\n";
  foreach $line (@moreusage)
  {
    print "                               $line\n";
  }
}

sub print_standard_help
{
  local(@morehelp) = @_;
  local($line);
  local($tline);
  local($t) = "      ";

  $line = "Test Driver For $testee";
  print "$line\n";
  $line = "=" x length ($line);
  print "$line\n";

  &print_usage;

  print "\ntestname\n"
      . "${t}You may, if you wish, run only ONE test if you know the name\n"
      . "${t}of that test and specify this name anywhere on the command\n"
      . "${t}line.  Otherwise ALL existing tests in the scripts directory\n"
      . "${t}will be run.\n"
      . "-verbose\n"
      . "${t}If this option is given, a description of every test is\n"
      . "${t}displayed before the test is run. (Not all tests may have\n"
      . "${t}descriptions at this time)\n"
      . "-detail\n"
      . "${t}If this option is given, a detailed description of every\n"
      . "${t}test is displayed before the test is run. (Not all tests\n"
      . "${t}have descriptions at this time)\n"
      . "-profile\n"
      . "${t}If this option is given, then the profile file\n"
      . "${t}is added to other profiles every time $testee is run.\n"
      . "${t}This option only works on VOS at this time.\n"
      . "-keep\n"
      . "${t}You may give this option if you DO NOT want ANY\n"
      . "${t}of the files generated by the tests to be deleted. \n"
      . "${t}Without this option, all files generated by the test will\n"
      . "${t}be deleted IF THE TEST PASSES.\n"
      . "-debug\n"
      . "${t}Use this option if you would like to see all of the system\n"
      . "${t}calls issued and their return status while running the tests\n"
      . "${t}This can be helpful if you're having a problem adding a test\n"
      . "${t}to the suite, or if the test fails!\n";

  foreach $line (@morehelp)
  {
    $tline = $line;
    if (substr ($tline, 0, 1) eq "\t")
    {
      substr ($tline, 0, 1) = $t;
    }
    print "$tline\n";
  }
}

#######################################################################
###########         Generic Test Driver Subroutines         ###########
#######################################################################

sub get_caller
{
  local($depth);
  local($package);
  local($filename);
  local($linenum);

  $depth = defined ($_[0]) ? $_[0] : 1;
  ($package, $filename, $linenum) = caller ($depth + 1);
  return "$filename: $linenum";
}

sub error
{
  local($message) = $_[0];
  local($caller) = &get_caller (1);

  if (defined ($_[1]))
  {
    $caller = &get_caller ($_[1] + 1) . " -> $caller";
  }

  die "$caller: $message";
}

sub compare_output
{
  local($answer,$logfile) = @_;
  local($slurp, $answer_matched) = ('', 0);

  print "Comparing Output ........ " if $debug;

  $slurp = &read_file_into_string ($logfile);

  # For make, get rid of any time skew error before comparing--too bad this
  # has to go into the "generic" driver code :-/
  $slurp =~ s/^.*modification time .*in the future.*\n//gm;
  $slurp =~ s/^.*Clock skew detected.*\n//gm;

  ++$tests_run;

  if ($slurp eq $answer) {
    $answer_matched = 1;
  } else {
    # See if it is a slash or CRLF problem
    local ($answer_mod) = $answer;

    $answer_mod =~ tr,\\,/,;
    $answer_mod =~ s,\r\n,\n,gs;

    $slurp =~ tr,\\,/,;
    $slurp =~ s,\r\n,\n,gs;

    $answer_matched = ($slurp eq $answer_mod);
  }

  if ($answer_matched && $test_passed)
  {
    print "ok\n" if $debug;
    ++$tests_passed;
    return 1;
  }

  if (! $answer_matched) {
    print "DIFFERENT OUTPUT\n" if $debug;

    &create_file (&get_basefile, $answer);

    print "\nCreating Difference File ...\n" if $debug;

    # Create the difference file

    local($command) = "diff -c " . &get_basefile . " " . $logfile;
    &run_command_with_output(&get_difffile,$command);
  }

  $suite_passed = 0;
  return 0;
}

sub read_file_into_string
{
  local($filename) = @_;
  local($oldslash) = $/;

  undef $/;

  open (RFISFILE, $filename) || return "";
  local ($slurp) = <RFISFILE>;
  close (RFISFILE);

  $/ = $oldslash;

  return $slurp;
}

sub attach_default_output
{
  local ($filename) = @_;
  local ($code);

  if ($vos)
  {
    $code = system "++attach_default_output_hack $filename";
    $code == -2 || &error ("adoh death\n", 1);
    return 1;
  }

  open ("SAVEDOS" . $default_output_stack_level . "out", ">&STDOUT")
        || &error ("ado: $! duping STDOUT\n", 1);
  open ("SAVEDOS" . $default_output_stack_level . "err", ">&STDERR")
        || &error ("ado: $! duping STDERR\n", 1);

  open (STDOUT, "> " . $filename)
        || &error ("ado: $filename: $!\n", 1);
  open (STDERR, ">&STDOUT")
        || &error ("ado: $filename: $!\n", 1);

  $default_output_stack_level++;
}

# close the current stdout/stderr, and restore the previous ones from
# the "stack."

sub detach_default_output
{
  local ($code);

  if ($vos)
  {
    $code = system "++detach_default_output_hack";
    $code == -2 || &error ("ddoh death\n", 1);
    return 1;
  }

  if (--$default_output_stack_level < 0)
  {
    &error ("default output stack has flown under!\n", 1);
  }

  close (STDOUT);
  close (STDERR);

  open (STDOUT, ">&SAVEDOS" . $default_output_stack_level . "out")
        || &error ("ddo: $! duping STDOUT\n", 1);
  open (STDERR, ">&SAVEDOS" . $default_output_stack_level . "err")
        || &error ("ddo: $! duping STDERR\n", 1);

  close ("SAVEDOS" . $default_output_stack_level . "out")
        || &error ("ddo: $! closing SCSDOSout\n", 1);
  close ("SAVEDOS" . $default_output_stack_level . "err")
         || &error ("ddo: $! closing SAVEDOSerr\n", 1);
}

# run one command (passed as a list of arg 0 - n), returning 0 on success
# and nonzero on failure.

sub run_command
{
  local ($code);

  # We reset this before every invocation.  On Windows I think there is only
  # one environment, not one per process, so I think that variables set in
  # test scripts might leak into subsequent tests if this isn't reset--???
  resetENV();

  print "\nrun_command: @_\n" if $debug;
  $code = system @_;
  print "run_command: \"@_\" returned $code.\n" if $debug;

  return $code;
}

# run one command (passed as a list of arg 0 - n, with arg 0 being the
# second arg to this routine), returning 0 on success and non-zero on failure.
# The first arg to this routine is a filename to connect to the stdout
# & stderr of the child process.

sub run_command_with_output
{
  local ($filename) = shift;
  local ($code);

  # We reset this before every invocation.  On Windows I think there is only
  # one environment, not one per process, so I think that variables set in
  # test scripts might leak into subsequent tests if this isn't reset--???
  resetENV();

  &attach_default_output ($filename);
  $code = system @_;
  &detach_default_output;

  print "run_command_with_output: '@_' returned $code.\n" if $debug;

  return $code;
}

# performs the equivalent of an "rm -rf" on the first argument.  Like
# rm, if the path ends in /, leaves the (now empty) directory; otherwise
# deletes it, too.

sub remove_directory_tree
{
  local ($targetdir) = @_;
  local ($nuketop) = 1;
  local ($ch);

  $ch = substr ($targetdir, length ($targetdir) - 1);
  if ($ch eq "/" || $ch eq $pathsep)
  {
    $targetdir = substr ($targetdir, 0, length ($targetdir) - 1);
    $nuketop = 0;
  }

  if (! -e $targetdir)
  {
    return 1;
  }

  &remove_directory_tree_inner ("RDT00", $targetdir) || return 0;
  if ($nuketop)
  {
    rmdir $targetdir || return 0;
  }

  return 1;
}

sub remove_directory_tree_inner
{
  local ($dirhandle, $targetdir) = @_;
  local ($object);
  local ($subdirhandle);

  opendir ($dirhandle, $targetdir) || return 0;
  $subdirhandle = $dirhandle;
  $subdirhandle++;
  while ($object = readdir ($dirhandle))
  {
    if ($object =~ /^(\.\.?|CVS|RCS)$/)
    {
      next;
    }

    $object = "$targetdir$pathsep$object";
    lstat ($object);

    if (-d _ && &remove_directory_tree_inner ($subdirhandle, $object))
    {
      rmdir $object || return 0;
    }
    else
    {
      unlink $object || return 0;
    }
  }
  closedir ($dirhandle);
  return 1;
}

# We used to use this behavior for this function:
#
#sub touch
#{
#  local (@filenames) = @_;
#  local ($now) = time;
#  local ($file);
#
#  foreach $file (@filenames)
#  {
#    utime ($now, $now, $file)
#          || (open (TOUCHFD, ">> $file") && close (TOUCHFD))
#               || &error ("Couldn't touch $file: $!\n", 1);
#  }
#  return 1;
#}
#
# But this behaves badly on networked filesystems where the time is
# skewed, because it sets the time of the file based on the _local_
# host.  Normally when you modify a file, it's the _remote_ host that
# determines the modtime, based on _its_ clock.  So, instead, now we open
# the file and write something into it to force the remote host to set
# the modtime correctly according to its clock.
#

sub touch
{
  local ($file);

  foreach $file (@_) {
    (open(T, ">> $file") && print(T "\n") && close(T))
	|| &error("Couldn't touch $file: $!\n", 1);
  }
}

# Touch with a time offset.  To DTRT, call touch() then use stat() to get the
# access/mod time for each file and apply the offset.

sub utouch
{
  local ($off) = shift;
  local ($file);

  &touch(@_);

  local (@s) = stat($_[0]);

  utime($s[8]+$off, $s[9]+$off, @_);
}

# open a file, write some stuff to it, and close it.

sub create_file
{
  local ($filename, @lines) = @_;

  open (CF, "> $filename") || &error ("Couldn't open $filename: $!\n", 1);
  foreach $line (@lines)
  {
    print CF $line;
  }
  close (CF);
}

# create a directory tree described by an associative array, wherein each
# key is a relative pathname (using slashes) and its associated value is
# one of:
#    DIR            indicates a directory
#    FILE:contents  indicates a file, which should contain contents +\n
#    LINK:target    indicates a symlink, pointing to $basedir/target
# The first argument is the dir under which the structure will be created
# (the dir will be made and/or cleaned if necessary); the second argument
# is the associative array.

sub create_dir_tree
{
  local ($basedir, %dirtree) = @_;
  local ($path);

  &remove_directory_tree ("$basedir");
  mkdir ($basedir, 0777) || &error ("Couldn't mkdir $basedir: $!\n", 1);

  foreach $path (sort keys (%dirtree))
  {
    if ($dirtree {$path} =~ /^DIR$/)
    {
      mkdir ("$basedir/$path", 0777)
               || &error ("Couldn't mkdir $basedir/$path: $!\n", 1);
    }
    elsif ($dirtree {$path} =~ /^FILE:(.*)$/)
    {
      &create_file ("$basedir/$path", $1 . "\n");
    }
    elsif ($dirtree {$path} =~ /^LINK:(.*)$/)
    {
      symlink ("$basedir/$1", "$basedir/$path")
        || &error ("Couldn't symlink $basedir/$path -> $basedir/$1: $!\n", 1);
    }
    else
    {
      &error ("Bogus dirtree type: \"$dirtree{$path}\"\n", 1);
    }
  }
  if ($just_setup_tree)
  {
    die "Tree is setup...\n";
  }
}

# compare a directory tree with an associative array in the format used
# by create_dir_tree, above.
# The first argument is the dir under which the structure should be found;
# the second argument is the associative array.

sub compare_dir_tree
{
  local ($basedir, %dirtree) = @_;
  local ($path);
  local ($i);
  local ($bogus) = 0;
  local ($contents);
  local ($target);
  local ($fulltarget);
  local ($found);
  local (@files);
  local (@allfiles);

  opendir (DIR, $basedir) || &error ("Couldn't open $basedir: $!\n", 1);
  @allfiles = grep (!/^(\.\.?|CVS|RCS)$/, readdir (DIR) );
  closedir (DIR);
  if ($debug)
  {
    print "dirtree: (%dirtree)\n$basedir: (@allfiles)\n";
  }

  foreach $path (sort keys (%dirtree))
  {
    if ($debug)
    {
      print "Checking $path ($dirtree{$path}).\n";
    }

    $found = 0;
    foreach $i (0 .. $#allfiles)
    {
      if ($allfiles[$i] eq $path)
      {
        splice (@allfiles, $i, 1);  # delete it
        if ($debug)
        {
          print "     Zapped $path; files now (@allfiles).\n";
        }
        lstat ("$basedir/$path");
        $found = 1;
        last;
      }
    }

    if (!$found)
    {
      print "compare_dir_tree: $path does not exist.\n";
      $bogus = 1;
      next;
    }

    if ($dirtree {$path} =~ /^DIR$/)
    {
      if (-d _ && opendir (DIR, "$basedir/$path") )
      {
        @files = readdir (DIR);
        closedir (DIR);
        @files = grep (!/^(\.\.?|CVS|RCS)$/ && ($_ = "$path/$_"), @files);
        push (@allfiles, @files);
        if ($debug)
        {
          print "     Read in $path; new files (@files).\n";
        }
      }
      else
      {
        print "compare_dir_tree: $path is not a dir.\n";
        $bogus = 1;
      }
    }
    elsif ($dirtree {$path} =~ /^FILE:(.*)$/)
    {
      if (-l _ || !-f _)
      {
        print "compare_dir_tree: $path is not a file.\n";
        $bogus = 1;
        next;
      }

      if ($1 ne "*")
      {
        $contents = &read_file_into_string ("$basedir/$path");
        if ($contents ne "$1\n")
        {
          print "compare_dir_tree: $path contains wrong stuff."
              . "  Is:\n$contentsShould be:\n$1\n";
          $bogus = 1;
        }
      }
    }
    elsif ($dirtree {$path} =~ /^LINK:(.*)$/)
    {
      $target = $1;
      if (!-l _)
      {
        print "compare_dir_tree: $path is not a link.\n";
        $bogus = 1;
        next;
      }

      $contents = readlink ("$basedir/$path");
      $contents =~ tr/>/\//;
      $fulltarget = "$basedir/$target";
      $fulltarget =~ tr/>/\//;
      if (!($contents =~ /$fulltarget$/))
      {
        if ($debug)
        {
          $target = $fulltarget;
        }
        print "compare_dir_tree: $path should be link to $target, "
            . "not $contents.\n";
        $bogus = 1;
      }
    }
    else
    {
      &error ("Bogus dirtree type: \"$dirtree{$path}\"\n", 1);
    }
  }

  if ($debug)
  {
    print "leftovers: (@allfiles).\n";
  }

  foreach $file (@allfiles)
  {
    print "compare_dir_tree: $file should not exist.\n";
    $bogus = 1;
  }

  return !$bogus;
}

# this subroutine generates the numeric suffix used to keep tmp filenames,
# log filenames, etc., unique.  If the number passed in is 1, then a null
# string is returned; otherwise, we return ".n", where n + 1 is the number
# we were given.

sub num_suffix
{
  local($num) = @_;

  if (--$num > 0) {
    return "$extext$num";
  }

  return "";
}

# This subroutine returns a log filename with a number appended to
# the end corresponding to how many logfiles have been created in the
# current running test.  An optional parameter may be passed (0 or 1).
# If a 1 is passed, then it does NOT increment the logfile counter
# and returns the name of the latest logfile.  If either no parameter
# is passed at all or a 0 is passed, then the logfile counter is
# incremented and the new name is returned.

sub get_logfile
{
  local($no_increment) = @_;

  $num_of_logfiles += !$no_increment;

  return ($log_filename . &num_suffix ($num_of_logfiles));
}

# This subroutine returns a base (answer) filename with a number
# appended to the end corresponding to how many logfiles (and thus
# base files) have been created in the current running test.
# NO PARAMETERS ARE PASSED TO THIS SUBROUTINE.

sub get_basefile
{
  return ($base_filename . &num_suffix ($num_of_logfiles));
}

# This subroutine returns a difference filename with a number appended
# to the end corresponding to how many logfiles (and thus diff files)
# have been created in the current running test.

sub get_difffile
{
  return ($diff_filename . &num_suffix ($num_of_logfiles));
}

# just like logfile, only a generic tmp filename for use by the test.
# they are automatically cleaned up unless -keep was used, or the test fails.
# Pass an argument of 1 to return the same filename as the previous call.

sub get_tmpfile
{
  local($no_increment) = @_;

  $num_of_tmpfiles += !$no_increment;

  return ($tmp_filename . &num_suffix ($num_of_tmpfiles));
}

1;
