import time
import os

def rm_case(tc_list):
    print(tc_list)
    new_test = []
    for i in tc_list:
        if "//" in i:
            pass
        elif i == "":
            pass
        else:
            new_test.append(i)
    
    return new_test

def tc_gen(root_path, tc_name, design_name):
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    tc_dut_code = r"""
// generate by python3
// {time_str}

`include "{tc_name}.sv"

string tc_name="{tc_name}";

task tc_dut;
    tc_send(tc_name);
endtask

""".format(time_str=time_str, tc_name=tc_name)

    tc_file = "{root_path}/dv/{design_name}/testcase/tc_dut.sv".format(root_path=root_path, design_name=design_name)

    with open(tc_file,"w") as f:
        f.write(tc_dut_code)
    f.close()   

def tc_run(work_path):
    tc_run_cmd = "/bin/sh {path}/vcs/work/vcs_run.sh".format(path=work_path)
    os.system(tc_run_cmd)

def tc_rm(work_path):
    pass_path = "{path}/vcs/work/tc.pass".format(path=work_path)
    if os.path.exists(pass_path):
        rm_cmd = "rm {path}/vcs/work/tc.pass".format(path=work_path)
        print(rm_cmd)
        os.system(rm_cmd)

def tc_result_check(rg_result_path, work_path, tc_name):
    pass_file = "{path}/vcs/work/tc.pass".format(path=work_path)
    pass_flag = 0
    if os.path.isfile(pass_file):
        pass_flag = 1

    with open(rg_result_path, "a") as f:
        if pass_flag:
            f.write("\033[1;32mpass\033[0m: " + tc_name +"\n")
        else:
            f.write("\033[1;32mfail\033[0m: " + tc_name +"\n")
    f.close()

def get_design_name(work_path):
    return work_path.split("/")[-1]

def rg(tc_list, root_path, work_path):
    design_name = get_design_name(work_path)
    print(design_name)

    if tc_list == None:
        rg_list_file = "{root_path}/dv/{design_name}/regress_list.txt".format(root_path=root_path,design_name=design_name)
        if os.path.exists(rg_list_file):
            with open(rg_list_file, "r") as f:
                tc_list = f.readlines()
            f.close()
        else:
            print("Warning: there is no {file}".format(file=rg_list_file))
            tc_list = ["tc001"] # TODO
    
    tc_list = rm_case(tc_list)

    # rg_result_path = work_path + "/regress_result.txt"
    rg_result_path = "{root_path}/dv/{design_name}/regress_result.txt".format(root_path=root_path,design_name=design_name)
    rm_result_cmd  = "rm {path}".format(path=rg_result_path)
    if os.path.exists(rg_result_path):
        os.system(rm_result_cmd)
        print(rm_result_cmd)
    
    for i in tc_list:
        tc_name = i.strip()
        tc_gen(root_path, tc_name, design_name)
        tc_rm(work_path)
        tc_run(work_path)
        tc_result_check(rg_result_path, work_path, tc_name)
    
    if os.path.exists(rg_result_path):
        cat_result_cmd = "cat {path}".format(path=rg_result_path)
        os.system("echo '--------------------------------------'")
        os.system(cat_result_cmd)
    else:
        print("Warning: there is no {file}".format(file=rg_result_path))
    print("RG DONE.")

if __name__=="__main__":
    tc_list = []
    rg(tc_list)