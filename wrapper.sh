#!/bin/bash

set -m # exit at the first error
# Start the primary process and put it in the background
/docker-entrypoint.sh neo4j &

# wait for Neo4j
wget --quiet --tries=10 --waitretry=2 -O /dev/null http://localhost:7474

# Check data available or not
output="$(cypher-shell -u neo4j "match(n) return count(n)" --format plain | xargs)"

IFS=' ' #setting space as delimiter
read -ra ADDR <<<"$output" # reading str as an array as tokens separated by IFS
availnode=${ADDR[1]}

# Start the inital_data process
if [ "$availnode" == '0' ]; then ./initial-data.sh; fi

# the inital_data might need to know how to wait on the
fg %1
