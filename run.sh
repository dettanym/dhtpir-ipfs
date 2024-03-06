log_num_rows=10
num_rows=$(( 2**log_num_rows ))
payload_byte_size=10

# SealPIR
SealPIR/bin/main2 $num_rows $payload_byte_size &&

# FastPIR
FastPIR/bin/fastpir -n $num_rows -s $payload_byte_size &&

# Constant-weight PIR
constant-weight-pir/src/build/main --num_keywords=$num_rows --response_bytesize=$payload_byte_size &&

## Spiral Variants

first_dim=8
other_dim=$((log_num_rows - first_dim))

# TODO: choose the payload size in Spiral
# TODO: Set the number of threads to max in the code

# Spiral
spiral/build/spiral $first_dim $other_dim 0 &&

# SpriralStream
spiral/build/spiral $first_dim $other_dim 0 --direct-upload &&

# SpriralPack
spiral/build/spiral $first_dim $other_dim 0 --high-rate &&

# SpriralStreamPack
spiral/build/spiral $first_dim $other_dim 0 --direct-upload --high-rate &&

echo "Done"
