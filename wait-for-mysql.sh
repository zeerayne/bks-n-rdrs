#!/bin/sh
# wait-for-mysql.sh

set -e

for i in "$@"
do
case $i in
    -m=*|--master=*)
    MYSQL_MASTER="${i#*=}"
    ;;
    -s=*|--slave=*)
    MYSQL_SLAVE="${i#*=}"
    ;;
    -u=*|--user=*)
    MYSQL_USER="${i#*=}"
    ;;
    -p=*|--password=*)
    MYSQL_PASSWORD="${i#*=}"
    ;;
    -d=*|--database=*)
    MYSQL_DATABASE="${i#*=}"
    ;;
    *)
    ;;
esac
done
>&2 echo MASTER = ${MYSQL_MASTER}
>&2 echo SLAVE = ${MYSQL_SLAVE}
>&2 echo USER = ${MYSQL_USER}
>&2 echo PASSWORD = ${MYSQL_PASSWORD}
>&2 echo DATABASE = ${MYSQL_DATABASE}
PHRASE1="Connection test to ${MYSQL_MASTER} successfull"
PHRASE2="Connection test to ${MYSQL_SLAVE} successfull"
# Should be checked twice as MySQL cluster can be restarted after config is applied
for i in 1 2
do
  sleep 15

  until mysql --user=$MYSQL_USER --password=$MYSQL_PASSWORD --host=$MYSQL_MASTER $MYSQL_DATABASE \
  --execute "SELECT '${PHRASE1}'"; do
  >&2 echo "${MYSQL_MASTER} is unavailable - sleeping"
  sleep 5
  done

  until mysql --user=$MYSQL_USER --password=$MYSQL_PASSWORD --host=$MYSQL_SLAVE $MYSQL_DATABASE \
  --execute "SELECT '${PHRASE2}'"; do
    >&2 echo "${MYSQL_SLAVE} is unavailable - sleeping"
    sleep 5
  done
done

>&2 echo "MySQL cluster is up - can start now"
exit 0
