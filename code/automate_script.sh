source ./.env
date=$(date +%Y%m%d)
page_sql_file="${DUMPS_URL_PREFIX}{date}/${DUMP_file_PREFIX}{date}{PAGE_DUMP_file_SUFFIX}"
pagelinks_sql_file="${DUMPS_URL_PREFIX}{date}/${DUMP_file_PREFIX}{date}{PAGELINKS_DUMP_file_SUFFIX}"
categorylinks_sql_file="${DUMPS_URL_PREFIX}{date}/${DUMP_file_PREFIX}{date}{CATEGORYLINKS_DUMP_file_SUFFIX}"

wget "${page_sql_file}.gz" && gunzip "${page_sql_file}.gz"
wget "${pagelinks_sql_file}.gz" && gunzip "${pagelinks_sql_file}.gz" 
wget "${categorylinks_sql_file}.gz" && gunzip "${categorylinks_sql_file}.gz" 
mv /docker-entrypoint-initdb.d/simplewiki-populate-tables-and-cleanup.sql ./ && rm /docker-entrypoint-initdb.d/* && mv ./*.sql /docker-entrypoint-initdb.d/

mysql -p $DATABASE_PWD < "/docker-entrypoint-initdb.d/${page_sql_file}"
mysql -p $DATABASE_PWD < "/docker-entrypoint-initdb.d/${pagelinks_sql_file}"
mysql -p $DATABASE_PWD < "/docker-entrypoint-initdb.d/${categorylinks_sql_file}"
mysql -p $DATABASE_PWD < /docker-entrypoint-initdb.d/simplewiki-populate-tables-and-cleanup.sql

python repopulate_cache.py