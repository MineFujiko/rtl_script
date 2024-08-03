import os
from pathlib import Path

def flist_ex(root_path,flist_path):
    '''filelsit expand'''
    with open(flist_path,"r") as f:
        fl_txt = f.readlines()
    f.close()

    # TODO define except
    flist = ""
    for i in fl_txt:
        if "incdir" in i:
            file_path = i
        else:
            file_path = "{root_path}/{file}".format(root_path=root_path, file=i)
        flist += file_path
    return flist

def src_flist_gen(flist_name,root_path,design_name):
    # filelist from /release/design_name/design_name.f
    flist_path = "{0}/release/{1}/{2}".format(root_path, design_name, flist_name)
    if Path(flist_path).exists():
        flist = flist_ex(root_path,flist_path)

        src_flist = "{0}/work/{1}/_resource/{2}".format(root_path,design_name,flist_name)
        with open(src_flist,"w") as f:
            f.write(flist)
        f.close()
    else:
        print("[NCT-Warning]: {0} is not exist!".format(flist_path))

def cp_xdc(root_path,design_name):
    src_path = "{0}/release/{1}/top.xdc".format(root_path,design_name)
    dst_path = "{0}/work/{1}/_resource".format(root_path,design_name)
    if Path(src_path).exists():
        cp_cmd = "cp {src_path} {dst_path}".format(src_path=src_path,dst_path=dst_path)
        os.system(cp_cmd)
    else:
        print("[NCT-Warning]: {0} is not exist!".format(src_path))


def src_gen(root_path, design_name, filelist):
    # mkdir _resource
    src_path = "{0}/work/{1}/_resource".format(root_path,design_name)
    if not Path(src_path).exists():
        Path(src_path).mkdir()
    
    top_name = design_name+".f"
    src_flist_gen(top_name,root_path,design_name)
    src_flist_gen("tb_top.f",root_path,design_name)
    src_flist_gen("syn_top.f",root_path,design_name)

    # cp xdc 
    cp_xdc(root_path,design_name)


def vcs_gen(root_path, design_name, curr_path):
    # mkdir vcs
    # mkdir vcs/00_script
    # mkdir vcs/work
    vcs_path = "{0}/vcs".format(curr_path)
    if not Path(vcs_path).exists():
        Path(vcs_path).mkdir()
    
    work_path = "{0}/vcs/work".format(curr_path)
    if not Path(work_path).exists():
        Path(work_path).mkdir()
    
    sci_path = "{0}/vcs/00_script".format(curr_path)
    if not Path(sci_path).exists():
        Path(sci_path).mkdir()
    
    # gen env.sh
    env_sh_tmp = "{path}/script/vcs/env.sh.tmp".format(path=root_path)
    with open(env_sh_tmp, "r") as f:
        env_txt = f.read()
    f.close()
    filelist = "{path}/_resource/tb_top.f".format(path=curr_path)
    env_txt = env_txt.format(filelist=filelist)

    env_path = "{path}/vcs/00_script/env.sh".format(path=curr_path)
    with open(env_path,"w") as f:
        f.write(env_txt)
    f.close()

    # gen vcs_compile.sh from script/vcs/vcs_compile.sh
    vcs_src_path = "{path}/script/vcs/vcs_compile.sh".format(path=root_path)
    with open(vcs_src_path, "r") as f:
        vcs_txt = f.read()
    f.close()
    vcs_dst_path = "{path}/vcs/00_script/vcs_compile.sh".format(path=curr_path)
    with open(vcs_dst_path,"w") as f:
        f.write(vcs_txt)
    f.close()

    # gen makefile from script/vcs/makefile
    mf_src_path = "{path}/script/vcs/makefile".format(path=root_path)
    with open(mf_src_path, "r") as f:
        mf_txt = f.read()
    f.close()
    mf_dst_path = "{path}/vcs/work/makefile".format(path=curr_path)
    with open(mf_dst_path,"w") as f:
        f.write(mf_txt)
    f.close()

    # gen vcs_run.sh from script/vcs/vcs_run.sh
    vcs_run_sh_tmp = "{path}/script/vcs/vcs_run.sh.tmp".format(path=root_path)
    with open(vcs_run_sh_tmp, "r") as f:
        vcs_run_txt = f.read()
    f.close()
    vcs_work_path = "{path}/vcs/work".format(path=curr_path)
    vcs_run_txt = vcs_run_txt.format(path=vcs_work_path)

    vcs_run_path = "{path}/vcs/work/vcs_run.sh".format(path=curr_path)
    with open(vcs_run_path,"w") as f:
        f.write(vcs_run_txt)
    f.close()

def vivado_gen(root_path, design_name):
    src_path = root_path + "/script/vivado"
    dst_path = root_path + "/work/" + design_name
    cp_cmd = "cp {src_path} {dst_path} -R".format(src_path=src_path,dst_path=dst_path)
    os.system(cp_cmd)

def questa_gen(root_path, design_name):
    src_path = root_path + "/script/questa"
    dst_path = root_path + "/work/" + design_name
    cp_cmd = "cp {src_path} {dst_path} -R".format(src_path=src_path,dst_path=dst_path)
    os.system(cp_cmd)

def work_path_gen(root_path, design_name):
    work_path = "{root_path}/work/{design_name}".format(root_path=root_path,design_name=design_name)
    if not Path(work_path).exists():
        Path(work_path).mkdir()
    return work_path

def work_gen(root_path, design_name, filelist):
    # TODO FILE CHECK
    curr_path = work_path_gen(root_path, design_name)
    print(curr_path)

    src_gen(root_path, design_name, filelist)

    vcs_gen(root_path, design_name, curr_path)

    vivado_gen(root_path, design_name)

    questa_gen(root_path, design_name)