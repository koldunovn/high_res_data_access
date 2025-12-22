#!/bin/bash
machine=lumi

# We install aqua (can be installed interactively with --core path/to/AQUA)
yes | aqua install $machine

# Modify according to your folder structure
# There is a catalog specific to this data access experiment
CATDIR=$AQUA/../high_res_data_access/aqua_catalog

# let's install the data access catalog
aqua add data-access -e $CATDIR

# If you need to install any other aqua catalog to not disrupt your current installation
# you can do it here, by default we install the catalogs useful on lumi

# Modify according to your folder structure
# AQUA_CATALOG=$AQUA/../Climate-DT-catalog

# Uncomment the following lines to install additional catalogs
# aqua add obs -e $AQUA_CATALOG/catalogs/obs
# aqua add climatedt-phase1 -e $AQUA_CATALOG/catalogs/climatedt-phase1
# aqua add lumi-phase1 -e $AQUA_CATALOG/catalogs/lumi-phase1
# aqua add lumi-phase2 -e $AQUA_CATALOG/catalogs/lumi-phase2
# aqua add nextgems4 -e $AQUA_CATALOG/catalogs/nextgems4
# aqua add climatedt-e25.1 -e $AQUA_CATALOG/catalogs/climatedt-e25.1
# aqua add climatedt-o25.1 -e $AQUA_CATALOG/catalogs/climatedt-o25.1
# aqua add ci -e $AQUA_CATALOG/catalogs/ci