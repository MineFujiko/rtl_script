import os
from pathlib import Path
from lib.v_tb_gen import writeTestBench, writeSB

def find_top(root_path,design_name):
    top_flist_path = "{root_path}/release/{design_name}/{design_name}.f".format(root_path=root_path,design_name=design_name)
    if os.path.exists(top_flist_path):
        with open(top_flist_path, "r") as f:
            top_flist = f.readlines()
        f.close()
        top_path = top_flist[-1].strip() # TODO 默认最后一个为top文件
        top_path = root_path + "/" + top_path
    else:
        print("Error: there is no %s" % top_flist_path)
    
    return top_path

def tb_top_gen(root_path, design_name):
    # 1. 找到top
    input_file = find_top(root_path,design_name)
    # 2. 生成目录
    # tb_path = "root_path/dv/demo"
    tb_path = "{0}/dv/{1}".format(root_path,design_name)
    if not Path(tb_path).exists():
        Path(tb_path).mkdir()
    # 2. 生成tb_top
    tb_code = writeTestBench(input_file,root_path)
    tb_top_path = "{root_path}/dv/{design_name}/tb_top.sv".format(root_path=root_path,design_name=design_name)
    with open(tb_top_path, "w") as f:
        f.write(tb_code)
    f.close()
    # 3. 生成tc模板

def sb_gen(root_path, design_name):
    # 1. 生成目录
    # 2. 生成tb_top
    # 3. 生成tc模板
    input_file = find_top(root_path,design_name)
    sb_code = writeSB(input_file)
    sb_path = "{root_path}/dv/{design_name}/scoreboard.sv".format(root_path=root_path,design_name=design_name)
    with open(sb_path, "w") as f:
        f.write(sb_code)
    f.close()

def tb_gen(root_path, design_name="syn_top"):
    tb_top_gen(root_path, design_name)
    # TODO sb_gen(root_path, design_name)