import os
import re

proj_root_tag = ".proj.config"
work_root_tag  = "_resource"

def path_re(path):
    return re.sub(r'\\','/',path)

def findProjRoot(path, start_path, tag):
    # if (not path.startswith("/")):
    #     raise("%s is not valid abs-path, check Please" % path)

    dest = os.path.join(path, tag)

    if(path=="/"):
        return None
    elif os.path.exists(dest):
        print("found valid project dir '%s'" % path)
        return path
    else:
        return findProjRoot(os.path.dirname(path),start_path,tag)

def getProjDir():
    cwd = os.getcwd()
    proj_dir = findProjRoot(cwd, cwd, tag=proj_root_tag)
    proj_dir = path_re(proj_dir)
    return proj_dir

def getWorkDir():
    cwd = os.getcwd()
    work_dir = findProjRoot(cwd, cwd, tag=work_root_tag)
    work_dir = path_re(work_dir)
    return work_dir