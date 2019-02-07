#!/usr/bin/env bash

CHART_ID="chart1"
LAYOUT="Chart: [[data: [[0]], transform: numbers, id: $CHART_ID]]"

start_page()
{
    # start the server, providing an initial layout
    awe start --open-browser --obj "${LAYOUT}" &

    # cleanup to stop server when script is done
    local server_pid=$?
    trap "kill ${server_pid}" EXIT
}

wait_for_started()
{
    for i in $(seq 5); do
        echo "waiting for page to start (attempt: $i)"
        awe --quiet status && break || sleep 1
    done
}

add_data()
{
    # add points to chart in a loop
    for index in $(seq 1 10); do
        echo "index: $index"
        # data is a list of entries. in this case, because we are using the numbers transformer,
        # each entry is a list of numbers itself.
        awe -q call --element-id ${CHART_ID} -m add -k "data: [[$index]]"
        sleep 0.3
    done
}

main()
{
    start_page
    wait_for_started
    add_data
}

main
