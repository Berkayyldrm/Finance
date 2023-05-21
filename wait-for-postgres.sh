#!/bin/bash

set -e

host="$1"
shift
cmd="$@"

until PGPASSWORD="qwertypoikjh1" psql -h "db" -U "postgres" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 10
done

>&2 echo "Postgres is up - executing command"
exec $cmd