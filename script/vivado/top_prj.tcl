# run_bft_kintex7_project.tcl
# BFT sample design 
#    A Vivado script that demonstrates an RTL-to-bitstream project flow.
#    This script will create a project, copy sources into the project 
#    directory, run synthesis, implementation and generate a bitstream.
#    It will also write a few reports to disk and open the GUI when finished.
#
# NOTE:  -Typical usage would be "vivado -mode tcl -source run_bft_kintex7_project.tcl" 
#        -To use -mode batch comment out the "start_gui" and "open_run impl_1" to save time
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
# put $hdl_list

#
create_project top ./top -part xcku3p-ffva676-3-e

# add_files ../_resource/syn_top.f
# add_files F:/Workspace/IC/RTL_LIB/design/component/multiplexer/mux1/mux1.sv
# add_files F:/Workspace/IC/RTL_LIB/dv/mux1/syn_top.sv
add_files $hdl_list

# add_files -fileset sim_1 ./Sources/hdl/bft_tb.v
# add_files ./Sources/hdl/bftLib
# set_property library bftLib [get_files  {./Sources/hdl/bftLib/round_4.vhdl ./Sources/hdl/bftLib/round_3.vhdl ./Sources/hdl/bftLib/round_2.vhdl ./Sources/hdl/bftLib/round_1.vhdl ./Sources/hdl/bftLib/core_transform.vhdl ./Sources/hdl/bftLib/bft_package.vhdl}]
import_files -force
import_files -fileset constrs_1 -force -norecurse ./../_resource/top.xdc
# Mimic GUI behavior of automatically setting top and file compile order
update_compile_order -fileset sources_1
# update_compile_order -fileset sim_1
set_property -name {STEPS.SYNTH_DESIGN.ARGS.MORE OPTIONS} -value {-mode out_of_context} -objects [get_runs synth_1]

# Launch Synthesis
launch_runs synth_1
wait_on_run synth_1
open_run synth_1 -name netlist_1
# Generate a timing and power reports and write to disk
report_timing_summary -delay_type max -report_unconstrained -check_timing_verbose -max_paths 10 -input_pins -file ./top/syn_timing.rpt
report_power -file ./top/syn_power.rpt
# Launch Implementation
launch_runs impl_1 -to_step route_design
wait_on_run impl_1 
# Generate a timing and power reports and write to disk
# comment out the open_run for batch mode
open_run impl_1
report_timing_summary -delay_type min_max -report_unconstrained -check_timing_verbose -max_paths 10 -input_pins -file ./top/imp_timing.rpt
report_power -file ./top/imp_power.rpt
# comment out the for batch mode
start_gui
