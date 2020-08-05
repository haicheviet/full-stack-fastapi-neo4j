#!/bin/bash
# shellcheck disable=SC2002

set -e

# check

# Init data
cat ./movie_data/movie_db.cypher | bin/cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" --format plain

# Init index
bin/cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -- "CREATE CONSTRAINT ON (p:Person) ASSERT p.name IS UNIQUE;"
bin/cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" "CREATE CONSTRAINT ON (p:Movie) ASSERT p.name IS UNIQUE;"