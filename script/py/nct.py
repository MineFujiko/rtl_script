import argparse
import os

from find_dir import getProjDir,getWorkDir
from rg import rg
from tb_gen import tb_gen,find_top
from work_gen import work_gen

def nct_help():
    green_begin = "\033[1;32m"
    green_end   = "\033[0m"
    help_str = """
Simulation NCT Tool, 20240224
CFG:
    gvim ~/.bashrc
CMD HELP:
{green_begin}    nct -h                   {green_end} nct help
{green_begin}    nct gen --tb demo        {green_end} gen testbench
{green_begin}    nct gen --work demo      {green_end} gen work dir
{green_begin}    nct gen --work demo -tb  {green_end} gen testbench dir
{green_begin}    nct gen --work demo -syn {green_end} gen syn
{green_begin}    nct rg                   {green_end} run simulation by rg.list
{green_begin}    nct rg -c tc_name        {green_end} run simulation by tc_name
""".format(green_begin=green_begin,green_end=green_end)
    print(help_str)

def write_sh(root_path, sim_path):
    sh_code = """
#!/bin/sh
cd {sim_path}
fe
mick vcs -lsf
""".format(sim_path=sim_path)
    
    sh_path = root_path + "/dv/script/mick.sh"
    with open(sh_path,"w") as f:
        f.write(sh_code)
    f.close()   

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", type=str, help="nct cmd",default="help",choices=["help","rg","gen"])

    # rg
    parser.add_argument("-c", type=str, help="tc_name, eg: -c tc001", nargs="+")
    # gen
    parser.add_argument("--work", help="gen the work dir, eg: --work lbus")
    parser.add_argument("--tb", help="gen the testbench dir, eg: nct gen --tb lbus")
    # parser.add_argument("--syn", help="gen the syn dir, eg: nct gen --syn lbus")
    parser.add_argument("-f", help="gen the syn dir, eg: nct gen --syn lbus -f syn_top.f")
    # parser_gen.add_argument("--flist", action="store_true", help="gen the filelist.")

    args = parser.parse_args()
    cmd = args.cmd

    root_path = getProjDir()
    # work_path = getWorkDir()
    # print("nct run.")
    print(root_path)
    # print(work_path)

    # TODO 如何区分两个subparser
    if "help" in cmd:
        nct_help()

    if "gen" in cmd:
        if args.work:
            design_name = args.work
            print(design_name)
            print("test....")
            if args.f:
                filelist = args.f
            else:
                filelist = design_name + ".f"
            work_gen(root_path, design_name, filelist)
    
        # 生成tb
        # nct gen --tb xxx
        # design_name = xxx
        if args.tb:
            design_name = args.tb
            tb_gen(root_path,design_name)

    if args.c:
        print("rg run.")
        # write_sh(root_path, work_path)
        tc_list = args.c
        rg(tc_list, root_path, work_path)
    # else:
    #     tc_list = []
