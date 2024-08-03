Windows：
```
cd ~
touch .bash_profile
gvim .bash_profile
alias nct="python D:/script/py/nct.py"
alias src="source ~/.bash_profile"
```

CMD HELP:
```
nct rg            run simulation by rg.list
nct rg -c tc_name run simulation by tc_name
nct gen --work    gen work dir
nct gen --tb      gen testbench
nct gen --syn     gen syn
```

# 1. 使用说明
## 1.1 工程目录结构
```
    - release
        - demo
            demo_top.f
            demo_top.fpga.xdc
            demo_top.sdc
            tb_top.f
    - script
    - src
    - work
        - demo
```

## 1.2 Feature
    - 生成work目录
        - 支持vivado工程生成
        - 支持questasim工程生成
        - 支持vcs工程生成

1. release目录文件
    - demo
        - demo.f
        - demo.fpga.xdc
        - demo.sdc
        - param.json
        - *lint
            - lint.param.json
        - *dc
            - dc.param.json
        - etc.
2. nct gen --tb demo
    会在dv目录下，生成目录：
    - demo
        - testbench
            - Driver.sv
            - DriverBse.sv
            - Enviroment.sv
            - Generator.sv
            - Packet.sv
            - Receiver.sv
            - ReceiverBase.sv
            - io.sv
            - global_pkg.sv
            - Makefile
        - tb_top.sv
        - tb_top.f
3. 生成work目录
    - nct gen --work demo       : 以demo.sv为顶层生成
    - nct gen --work demo --tb  : 以demo.sv对应的testbench为顶层生成
    - nct gen --work demo --syn : 以demo.sv生成特定综合顶层
4. 回归测试
    nct rg
    nct rg -c tc_name

版本说明：
    20240427 v0.1.1
        1. 新增：支持syn_top生成;
    20240224 v0.1
        1. 新增：增加帮助文档;
    20230526 v0.0
        初始版本