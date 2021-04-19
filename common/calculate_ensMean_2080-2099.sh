#!/bin/bash
module load R/3.5.1

debug=
#debug=echo

S5=2080
S6=2099

for region in AUS AFR CAM EAS NAM SAM SEA WAS ; do

for file in `ls ../../${region}006/output_rcp{26,85}/*/run_2006000100_qmax.nc` ; do

#Read simulation name from file path
v1=${file%/*}
sim=${v1##*/}

#Read period from file path
v1=${file##*output_}
per=${v1%%/*}

#Read GCM from file path
v1=${file##*$per/}
v2=${v1%%/*}
v3=${v2#*_}
gcm=${v3%_*}



$debug /opt-ictp/ESMF/201906/bin/cdo -L -z zip selyear,$S5/$S6 -cat ../../${region}006/output_his/${sim}/run_??????????_qmax.nc ../../${region}006/output_${per}/${sim}/run_??????????_qmax.nc ${region}/${sim}_${per}_${S5}-${S6}.nc
$debug ./create_Qx_regcm.R --var="qmax" ${region}/${sim}_${per}_${S5}-${S6}.nc
$debug /opt-ictp/ESMF/201906/bin/cdo -L -z zip sellevel,100 -selvar,QRP ${region}/${sim}_${per}_${S5}-${S6}.nc ${region}/${sim}_${per}_${S5}-${S6}_Q100.nc

done
done



#Small Example

#    |
#    |
#    V


#  var=GERICS-REMO2015_MOHC-HadGEM2-ES_r1
#  ens=${var##*_}
#  var=${var#*_}
#  gcm=${var%%_*}
#  echo $var
#  echo $gcm
#  echo $ens
