#!/bin/sh

local_file='Libreosteo/settings/local.py'
bin_local_file='Libreosteo/settings/local.pyc'
tmp_constant_file='/tmp/pre_local.py'
tmp2_constant_file='/tmp/pre_local2.py'

KEY=$(python /usr/local/bin/django-secret-key)

cat <<EOT > $tmp_constant_file
host = "$sql_host"
port = $sql_port
name = "$sql_name"
user = "$sql_user"
EOT

cat <<EOT > $tmp2_constant_file
SECRET_KEY = '$KEY'
DEBUG = $debug
TEMPLATE_DEBUG = $debug
EOT

if ! echo "$sql_type" | grep -q 'postgres'
then
    rm -f $local_file $bin_local_file
    cat $tmp2_constant_file ${local_file}.sqlite > $local_file
else
    cat $tmp2_constant_file $tmp_constant_file ${local_file}.pg > $local_file
fi

python manage.py migrate
python manage.py runserver 0.0.0.0:8085
