#!/bin/bash
cd $(dirname $0)

#check for linux updates and the appropiate packages

#number of tests to run (default 4)
numtests=$1
#if s, add new tests to summary table
summ=$2
#server to run tests on (default 16970)
server=$3
#if u, update packages
update=$4

#update packages
if [[ "$update" == "u" ]]; then
	echo "y" | sudo apt-get dist-upgrade
	echo "y" | sudo apt-get install speedtest-cli
	echo "y" | sudo apt-get install bc
	echo "y" | sudo apt-get install jq
fi

touch summary.temp
mv summary.temp summary.txt

#set defaults
if [[ -z $numtests ]]; then
	numtests=4
fi
if [[ -z $server ]]; then
	server=16970
fi

TEMPFILE=/tmp/$$.tmp
echo 0 > $TEMPFILE

#create a file to store speed test summary
sudo touch summary.txt
sudo chmod 777 summary.txt

#for loop to run the test numtest times
(for test in $(seq 1 $numtests); do
(
  (


#create a temporary file to store json data from each test if such a
#file name exists then it will create another file 
name=speedtestdata
if [[ -e $name.save ]] ; then
	i=0
    while [[ -e $name-$i.save ]] ; do
        let i++
    done
    name=$name-$i
fi

#calls speed test program and pipes json output to the speed test file 
sudo speedtest-cli  --server $server --json | sudo tee "$name".save >/dev/null
#changes permission on data file so the anyone can read or write to it
sudo chmod 777 "$name".save

#parsing variables from json file with jq program
location=$(jq '.server.name' "$name".save)
download=$(jq '.download' "$name".save)
upload=$(jq '.upload' "$name".save)
time=$(jq '.timestamp' "$name".save)
latency=$(jq '.server.latency' "$name".save)

btoMb=1000000
#echos all results
printf "\nlocation of the server is: $location\n"
echo "your download speed is:"
echo "$download / 1000000" | bc -l
echo "your upload speed is:"
echo "$upload / 1000000" | bc -l
echo "time is: $time"
echo "latency is: $latency" 

#counter to keep track of test run
COUNTER=$[$(cat $TEMPFILE)]

#stores results in the accumalated summary file
echo "location:$COUNTER $location" | sudo tee -a summary.txt >/dev/null
echo "download:$COUNTER $download" | sudo tee -a summary.txt >/dev/null
echo "upload:$COUNTER $upload" | sudo tee -a summary.txt >/dev/null
echo "time:$COUNTER $time" | sudo tee -a summary.txt >/dev/null
echo "latency:$COUNTER $latency" | sudo tee -a summary.txt >/dev/null

) &

PID=$! #simulate a long process

#stores count in tempfile
COUNTER2=$[$(cat $TEMPFILE)]

printf "THIS MAY TAKE A WHILE, PLEASE BE PATIENT WHILE \nINTERNET SPEED TEST $COUNTER2 IS RUNNING...\n"
# While process is running...
while kill -0 $PID 2> /dev/null; do 
    printf  "▓"
    sleep 2
done

COUNTER=$[$(cat $TEMPFILE) + 1]
echo $COUNTER > $TEMPFILE

printf "\nAlways know your internet speed!\n"
)

sleep 1; done;)
unlink $TEMPFILE

#run table parse for summary file
echo "records of your internet speeds are also saved to a file named "\"SpeedTestTable.txt"\" " 
echo ":)"
sudo touch SpeedTestTable.txt
sudo chmod 777 SpeedTestTable.txt

#add new data to logs
./SpeedTestTable.sh $numtests
./create_all_logs.sh $summ
#if this data should be included in the summary, graph it
if [[ $summ == 's' ]]; then
	echo nvmd
else
	./SpeedTestParser3.py
fi

#remove excesss speedtestdata
for (( y=0; y<=10; y++ ))
do
	echo $y
	mv "./speedtestdata-${y}.save" "./speedtestdata.save"
done
