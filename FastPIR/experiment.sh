# iterate over log_n from 1 to 10
# run the experiment for each 2^log_n

for log_n in {2..20}
do
    # run the experiment
    echo "----------------------------------------"
    echo "Running experiment for n = $((2**log_n))"
    bin/fastpir -n $((2**log_n)) -s 10000
done
