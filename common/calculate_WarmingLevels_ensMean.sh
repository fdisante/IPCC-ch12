#!/bin/bash
module load R/3.5.1

debug=
#debug=echo

#for region in AFR AUS  CAM  EAS  NAM  SAM  SEA  WAS ; do
for region in AFR NAM ; do

#Read reg from region
#reg=${region%006*}

for file in `ls ../../${region}006/output_rcp{26,85}/*/compressed/run_2006010100.nc` ; do
#for file in `ls ../../AUS006/output_rcp26/*/run_2006010100.nc` ; do

while read S1 S2 S3 S4 S5 S6 ;do
#Read simulation name from file path
v1=${file%/compressed*}
sim=${v1##*/}

#Read period from file path
v1=${file##*output_}
per=${v1%%/*}

#Read GCM from file path
v1=${file##*$per/}
v2=${v1%%/*}
v3=${v2#*_}
gcm=${v3%_*}



#echo $gcm

if [ "$S2" = "r1i1p1" ] ; then
if [[ $gcm == *"$S1"* ]]; then
if [ "$S4" = "1.5" ] || [ "$S4" = "2.0" ] || [ "$S4" = "3.0" ] || [ "$S4" = "4.0" ]; then
if [ "$S3" = "$per" ] ; then
echo $file
echo $region $S1 $S2 $S3 $S4 $S5 $S6
echo $gcm
#$debug /opt-ictp/ESMF/201906/bin/cdo -L -z zip selyear,$S5/$S6 -cat ../../${region}006/output_his/${sim}/run_??????????_qmax.nc ../../${region}006/output_${S3}/${sim}/run_??????????_qmax.nc ${region}/${sim}_${S2}_${S3}_${S4}_${S5}-${S6}.nc
#$debug ./create_Qx_regcm.R --var="qmax" ${region}/${sim}_${S2}_${S3}_${S4}_${S5}-${S6}.nc
$debug /opt-ictp/ESMF/201906/bin/cdo -L -z zip sellevel,100 -selvar,QRP ${region}/${sim}_${S2}_${S3}_${S4}_${S5}-${S6}.nc ${region}/${sim}_${S2}_${S3}_${S4}_${S5}-${S6}_Q100.nc
#$debug cdo -L -z zip ../../${region}006/output_rcp26/run_2098000100_qmax.nc 
#$debug cdo -L -z zip ../../${region}006/output_rcp85/run_2098000100_qmax.nc 

fi
fi
fi
fi
done < cmip5_warming_levels_all_ens_1850_1900_noHEAD.csv 
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
