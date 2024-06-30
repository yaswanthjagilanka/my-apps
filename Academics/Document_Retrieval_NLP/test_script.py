import os

benchmarks = ["401.bzip2","429.mcf","456.hmmer","458.sjeng","470.lbm"]


out_options = ["/util/gem5/benchmark/401.bzip2/data/input.program", "/util/gem5/benchmark/429.mcf/data/inp.in",
               "/util/gem5/benchmark/456.hmmer/data/bombesin.hmm.new","/util/gem5/benchmark/458.sjeng/data/test.txt",
             "/util/gem5/benchmark/470.lbm/data/100_100_130_cf_a.of"]

param_dict = {"l1d_sizes" : ["8kB","16kB","32kB","64kB","128kB"],
"l1i_sizes" : ["8kB","16kB","32kB","64kB","128kB"],
"l2_sizes" : ["128kB","256kB","512kB","1MB","2MB"],
"l1dassoc_sizes" : ["1","2","4","8","16"],
"l1i_assoc" : ["1","2","4","8","16"],
"l2_assoc" : ["1","2","4","8","16"]}




def command_return(benchmark_path,data_path,output_dir,l1d="256",l1i="256",l2_s="4",l1d_a="4",l1i_a="4",l2_a="4"):
    command = "time /util/gem5/build/X86/gem5.opt -d "
    command+=output_dir
    command+=" /util/gem5/configs/example/se.py -c "
    command+=benchmark_path
    command+=" -o "
    command+=data_path
    command+=" -I 100000000 "
    command+="--caches --l2cache --l1d_size="
    command+=l1d+"kB --l1i_size="
    command+=l1i+"kB --l2_size="
    command+=l2_s+"MB --l1d_assoc="
    command+=l1d_a+" --l1i_assoc="
    command+=l1i_a+" --l2_assoc="
    command+=l2_a
    return command


path = "/home/csgrad/chitrava/CSE_590_Project2/"
if not os.path.exists(path):
    os.makedirs(path)

for i,x in enumerate(benchmarks):
    print("running for ",x)
    if not os.path.exists(path+x):
        os.makedirs(path+x)
    benchmark_path = "/util/gem5/benchmark/"+x+"/src/benchmark"
    data_path = out_options[i]
    path1 = path+x+"/"
    if not os.path.exists(path1):
        os.makedirs(path1)
    for k in param_dict.keys():
        path2 = path1+k+"/"
        if not os.path.exists(path2):
            os.makedirs(path2)
        for v in param_dict.get(k):
            path3 = path2+"size_"+v+"/"
            if not os.path.exists(path3):
                os.makedirs(path3)
            output_dir = path3
            if k=="l1d_sizes":
                command = command_return(benchmark_path,data_path,output_dir,l1d=v)
                os.system(command)
            elif k=="l1i_sizes":
                command = command_return(benchmark_path,data_path,output_dir,l1i=v)
                os.system(command)
            elif k=="l2_sizes":
                command = command_return(benchmark_path,data_path,output_dir,l2_s=v)
                os.system(command)
            elif k=="l1dassoc_sizes":
                command = command_return(benchmark_path,data_path,output_dir,l1d_a=v)
                os.system(command)
            elif k=="l1i_assoc":
                command = command_return(benchmark_path,data_path,output_dir,l1i_a=v)
                os.system(command)
            else:
                command = command_return(benchmark_path,data_path,output_dir,l2_a=v)
                os.system(command)