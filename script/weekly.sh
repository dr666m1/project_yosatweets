#!/bin/bash
chdir $(dirname $0)
rm ./../data/last_week.db
mv ./../data/this_week.db ./../data/last_week.db

