#!/bin/bash
{  
set -e

dirbase=/home/netapp-clima-scratch/fdi_sant/REGION
dirout=/home/clima-archive4/CORDEX_HYDRO/REGION006/input_rcp26
while read s1 s2 s3 s4 s5 s6 s7
do

s11="$(echo -e "${s1}" | tr -d '[:space:]')"
s21="$(echo -e "${s2}" | tr -d '[:space:]')"
s31="$(echo -e "${s3}" | tr -d '[:space:]')"
s41="$(echo -e "${s4}" | tr -d '[:space:]')"
s51="$(echo -e "${s5}" | tr -d '[:space:]')"
s61="$(echo -e "${s6}" | tr -d '[:space:]')"
s71="$(echo -e "${s7}" | tr -d '[:space:]')"
JOB=${s71}_i26

if [ -d "${dirout}/${s3}_${s1}_${s2}" ]; then
   echo "${dirout}/${s3}_${s1}_${s2} EXIST!!!"
else
   mkdir ${dirout}/${s3}_${s1}_${s2}
fi


cat <<eof> input.job
#!/bin/bash
################-----Istruzioni-----################
##                                                ##
##                                                ##
####################################################

#SBATCH -J $JOB
#SBATCH -N 1 --ntasks-per-node=20 #--mem=180G ##SKL
#SBATCH -p esp1 ##SKL
#SBATCH -t 1-00:00:00
#SBATCH -o ${dirout}/${s3}_${s1}_${s2}/${JOB}pbs.out
#SBATCH -e ${dirout}/${s3}_${s1}_${s2}/${JOB}pbs.err
#SBATCH --exclude=node[90,92-93]
##SBATCH --mail-type=ALL
##SBATCH --reservation=fdi_sant_12

source /opt-ictp/ESMF/environ
cd /home/clima-archive4/CORDEX_HYDRO/REGION006/input_rcp26

./scripttorun.sh $s11 $s21 $s31 $s11  > ${JOB}.out 2> ${JOB}.err

eof
sbatch input.job 
done < $1
}
