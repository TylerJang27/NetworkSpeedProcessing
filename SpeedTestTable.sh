#!/bin/bash
#create a speed test table with 5 columns 10 rows

#Create top of the table

#input should be one less than desired number of tests
numtests=$1
if [[ -z $numtests ]]; then
	numtests=10
fi
numdisplay=$(( $numtests - 1 ))

#Print the nums at top of table and format dashes
itemarray=("location" "download" "upload" "time" "latency")
#for loops to create speed test number
downs=()
ups=()
lats=()
#for y in {0..$numdisplay}
for (( y=0; y<=$numdisplay; y++ ))
do  
    #Print the side nums and |  
    printf "%s %d | " "test" $y >> all_speed_tests.txt
    #for loop to create x   
    for x in {0..4}
    do 
    #item varibles referenced from the summary file, tab for spacing  
        dataop="${itemarray[x]}"
        datapos="$dataop:$y"
        itemval="$(grep "$datapos" summary.txt|awk '{print $2 $3}')"
	if [[ "$x" == "1" ]]; then
		#totals[$x]=$(echo($totals[$x] + $itemval | bc))
		downs[$y]=$itemval
	elif [[ "$x" == "2" ]]; then
		#totals[$x]=$(echo($totals[$x] + $itemval | bc))
		ups[$y]=$itemval
	elif [[ "$x" == "4" ]]; then
		#totals[$x]=$(echo($totals[$x] + $itemval | bc))
		lats[$y]=$itemval
	fi
        printf "%-30s" $itemval >> all_speed_tests.txt

    done
    #Print
    echo >>all_speed_tests.txt
done

#Grab the most recent data to add to last_speed_test.txt
totals=()
avgarray=()
totals[0]=0
avgarray[0]="$(grep 'location:0' summary.txt|awk '{print $2 $3}')"
totals[1]=$( IFS="+"; bc <<< "${downs[*]}" )
avgarray[1]=$(bc -l <<< "${totals[1]} / $numtests" )
totals[2]=$( IFS="+"; bc <<< "${ups[*]}" )
avgarray[2]=$(bc -l <<< "${totals[2]} / $numtests" )
totals[3]=0
avgarray[3]="$(grep 'time:0' summary.txt|awk '{print $2 $3}')"
totals[4]=$( IFS="+"; bc <<< "${lats[*]}" )
avgarray[4]=$(bc -l <<< "${totals[4]} / $numtests" )

touch last.temp
mv last.temp last_speed_test.txt

printf "%s 0 | " "test" >> last_speed_test.txt

if [[ -z ${avgarray[1]} ]]; then
	avgarray[1]="0"
fi
if [[ -z ${avgarray[2]} ]]; then
	avgarray[2]="0"
fi
if [[ -z ${avgarray[4]} ]]; then
	avgarray[4]="0"
fi

#Print to last_speed_test.txt
printf "%-30s" ${avgarray[0]} >> last_speed_test.txt
printf "%-30.8f" ${avgarray[1]} >> last_speed_test.txt
printf "%-30.8f" ${avgarray[2]} >> last_speed_test.txt
printf "%-30s" ${avgarray[3]} >> last_speed_test.txt
printf "%-30.3f" ${avgarray[4]} >> last_speed_test.txt


