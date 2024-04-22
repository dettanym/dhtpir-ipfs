import subprocess
import re
import json
import math

def run_command_no_output(command):
    try:
        subprocess.check_call(command)
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to run: {' '.join(command)}")
        return False

def run_command(command, output_file):
    try:
        with open(output_file, 'w') as f:
            subprocess.check_call(command, stdout=f, stderr=open('err.txt', 'w'))
        print(f"Success {command}")
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to run: {' '.join(command)}")
        return False

def parse_cwpir(log_dir):
    # Open the file and read the content
    with open(f'{log_dir}/cwpir.txt', 'r') as file:
        log_content = file.read()

    # Create a dictionary to store the extracted values
    data = {}

    # Use regular expressions to extract the values
    data['Poly Mod Degree'] = int(re.search(r'Poly Mod Degree:\s+(\d+)', log_content).group(1))
    data['Number of Keywords'] = int(re.search(r'Number of Keywords:\s+(\d+)', log_content).group(1))
    data['Hamming Weight'] = int(re.search(r'Hamming Weight:\s+(\d+)', log_content).group(1))
    data['Database Prep (ms)'] = int(re.search(r'Database Prep\s+:\s+(\d+)', log_content).group(1))
    data['Total Server (ms)'] = int(re.search(r'Total Server\s+:\s+(\d+)', log_content).group(1))
    data['Data Independant KB (Relin keys)'] = int(re.search(r'Data Independant:\s+(\d+) KB \(Relin keys\)', log_content).group(1))
    data['Data Independant KB (Gal Keys)'] = int(re.search(r'Data Independant:.+\+ (\d+) KB \(Gal Keys\)', log_content).group(1))
    data['Data Dependant KB (Query)'] = int(re.search(r'Data Dependant: (\d+) KB \(Query\)', log_content).group(1))
    data['Data Dependant KB (Reponse)'] = int(re.search(r'Data Dependant:.+\+ (\d+) KB \(Reponse\)', log_content).group(1))

    # Write the extracted values to a JSON file
    with open(f'{log_dir}/cwpir.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

def parse_sealpir(log_dir):
    try:
        with open(f"{log_dir}/sealpir.txt", 'r') as f:
            log_data = f.read()
    except FileNotFoundError:
        return "File not found. Please check the file path."

    data_dict = {}
    
    fields_to_extract = [
        "number_of_elements",
        "max_element_size",
        "PIRServer_reply_generation_time",
        "query_size",
        "reply_size",
        "size_gal_keys",
    ]
    
    for field in fields_to_extract:
        pattern = re.compile(rf"{field}: (\d+)")
        match = pattern.search(log_data)
        if match:
            data_dict[field] = int(match.group(1))
        else:
            data_dict[field] = None

    # Write the extracted values to a JSON file
    with open(f'{log_dir}/sealpir.json', 'w') as json_file:
        json.dump(data_dict, json_file, indent=4)

def parse_spiral(log_dir, version="spiral"):
    
    with open(f"{log_dir}/{version}.txt", 'r') as file:
        log_content = file.read()
    
    patterns = {
        "Number of items" : r"Number of items\s*:\s*(\d+)",
        "n" : r"PIR over n=(\d+) elements",
        "Item size (B)" : r"Item size\s*:\s*(\d+)",
        "size (B)" : r"elements of size (\d+) bytes each",
        "Total offline query size (KB)": r"Total offline query size\s*\(b\)\s*:\s*(\d+)",
        "First dimension": r"First dimension\s*\(b\)\s*:\s*(\d+)",
        "Total for other dimensions": r"Total for other dimensions\s*\(b\)\s*:\s*(\d+)",
        "Total online query size (KB)": r"Total online query size\s*\(b\)\s*:\s*(\d+)",
        "Response size (KB)": r"Response size\s*\(b\)\s*:\s*(\d+)",
        "Main expansion (us)": r"Main expansion\s*\(CPU·us\)\s*:\s*(\d+)",
        "Further dimension expansion (us)": r"Further dimension expansion\s*\(CPU·us\)\s*:\s*(\d+)",
        "Conversion (us)": r"Conversion \(CPU·us\)\s*:\s*(\d+)",
        "Database-independent computation Total (us)": r"Database-independent computation.*?Total \(CPU·us\)\s*:\s*(\d+)",
        "First dimension multiply (us)": r"First dimension multiply \(CPU·us\)\s*:\s*(\d+)",
        "Folding (us)": r"Folding \(CPU·us\): (\d+)",
        "Database-dependent computation Total (us)": r"Database-dependent computation.*?Total \(CPU·us\)\s*:\s*(\d+)",
        "Key generation (us)": r"Key generation \(CPU·us\)\s*:\s*(\d+)",
        "Query generation (us)": r"Query generation \(CPU·us\)\s*:\s*(\d+)",
        "Decoding (us)": r"Decoding \(CPU·us\)\s*:\s*(\d+)"
    }
    
    results = {}
    for field_name, pattern in patterns.items():
        match = re.search(pattern, log_content, re.DOTALL)
        if match:
            results[field_name] = int(match.group(1))
        else:
            results[field_name] = None
    
    with open(f'{log_dir}/{version}.json', 'w') as json_file:
        json.dump(results, json_file, indent=4)
              
def parse_fastpir(log_dir, num_rows, item_size):
    # Open the file and read the content
    with open(f'{log_dir}/fastpir.txt', 'r') as file:
        data = file.read()

    # Define the regex patterns for each item to be extracted
    patterns = {
        "Gal Keys (B)": r"Gal Keys: (\d+) bytes",
        "Query size (B)": r"Query size: (\d+) bytes",
        "Response size (B)": r"Response size: (\d+) bytes",
        "DB preprocessing time (us)": r"DB preprocessing time \(us\): (\d+)",
        "Query generation time (us)": r"Query generation time \(us\): (\d+)",
        "Response generation time (us)": r"Response generation time \(us\): (\d+)",
        "Response decode time (us)": r"Response decode time \(us\): (\d+)"
    }

    # Create a dictionary to store the extracted values
    extracted_values = {
        "Number of items": num_rows,
        "Item size (B)": item_size,       
    }

    # Loop through each pattern and find the matching value in the data
    for key, pattern in patterns.items():
        match = re.search(pattern, data)
        if match:
            extracted_values[key] = int(match.group(1))
        else:
            extracted_values[key] = None

    # Write the extracted values to a JSON file
    with open(f'{log_dir}/fastpir.json', 'w') as json_file:
        json.dump(extracted_values, json_file, indent=4)

def parse_onionpir(log_dir, num_rows, item_size):
    # Open the file and read the content
    with open(f'{log_dir}/onionpir.txt', 'r') as file:
        data = file.read()

    # Define the regex patterns for each item to be extracted
    patterns = {
        "Gal Keys (KB)": r"Gal keys Size: (\d+) KB",
        "Query size (KB)": r"Query Size: (\d+) KB",
        "Reply size (B)": r"Reply Size: (\d+) KB",
        "Preprocessing time (ms)": r"Main: PIRServer pre-processing time: (\d+) ms",
        "Query generation time (ms)": r"Main: PIRClient query generation time: (\d+) ms",
        "Reply time (ms)": r"Main: PIRServer reply generation time: (\d+) ms",
    }

    # Create a dictionary to store the extracted values
    extracted_values = {
        "Number of items": num_rows,
        "Item size (B)": item_size,       
    }

    # Loop through each pattern and find the matching value in the data
    for key, pattern in patterns.items():
        match = re.search(pattern, data)
        if match:
            extracted_values[key] = int(match.group(1))
        else:
            extracted_values[key] = None

    # Write the extracted values to a JSON file
    with open(f'{log_dir}/onionpir.json', 'w') as json_file:
        json.dump(extracted_values, json_file, indent=4)

def main():
    
    for payload_byte_size in [256*1024]:
        for log_num_rows in [11, 12]:
            num_rows = 2**log_num_rows
            log_dir = f"logs/logs-{num_rows}-{payload_byte_size}"
            
            log_num_rows = int(math.log(num_rows, 2))
            run_command_no_output(["mkdir", "-p", log_dir])

            # SealPIR
            if run_command(["SealPIR-clone/bin/main2", str(num_rows), str(payload_byte_size)], f"{log_dir}/sealpir.txt"):
                parse_sealpir(log_dir)
            else :
                print("Failed to run SealPIR")

            # FastPIR
            if run_command(["FastPIR-clone/bin/fastpir", "-n", str(num_rows), "-s", str(payload_byte_size)], f"{log_dir}/fastpir.txt"):
                parse_fastpir(log_dir, num_rows, payload_byte_size)
            else:
                print("Failed to run FastPIR")

            # # Constant-weight PIR
            # command = ["constant-weight-pir/src/build/main", f"--num_keywords={num_rows}", f"--response_bytesize={payload_byte_size}"]
            # if run_command(command, f"{log_dir}/cwpir.txt"):
            #     parse_cwpir(log_dir)
            
            # OnionPIR
            command = ["Onion-PIR-clone/onionpir", str(num_rows), str(payload_byte_size)]
            if run_command(command, f"{log_dir}/onionpir.txt"):
                parse_onionpir(log_dir, num_rows, payload_byte_size)
            else:
                print("Failed to run OnionPIR")

            # Spiral Variants
            first_dim = 8
            other_dim = log_num_rows - first_dim
            base_spiral_command = ["spiral-clone/build/spiral", str(first_dim), str(other_dim), "0"]

            # Spiral
            if run_command(base_spiral_command, f"{log_dir}/spiral.txt"):
                parse_spiral(log_dir, 'spiral')
            else:
                print("Failed to run Spiral")

            # SpiralStream
            if run_command(base_spiral_command + ["--direct-upload"], f"{log_dir}/spiral-stream.txt"):
                parse_spiral(log_dir, 'spiral-stream')
            else:
                print("Failed to run SpiralStream")

            # SpiralPack
            if run_command(base_spiral_command + ["--high-rate"], f"{log_dir}/spiral-pack.txt"):
                parse_spiral(log_dir, 'spiral-pack')
            else:
                print("Failed to run SpiralPack")

            # SpiralStreamPack
            if run_command(base_spiral_command + ["--direct-upload", "--high-rate"], f"{log_dir}/spiral-stream-pack.txt"):
                parse_spiral(log_dir, 'spiral-stream-pack')
            else:
                print("Failed to run SpiralStreamPack")

            print("Done")

if __name__ == "__main__":
    main()
