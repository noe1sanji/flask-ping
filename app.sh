#!/bin/bash


if [ ! -f "app/database.db" ]; then
  flask init-db
fi


export FLASK_DEBUG=true
flask run --debugger
