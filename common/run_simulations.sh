#!/bin/bash
{  
set -e

dirbase=/home/clima-archive4/CORDEX2/EUR-11
dirout=/home/clima-archive4/CORDEX_HYDRO/REGION006/output
dirin=/home/clima-archive4/CORDEX_HYDRO/REGION006/input
while read s1 s2 s3 s4 s5 s6 s7
do

s11="$(echo -e "${s1}" | tr -d '[:space:]')"
s41="$(echo -e "${s4}" | tr -d '[:space:]')"
s51="$(echo -e "${s5}" | tr -d '[:space:]')"
s61="$(echo -e "${s6}" | tr -d '[:space:]')"
s71="$(echo -e "${s7}" | tr -d '[:space:]')"
JOB=${s71}_run

if [ -d "${dirout}/${s3}_${s1}_${s2}" ]; then
   echo "${dirout}/${s3}_${s1}_${s2} EXIST!!!"
else
   mkdir ${dirout}/${s3}_${s1}_${s2}
fi

calendar=`ncdump -h ${dirin}/${s3}_${s1}_${s2}/mrroy_2006.nc | grep calendar | grep -o -P '(?<=").*(?=")'`

sed "s/CALENDARIO/$calendar/g" <chymini.inp >chymini.inp_run
sed -i -e "s/SIMNAME/${s3}_${s1}_${s2}/g" chymini.inp_run

exit
cat <<eof> run.job
#!/bin/bash
################-----Istruzioni-----################
##                                                ##
##                                                ##
####################################################

#SBATCH -J $JOB
#SBATCH -N 1 --ntasks-per-node=12 #--mem=180G ##SKL
#SBATCH -p esp ##SKL
#SBATCH -t 1-00:00:00
#SBATCH -o ${dirout}/${s3}_${s1}_${s2}/${JOB}pbs.out
#SBATCH -e ${dirout}/${s3}_${s1}_${s2}/${JOB}pbs.err
#SBATCH --exclude=node[90,92-93]
##SBATCH --mail-type=ALL
##SBATCH --reservation=fdi_sant_12

source /opt-ictp/ESMF/environ
cd /home/clima-archive4/CORDEX_HYDRO/REGION006/input

mpirun -np 12 ./main.x chymini.inp_run

eof
sbatch run.job 
done < $1
}
