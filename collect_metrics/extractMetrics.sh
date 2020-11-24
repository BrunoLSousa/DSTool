#!/bin/bash

# store arguments in a special array 
args="$@"
# get number of elements 
ELEMENTS=${#@}

call_metrics_tool(){
    IN="$1"
    OUT="$2"

    # get the number of files and subdirectories existing in the the path IN
    directories=`ls "$IN" | wc -l`

    # create a string vector spliting IN by '/'
    IFS='/'
    read -ra ADDR <<< "$IN"
    
    # create directory of the project in OUT
    mkdir "$OUT"/${ADDR[$(($size-1))]}

    for ((index=1; index<=($directories-1); index++)); do

        echo $'\n----------------------- Collecting metrics from the release' $index $'out of' $(($directories-1)) $'... ----------------------\n'

        EXPORTION_DIR="$OUT"
        IN_RELEASE="$IN"

        # build the IN directory by including each number of release from the project        
        if [ "${IN: -1}" == "/" ]; then
            IN_RELEASE="$IN_RELEASE"$index
        else
            IN_RELEASE="$IN_RELEASE"/$index
        fi

        # build the OUT directory by including the name of the project and each number of release from the project  
        if [ "${OUT: -1}" == "/" ]; then
            EXPORTION_DIR="$EXPORTION_DIR""${ADDR[$(($size-1))]}"/$index
        else
            EXPORTION_DIR="$EXPORTION_DIR"/"${ADDR[$(($size-1))]}"/$index
        fi
        
        # create the release number folder in Metrics folder
        mkdir "$EXPORTION_DIR"
        
        # run the metrics collection tool (ck.jar) passing as parameters the path of the source code of the release 
        # and the path where the metrics will be exported
        java -jar ck.jar "$IN_RELEASE" false 0 true "$EXPORTION_DIR"/

        echo $'\n----------------------------------------------------------------------------------------\n'

    done

}


# checks if the command for running the script was provided correctly.
if [ $ELEMENTS -eq 4 ] && [ $1 == "-i" ] && [ $3 == "-o" ]; then
    if [ -d "$2" ] && [ -d "$4" ]; then

        # call the function of metrics collection
        call_metrics_tool "$2" "$4"

    else
        echo "Check if the path provided for input or output are really directories!!!"
    fi
else
    echo "Usage ./extractMetrics.sh -i <path to project with source code of the releases> -o <path to save the output files>"
fi
