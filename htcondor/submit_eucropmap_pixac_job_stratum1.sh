universe       = docker
docker_image   = jeoreg.cidsn.jrc.it:5000/jeodpp-htcondor/d5-eucropmap_py3:1.1 
executable     = ./start_process_pixac.sh 
transfer_input_files = /eos/jeodpp/home/users/verheas/pixac/htcondor/start_process_pixac.sh,/eos/jeodpp/home/users/verheas/pixac/run_eucropmap_htc.py
arguments      = /eos/jeodpp/home/users/verheas/pixac/htcondor/list_rasters_eu_stratum_all1_all.lst $(ClusterID) $(ProcId) /eos/jeodpp/data/projects/REFOCUS/data/S1_GS/pixac_v7_stratum_1/ /eos/jeodpp/data/projects/REFOCUS/data/S1_GS/S1_classif_v7_stratum_1/ /eos/jeodpp/home/users/verheas/pixac/ 1


should_transfer_files   = YES
when_to_transfer_output = ON_EXIT
#job_machine_attrs = Machine  
#job_machine_attrs_history_length = 5           
#requirements = target.machine =!= MachineAttrMachine1 && target.machine =!= MachineAttrMachine2

request_memory = 200GB
request_cpus   = 10
output         = /eos/jeodpp/htcondor/processing_logs/REFOCUS/cropclassif.$(ClusterId).$(ProcId).out 
error          = /eos/jeodpp/htcondor/processing_logs/REFOCUS/cropclassif.$(ClusterId).$(ProcId).err 
log            = /eos/jeodpp/htcondor/processing_logs/REFOCUS/cropclassif.$(ClusterId).$(ProcId).log
batch_name = "EUcropmap_str1_pixac"
queue infile from /eos/jeodpp/data/projects/REFOCUS/cropclassif/v7/list_rasters_eu_stratum_all1_all.lst

