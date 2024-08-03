#!/bin/sh

source ../00_script/env.sh

mkdir worklib

# if [ -f $vhdllist];then
# vhdlan -f $vhdllist \
#        -full64 \   
#        +error+100 \
#        -l $vhdl_log \
#        -kdb
# else
#     echo "only vlogan compile"
# fi

vlogan -sverilog \
    -full64 \
    -assert svaext \
    -assert enable_diag \
    -debug_access+pp \
    -timescale=1ns/1ps \
    +error+100 \
    +define+$defines \
    -f $filelist \
    -l vlog.log \
    -kdb

vcs -cpp g++-4.8 -cc gcc-4.8 -LDFLAGS -Wl,--no-as-needed \
    -lca \
    -sverilog $extopt \
    -top $topname \
    -P /disk/Synopsys/verdi-2018.9/verdi/Verdi_O-2018.09-SP2/share/PLI/VCS/LINUXAMD64/novas.tab /disk/Synopsys/verdi-2018.9/verdi/Verdi_O-2018.09-SP2/share/PLI/VCS/LINUXAMD64/pli.a \
    +lint=TFIPC-L \
    -full64 \
    -diag timescale \
    +notimingcheck \
    +error+100 \
    -kdb \
    -l vcs.log \
    -R
