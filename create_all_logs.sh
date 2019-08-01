#!/bin/bash
#create a running log of the last 1000 speed tests

#whether or not to add to the last 14 speed test summary
add_to_summ=$1

#Create top of the table
touch temp_log.txt
echo "                                                            Last 1000 Speed Tests           " >>temp_log.txt
echo "----------------------------------------------------------------------------------------------------------------------------------------------------------------" >>temp_log.txt

numtests=10
numdisplay="$(( $numtests - 1 ))"

#Print the nums at top of table and format dashes
echo -n "      |">>temp_log.txt; printf "%-30s"      "location"      "download"      "upload"        "time"      "latency"      >>temp_log.txt ; echo >>temp_log.txt
echo  "----------------------------------------------------------------------------------------------------------------------------------------------------------------" >>temp_log.txt

cat all_speed_tests.txt | tail -n +5|tail -n 1000 >>temp_log.txt
mv temp_log.txt all_speed_tests.txt

#itemarray=("location" "download" "upload" "time" "latency")
##for loops to create speed test number
#for y in {0..$numdisplay}
#do  
#    #Print the side nums and |  
#    printf "%s %d | " "test" $y
#    #for loop to create x   
#    for x in {0..4}
#    do 
#    #item varibles referenced from the summary file, tab for spacing  
#        dataop="${itemarray[x]}"
#        datapos="$dataop:$y"
#        itemval="$(grep "$datapos" summary.txt|awk '{print $2 $3}')"
#        printf "%-30s" $itemval
#    done
#    #Print
#    echo
#done
##Print bottom dashes for format
##echo "----------------------------------------------------------------------------------------------------------------------------------------------------------------"

#create an updated log of the last 14 speed tests

#tests for whether speed test should be added to summary
if [[ "$add_to_summ" == "s" ]]; then
	echo nvmd
else
	touch summ.txt
	#print header to summary
	echo "                                                     Last 14 Speed Test Summaries           " >>summ.txt
	echo "----------------------------------------------------------------------------------------------------------------------------------------------------------------" >>summ.txt
	echo -n "      |">>summ.txt; printf "%-30s"      "location"      "download"      "upload"        "time"      "latency">>summ.txt       ; echo >>summ.txt
	echo  "----------------------------------------------------------------------------------------------------------------------------------------------------------------" >>summ.txt
	#prints all except earliest test
	cat SpeedTestTable.txt | tail -n +5 |tail -n 14 >> summ.txt
	#prints most recent test to summary
	cat last_speed_test.txt|head -n 1 >> summ.txt
	echo "" >> summ.txt
	mv summ.txt SpeedTestTable.txt
fi
