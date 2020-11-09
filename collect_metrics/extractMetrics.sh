#  if [ "$#" -eq  "0" ]
#    then
#      echo "No arguments supplied"
#  else
#      echo "Hello world"
#  fi

# store arguments in a special array 
args="$@"
# get number of elements 
# ELEMENTS=${#args[@]} 
ELEMENTS=${#@}
# echo "Dê algum sinal de vida script!!!"

# add_a_user(){
#   USER=$1
#   PASSWORD=$2
#   shift; shift;
#   # Having shifted twice, the rest is now comments ...
#   COMMENTS=$@
#   echo "Adding user $USER ..."
#   echo useradd -c "$COMMENTS" $USER
#   echo passwd --stdin $USER $PASSWORD
#   echo "Added user $USER ($COMMENTS) with pass $PASSWORD"
# }

call_metrics_tool(){
    IN="$1"
    OUT="$2"

    # echo $IN
    # echo $OUT


    directories=`ls "$IN" | wc -l`

    # echo $directories
    IFS='/'
    read -ra ADDR <<< "$IN"
    # echo ${ADDR[@]}
    # echo ${#ADDR[@]}
    # size=${#ADDR[@]}
    # JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64"

    # CLASSPATH=/home/freddy/myapp/lib/whatever.jar:.
    
    # create directory of the project in OUT
    mkdir "$OUT"/${ADDR[$(($size-1))]}

    # for entry in `ls "$IN"`; do
    # for index in `seq 1 $directories`; do

    for ((index=1; index<=$directories; index++)); do

        EXPORTION_DIR="$OUT"/${ADDR[$(($size-1))]}/$entry
        EXPORTION_DIR="$OUT"
        IN_RELEASE="$IN"
        
        if [ "${IN: -1}" == "/" ]; then
            IN_RELEASE="$IN_RELEASE"$index
        else
            IN_RELEASE="$IN_RELEASE"/$index
        fi

        if [ "${OUT: -1}" == "/" ]; then
            EXPORTION_DIR="$EXPORTION_DIR""${ADDR[$(($size-1))]}"/$index
        else
            EXPORTION_DIR="$EXPORTION_DIR"/"${ADDR[$(($size-1))]}"/$index
        fi
        # echo "$IN_RELEASE"
        # echo "$EXPORTION_DIR"
        mkdir "$EXPORTION_DIR"
        
        # $JAVA_HOME/jre/bin/java -cp $CLASSPATH MyJavaClass
        # $JAVA_HOME/jre/bin/java -jar ck.jar "$IN"/"$index" false 0 true "$EXPORTION_DIR"
        java -jar ck.jar "$IN_RELEASE" false 0 true "$EXPORTION_DIR"/


        # java -jar ck.jar /home/bruno/Área de Trabalho/Head-First-Design-Patterns/src/headfirst/ false 0 true /home/bruno/Área de Trabalho/Head-First-Design-Patterns/metrics/

        # exit 0

        # echo $entry
    done

}


# checks if the command for running the script was provided correctly.
if [ $ELEMENTS -eq 4 ] && [ $1 == "-i" ] && [ $3 == "-o" ]; then
    if [ -d "$2" ] && [ -d "$4" ]; then
        # implement the code
        # call the function
        # echo "Command type correctly and input and output are directories."

        # echo $2
        # echo $4

        call_metrics_tool "$2" "$4"
        
        # echo "Start of script..."
        # add_a_user bob letmein Bob Holness the presenter
        # add_a_user fred badpassword Fred Durst the singer
        # add_a_user bilko worsepassword Sgt. Bilko the role model
        # echo "End of script..."


    else
        echo "Check if the path provided for input or output are really directories!!!"
    fi
else
    echo "Usage ./extractMetrics.sh -i <path to project with source code of the releases> -o <path to save the output files>"
fi


# if [ $ELEMENTS -eq 4 ]
# # if (($ELEMENTS -eq 4 & $1 == "-i" & $3 == "-o" ))
# # & $1 == "-i" & $3 == "-o"]
#     then
#         echo $args[{$2}]
#         # checks if the directory provided are really directory
#         if [ -d $args[2] && -d $args[4] ]
#             then
#                 # implement the code
#                 # call the function
#                 echo "Command type correctly and input and output are directories."
#             else
#                 echo "Check if the path provided for input or output are really directories!!!"
#         fi
#     else
#         echo "Usage ./extractMetrics.sh -i <path to project with source code of the releases> -o <path to save the output files>"
# fi

# vector = (${args//;/ })

# echo ELEMENTS
 
# echo each element in array  
# for loop 
# for (( i=0;i<$ELEMENTS;i++))
# for i in {0..$ELEMENTS}
# for i in `seq 0 $ELEMENTS`
# for arg in "$@" 
# do 
#     echo $arg
#     # echo "ok"
#     # echo $args[$i]
# done