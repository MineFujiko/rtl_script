import os
from pathlib import Path
from lib.v_syn_gen import writeSyntop

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

def syn_top_gen(root_path, design_name):
    # 1. 获取当前目录
    curr_path = os.getcwd()
    input_file = curr_path + "/" + design_name

    # 2. 生成syn_top
    syn_code = writeSyntop(input_file)
    
    # 3. 生成文件
    new_top_name = design_name.split(".")[0] + "_syn.sv"
    syn_top_path = "{curr_path}/{new_top_name}".format(curr_path=curr_path,new_top_name=new_top_name)
    with open(syn_top_path, "w") as f:
        f.write(syn_code)
    f.close()

def syn_gen(root_path, design_name="syn_top"):
    syn_top_gen(root_path, design_name)