import os

# os.system('python ../visualization/plot_summary.py \
# -i ./op/summary.xml \
# -o ./graphs/summary_running.png \
# --xtime1 --ygrid \
# --ylabel "running vehicles [#]" --xlabel "time" \
# --title "running vehicles over time" --adjust .14,.1')



# os.system('python ../tools/plot_trajectories.py -t ts \
# -o ./graphs/timeSpeed_output.png ./op/fcd.xml \
# --filter-ids v.0.2.0,v.15.1.0,v.9.0.0,v.10.10.0,v.11.1.0,v.7.6.0 --legend')




# os.system('python ../visualization/plot_tripinfo_distributions.py \
#  -i ./op/tripinfo.xml \
#  -o ./graphs/tripinfo_distribution_duration.png -v -m duration \
#  --minV 0 --maxV 30 --bins 20 --xticks 25,30,1,5 \
#  --xlabel "duration [s]" --ylabel "number [#]" \
#  --title "duration distribution" \
#  --xlabelsize 14 --ylabelsize 14 --titlesize 16 \
#  --adjust .14,.1 --xlim 25,30')



# os.system('python ../tools/plot_trajectories.py -t xy -o ./graphs/allLocations_output.png ./op/fcd.xml')

# os.system('python ../tools/plot_trajectories.py -t da -o ./graphs/Plot_trajectories.png ./op/fcd.xml')

# os.system('python ../visualization/plotXMLAttributes.py ./op/summary.xml -x time -y running,halting -o ./graphs/plot-running.png --legend')

# os.system('python ../visualization/plot_tripinfo_distributions.py -i ./op/tripinfo.xml -o ./graphs/stopCountDist.png \
#  --measure waitingCount --bins 10 --maxV 10 \
#  --xlabel "number of stops [-]" --ylabel "count [-]" \
#  --title "distribution of number of stops" --colors blue -b --no-legend')