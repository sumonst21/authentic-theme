#!/usr/bin/perl

#
# Authentic Theme (https://github.com/authentic-theme/authentic-theme)
# Copyright Ilia Rostovtsev <programming@rostovtsev.io>
# Copyright Alexandr Bezenkov (https://github.com/real-gecko/filemin)
# Licensed under MIT (https://github.com/authentic-theme/authentic-theme/blob/master/LICENSE)
#
use strict;

use File::Basename;

our (%in, %text, $cwd, $path);

require(dirname(__FILE__) . '/file-manager-lib.pm');

if (!$in{'arch'}) {
    redirect('list.cgi?path=' . urlize($path) . '&module=' . $in{'module'});
}

my %errors;
my $command;
my $extension;

my @entries_list = get_entries_list();

if ($in{'method'} eq 'tar') {
    my $list = transname();
    open my $fh, ">", $list or die $!;
    print $fh "$_\n" for @entries_list;
    close $fh;
    $command   = "tar czf " . quotemeta("$cwd/$in{'arch'}.tar.gz") . " -C " . quotemeta($cwd) . " -T " . $list;
    $extension = ".tar.gz";
} elsif ($in{'method'} eq 'zip') {
    $command   = "cd " . quotemeta($cwd) . " && zip -r " . quotemeta("$cwd/$in{'arch'}.zip");
    $extension = ".zip";
    foreach my $name (@entries_list) {
        $command .= " " . quotemeta($name);

        if (!-e ($cwd . '/' . $name)) {
            $errors{ urlize(html_escape($name)) } = lc($text{'theme_xhred_global_no_target'});
        }
    }
}

system_logged($command);

redirect('list.cgi?path=' . urlize($path) . '&module=' . $in{'module'} . '&error=' . get_errors(\%errors) . extra_query());
