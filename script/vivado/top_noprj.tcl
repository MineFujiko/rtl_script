# run_top_batch.tcl
# bft sample design 
# A Vivado script that demonstrates a very simple RTL-to-bitstream non-project batch flow
#
# NOTE:  typical usage would be "vivado -mode tcl -source top_noprj.tcl" 
#
proc read_filelist {filelist} {
    global hdl_list
    global incdir_list
    set fp [open $filelist r]
    while {[gets $fp fname] != -1} {
        if {[regexp {^//} $fname]} {
            continue
        } elseif {[regexp {^\S+\.v} $fname]} {
            lappend hdl_list $fname
        } elseif {[regexp {^\S+\.sv} $fname]} {
            lappend hdl_list $fname
        } elseif {[regexp {^-v} $fname]} {
            regsub {^-v} $fname "" fname_sub
            lappend hdl_list $fname_sub
        } elseif {[regexp {^\+incdir\+} $fname]} {
            regsub {^\+incdir\+} $fname "" fname_sub
            lappend incdir_list $fname_sub
        }
    }
    close $fp
}

set hdl_list ""
set incdir_list ""
read_filelist "../_resource/syn_top.f"
# STEP#0: define output directory area.
#
set outputDir ./top
file mkdir $outputDir
#
# STEP#1: setup design sources and constraints
#
# read_vhdl -library bftLib [ glob ./Sources/hdl/bftLib/*.vhdl ]         
# read_vhdl ./Sources/hdl/bft.vhdl
# read_verilog  [ glob ./Sources/hdl/*.v ]
# read_xdc ./Sources/bft_full_kintex7.xdc

read_verilog $hdl_list
# read_ip "./xxx.xci"
read_xdc ./../_resource/top.xdc
#
# STEP#2: run synthesis, report utilization and timing estimates, write checkpoint design
#
synth_design -top top -part xcku3p-ffva676-3-e -mode out_of_context
write_checkpoint -force $outputDir/post_synth
report_timing_summary -file $outputDir/post_synth_timing_summary.rpt
report_power -file $outputDir/post_synth_power.rpt
#
# STEP#3: run placement and logic optimzation, report utilization and timing estimates, write checkpoint design
#
opt_design
place_design
phys_opt_design
write_checkpoint -force $outputDir/post_place
report_timing_summary -file $outputDir/post_place_timing_summary.rpt
#
# STEP#4: run router, report actual utilization and timing, write checkpoint design, run drc, write verilog and xdc out
#
route_design
write_checkpoint -force $outputDir/post_route
report_timing_summary -file $outputDir/post_route_timing_summary.rpt
report_timing -sort_by group -max_paths 100 -path_type summary -file $outputDir/post_route_timing.rpt
report_clock_utilization -file $outputDir/clock_util.rpt
report_utilization -file $outputDir/post_route_util.rpt
report_power -file $outputDir/post_route_power.rpt
report_drc -file $outputDir/post_imp_drc.rpt
write_verilog -force $outputDir/top_impl_netlist.v
write_xdc -no_fixed_only -force $outputDir/top.xdc
#
# STEP#5: generate a bitstream
# 
# write_bitstream -force $outputDir/top.bit