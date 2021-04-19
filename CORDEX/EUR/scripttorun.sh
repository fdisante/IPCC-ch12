#!/bin/bash 
dirbase=/home/netapp-clima-scratch/fdi_sant/REGION
dirout=/home/clima-archive4/CORDEX_HYDRO/REGION006/input
  inpdir=${dirbase}
  inpdir=${dirbase}
  for yearbase in {2006..2100..5}
    do
    for i in {0..4}
      do
        year=$(($yearbase+$i))
        yearmax=$(($yearbase+4))
        if [ $3 == "ICTP-RegCM4-7" ]; then
          echo ${inpdir}
          list=$(eval echo ${inpdir}/mrro*${1}*${3}*day_$year*)
          cdo -L -z zip selyear,${year} -cat ${inpdir}/mrro_*${1}_rcp26*${3}*day_$year* \
              ${dirout}/${3}_${1}_${2}/mrro_${year}.nc
        else
          list=$(eval echo ${inpdir}/mrro_*${1}*${3}*day_$yearbase*)
          cdo -L -z zip selyear,${year} ${inpdir}/mrro_*${1}_rcp26*${3}*day_$yearbase* \
             ${dirout}/${3}_${1}_${2}/mrro_${year}.nc
        fi
        cdo -z zip -P 20 remapdis,grid.AFRICA006 ${dirout}/${3}_${1}_${2}/mrro_${year}.nc \
           ${dirout}/${3}_${1}_${2}/mrroy_${year}.nc
        rm ${dirout}/${3}_${1}_${2}/mrro_${year}.nc
    done
  done
