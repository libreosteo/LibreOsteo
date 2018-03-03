#!/bin/bash

rank=$1

rank=${rank:-prod}

source check_libreosteo.sh
source constant.sh

#MAIN
main() {
    lo_rank_dir=$LO_DIR/$rank
    lo_media_dir=$lo_rank_dir/media
    lo_sql_dir=$lo_rank_dir/sql

    cd $lo_rank_dir && docker-compose down
    rm -rf $LO_DIR/$rank
}

check_remove_all
main
