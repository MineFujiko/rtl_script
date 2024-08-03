.PHONY: clean

vcs:
	sh ../00_script/vcs_compile.sh

verdi:
	verdi -f ../../_resource/tb_top.f -ssf tb_top.fsdb

clean:
	rm -f *.log
	rm -rf 64
	rm -rf AN.DB
	rm -rf simv.daidir
	rm -rf work.lib++
	rm -rf worklib
	rm -rf csrc
	rm -rf *.fsdb
	rm -rf simv
	rm -rf *.key
	rm -rf *.h