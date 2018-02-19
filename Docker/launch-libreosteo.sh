#!/bin/bash

sql_type=$1
sql_host=$2
sql_port=$3
sql_name=$4
sql_user=$5

local_file='Libreosteo/settings/local.py'
bin_local_file='Libreosteo/settings/local.pyc'
tmp_constant_file='/tmp/pre_local.py'

cat <<EOT > $tmp_constant_file
host = "${sql_host:-db}"
port = ${sql_port:-5432}
name = "${sql_name:-postgres}"
user = "${sql_user:-postgres}"
EOT

if ! echo "$sql_type" | grep -q 'postgres'
then
    rm -f $local_file $bin_local_file
else
    cat $tmp_constant_file ${local_file}.pg > $local_file
fi

python manage.py migrate
python server.py
