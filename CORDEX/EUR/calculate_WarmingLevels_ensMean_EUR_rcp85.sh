#!/bin/bash
module load R/3.5.1

debug=
#debug=echo

diri=/home/clima-archive4/CORDEX_HYDRO/EUROPE006
for region in EUR ; do
#for region in AUS ; do

#Read reg from region
#reg=${region%006*}

for file in `ls ${diri}/output/*/run_2007010100.nc` ; do

while read S1 S2 S3 S4 S5 S6 ;do
#Read simulation name from file path
v1=${file%/*}
sim=${v1##*/}

#Read ensemble from file path
ens=${sim##*_}
if [ "$ens" = "r1" ] ; then ens=r1i1p1 ; fi
if [ "$ens" = "r2" ] ; then ens=r2i1p1 ; fi
if [ "$ens" = "r3" ] ; then ens=r3i1p1 ; fi
if [ "$ens" = "r4" ] ; then ens=r4i1p1 ; fi
if [ "$ens" = "r5" ] ; then ens=r5i1p1 ; fi
if [ "$ens" = "r12" ] ; then ens=r12i1p1 ; fi

#Read period from file path
per=rcp85

#Read GCM from file path
v1=${file#*output/}
v2=${v1%%/*}
v3=${v2#*_}
gcm=${v3%_*}

if [ "$S2" = "$ens" ] ; then
if [[ $gcm == *"$S1"* ]]; then
if [ "$S4" = "1.5" ] || [ "$S4" = "2.0" ] || [ "$S4" = "3.0" ] || [ "$S4" = "4.0" ]; then
if [ "$S3" = "$per" ] ; then
echo $file
echo $region $S1 $S2 $S3 $S4 $S5 $S6
echo $gcm
$debug /opt-ictp/ESMF/201906/bin/cdo -L -z zip selyear,$S5/$S6 -cat ${diri}/output/${sim}/run_{1976..2099}??????_qmax.nc ${region}/${sim}_${S2}_${S3}_${S4}_${S5}-${S6}.nc
$debug ./create_Qx_regcm.R --var="qmax" ${region}/${sim}_${S2}_${S3}_${S4}_${S5}-${S6}.nc
$debug /opt-ictp/ESMF/201906/bin/cdo -L -z zip sellevel,100 -selvar,QRP ${region}/${sim}_${S2}_${S3}_${S4}_${S5}-${S6}.nc ${region}/${sim}_${S2}_${S3}_${S4}_${S5}-${S6}_Q100.nc
#$debug cdo -L -z zip ../../${region}006/output_rcp85/run_2098000100_qmax.nc 
#$debug cdo -L -z zip ../../${region}006/output_rcp85/run_2098000100_qmax.nc 

fi
fi
fi
fi
done < cmip5_warming_levels_all_ens_1850_1900_noHEAD.csv 
done
done
