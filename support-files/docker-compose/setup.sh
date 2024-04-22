#!/bin/bash

function setup_network() {
    docker network create traefik
}

function setup_env() {
    export RABBITMQ_DEFAULT_PASS=`openssl rand -hex 32`
    envsubst < .env.example > .env
}

PS3='Please enter your choice: '
options=("setup-network" "setup-env" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "setup-network")
            setup_network
            break
            ;;
        "setup-env")
            setup_env
            break
            ;;
        "Quit")
            break
            ;;
        *) echo "invalid option $REPLY";;
    esac
done