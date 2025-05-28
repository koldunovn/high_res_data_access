# not needed on LUMI
# conda activate aqua

yes | aqua install lumi -e $AQUA/config

# modify according to your folder structure
CATDIR=$AQUA/../high_res_data_access/aqua_catalog

# let's install the data access catalog
aqua add data-access -e $CATDIR

# If you need to install any other aqua catalog to not disrupt your current installation
# you can do it here

# AQUA_CATALOG=$AQUA/../Climate-DT-catalog

# we loop over the catalogs and install them
# aqua add obs -e $CATDIR/catalogs/obs
# aqua add climatedt-phase1 -e $CATDIR/catalogs/climatedt-phase1
# aqua add lumi-phase1 -e $CATDIR/catalogs/lumi-phase1
# aqua add lumi-phase2 -e $CATDIR/catalogs/lumi-phase2
# aqua add nextgems4 -e $CATDIR/catalogs/nextgems4
# aqua add climatedt-e25.1 -e $CATDIR/catalogs/climatedt-e25.1
# aqua add climatedt-o25.1 -e $CATDIR/catalogs/climatedt-o25.1