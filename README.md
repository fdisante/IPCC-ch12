# IPCC-ch12
Script collection to create Q100 maps from CMIPs and CORDEX total runoff output
STEPS:
1) Run the RTM CHyM-roff using interpolated runoff from CMIPs or CORDEX simulations (https://github.com/fdisante/CHyM-roff)
2) Create csv files using the dranetwrite utility available with the chym-esp package (https://github.com/ictp-esp/CHyM/tree/master/utility/dranetwrite)
3) Use the python scripts to create map plots (CORDEX/REGION/ch12_fig12.figNumber_plotting_code_Q100_REGION.py)

Static fields (DEM, direction matrix etc.) needed to run the CHyM-roff can be downloaded from the following link:
/home/esp-shared-a/Distribution/Projects/ACQWA/AR6/SOD/IPCC-ch12

