#!/usr/bin/env Rscript
# Jan 2019
#afantini@ictp.it
# Script to calculate peak Q(RP) discharge fitting a gumbel distribution from RegCM model files
.libPaths( c( "/home/netapp-clima/users/fdi_sant/LIBRARY/R_Library", .libPaths()) )
library(pacman)
p_load(optparse)

option_list = list(
                    make_option("--var",
                                type="character",
                                default='mrro',
                                help="Variable to use from input file [default: %default]"),
                    make_option("--returnperiod",
                                type="character",
                                default='2,5,10,25,50,100,200,250,500',
                                help="Comma separated list of return periods to calculate, in years [default: %default]"),
                    make_option("--conversion",
                                type="double",
                                default=1,
                                help="Multiplicative conversion factor from the input unit to the output units [default: %default]"),
                    make_option("--ounit",
                                type="character",
                                default='m3 s-1',
                                help="Output units [default: %default]"),
                    make_option("--minq",
                                type="double",
                                default=0,
                                help="Minimum values for discharge, lower values will become NA [default: %default]"),
                    make_option(c("-n", "--nthreads"),
                                type="integer",
                                default=NA,
                                help="Number of threads to be used, NA for automatic detection [default: %default]")
)
parser = OptionParser(
    usage = "%prog [options] INPUT",
    option_list=option_list,
    epilogue=paste0("This script calculates the peak Q(RP) for a given RP and variable in a NetCDF file. Does everything in memory, so make sure your dataset fits in memory! INPUT must be the output of a CDO yearmax process (or equivalent). No checks are performed, make sure you know what you are doing. Assumes lat-lon files. A new variable will be created in the input file, containing the Q(RP) data. For feature requests and bug reports, please write to:
    afantini@ictp.it")
)

arguments = parse_args(parser, positional_arguments = 1) #, args = 'data/monthlymax/mergetime/yearmax.nc')
opt = arguments$options

suppressPackageStartupMessages(p_load(futile.logger))

flog.debug("Parsed input arguments")

input_file = arguments$args[1]
flog.info("Input file: %s", input_file)


nthreads = opt$nthreads
input_var = opt$var
conversion_factor = opt$conversion
output_unit = opt$ounit
minQ = opt$minq
overwrite = isTRUE(opt$overwrite)

RPs = as.numeric(unlist(strsplit(opt$returnperiod, ',')))

#==================== PROGRAM STARTS ====================


emgamma = 0.5772     # Euler-Mascheroni constant

flog.info('USING DATA FROM FILE %s , VARIABLE : %s', input_file, input_var)
flog.info('VALUES LOWER THAN  %d WILL BE SET TO NA', minQ)

flog.info('LOADING PACKAGES')
p_load(
FAdist,       # Provides the Gumbel distribution
fitdistrplus, # To do distribution fits
purrr,        # for furrr
furrr,        # Multicore execution
ncdf4,        # Netcdf file handling
magrittr      # provides %>%
)
source('/home/netapp-clima-users1/afantini/R/functions/netcdfTimes.R')

flog.info('OPENING INPUT FILE')
nc = nc_open(input_file, write=TRUE)

flog.info('READING DATA')
discharges = nc %>% ncvar_get(input_var) * conversion_factor # Read ALL into RAM


#====================== GENERATE PEAKS FILE ======================

#Create an NC file which contains all the peak discharges
#Define dimensions
dims = sapply(nc$var[[input_var]]$dim, function(x) x$name)

nc_input_var = nc$var[[input_var]]
output_var = paste0('QRP')
RP_dim = ncdim_def('RP', 'years', RPs, longname = 'Return Period')
qRP = ncvar_def(name = output_var, units = output_unit, dim=c(nc$dim[dims[-which(dims=='time')]], list(RP_dim)), missval = nc_input_var$missval, longname = 'Peak discharge')

nc = ncvar_add(nc, qRP)

#nc %>% ncatt_put(output_var,  "coordinates", ncatt_get(nc, input_var, 'coordinates')$value)
#nc %>% ncatt_put(output_var,  "grid_mapping", ncatt_get(nc, input_var, 'grid_mapping')$value)

crDate <- format(Sys.time(), format="%F %T %Z")
nc %>% ncatt_put(0, "history", paste0(crDate, " : created by create_Qx_regcm.R ; ", (nc %>% ncatt_get(0, 'history'))$value))
nc %>% ncatt_put(0, "R_version", version$version.string)
nc %>% ncatt_put(0, "ncdf4_version", as.character(packageVersion("ncdf4")))
nc_sync(nc)
# nc_close(nc)


#====================== FUNCTIONS ======================


compute_one = function(n) { #Function to compute one cell
    i = ij[n,1]
    j = ij[n,2]
    v = discharges[i, j, ] #%>%
    #as_units(var_units) %>%
#     set_units('m3 s-1') %>%
    #as.numeric  #convert discharge to m3/s
    v[v<=minQ] = NA

    if (sum(!is.na(v)) <= 10) { #less than 10 years avail
       return(rep(NA, length(RPs)))
    }

    #Set initial parameters for the fit
    gscale <- sd(v, na.rm=TRUE) * sqrt(6) / pi          #Alpha
    glocation <- mean(v, na.rm=TRUE) - emgamma * gscale #Mu
    capture.output(fit <- tryCatch(
        fitdist(as.vector(na.omit(v)), #default options: MLE estimation
            'gumbel',
            start = list(location = glocation, scale = gscale)
        ),
        error = function(e) return(list(estimate = c(NA, NA)))
    )) %>%  invisible
    fitmu <- fit$estimate[1]
    fitalpha <- fit$estimate[2]

    loc = as.numeric(fitmu)
    sca = as.numeric(fitalpha)

    if (is.na(loc) || is.na(sca)) return(rep(NA, length(RPs)))

    fpeaks = function(rp) { # This is Q0(RP)
        loc - sca *log(-log(1-1/rp))
    }
#     map(RPs, fpeaks) %>% unlist
    fpeaks(RPs)
}


#====================== COMPUTE ======================


if (isTRUE(debug)) {
    flog.debug('USING TRANSPARENT SINGLE PROCESS PLAN FOR DEBUGGING')
    plan(transparent)
} else {
    if (is.na(nthreads)) nthreads = availableCores()
    flog.info('USING %i CORES', nthreads)
    plan(multiprocess)
}
options(future.globals.maxSize = object.size(discharges)*1000 )
flog.info('COMPUTING')
ij = expand.grid(1:nrow(discharges), 1:ncol(discharges))
peak_discharges = future_map(seq_len(nrow(ij)), compute_one, .progress = TRUE) %>%
    invisible %>%
    unlist %>%
    array(dim = c(length(RPs), nrow(discharges), ncol(discharges))) %>%
    aperm(c(2,3,1))

flog.info('WRITING OUTPUT')

nc %>% ncvar_put(qRP, peak_discharges)
nc %>% nc_close()

flog.info('DONE')


