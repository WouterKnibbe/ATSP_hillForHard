import algorithm
import numpy as np
import json
import os
import argparse
import ast 
import time

# Initialize the parser
parser = argparse.ArgumentParser(description='Run the experiment with provided parameters.')

# Add arguments
parser.add_argument('sizes', type=str, help='A list of city sizes, e.g., "[10,12]"')
parser.add_argument('ranges', type=str, help='A list of value ranges, e.g., "[10,1000]"')
parser.add_argument('mutations', type=int, help='An integer mutations, e.g., 500')
parser.add_argument('continuation', type=str, default="", nargs='?', help='A list of matrix continuations, e.g., "[(7,10),(50,10)]". Corresponding matrices must be in "Progress" folder')

# Parse arguments
args = parser.parse_args()

# Convert string representations of lists to actual lists
sizes = ast.literal_eval(args.sizes)
ranges = ast.literal_eval(args.ranges)
if args.continuation == "":
    continuations = []
else:
    continuations = [",".join(map(str, tup)) for tup in ast.literal_eval(args.continuation)]


def custom_encoder(obj):
    """
    Custom JSON encoder function that converts non-serializable objects.
    Converts:
    - numpy arrays to lists
    - numpy int64 to int
    - numpy float64 to float
    """
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.inf):
        return "np.inf"
    else:
        # This will raise a TypeError for unknown types
        raise TypeError(f"Object of type '{obj.__class__.__name__}' is not JSON serializable")

def save_partial(results, citysize, range, time, contin):
    base_file_path = f"results{citysize}_{range}"
    file_extension = ".json"
    file_index = 0
    file_path = f"{base_file_path}{file_extension}"

    # Continue mode adds a suffix '_c'
    if contin:
        file_path = f"{base_file_path}_c{file_extension}"

    # Function to generate new file path with incrementing index
    def get_new_file_path():
        nonlocal file_index
        while True:
            new_file_path = f"{base_file_path}_{file_index}{file_extension}"
            if contin:
                new_file_path = f"{base_file_path}_c_{file_index}{file_extension}"
            if not os.path.exists(new_file_path):
                break
            elif os.path.getsize(new_file_path) <= 50 * 1024 * 1024:
                break
            file_index += 1
        return new_file_path

    # Check if the file exists and its size
    if os.path.exists(file_path) and os.path.getsize(file_path) >= 50 * 1024 * 1024:
        file_path = get_new_file_path()  # Get a new file path if current is too large

    # Check if the file exists to append or create new data structure
    if os.path.exists(file_path):
        with open(file_path, "r") as json_file:
            try:
                existing_data = json.load(json_file)
            except json.decoder.JSONDecodeError:
                existing_data = []
        existing_data.append((time, results))
        data_to_write = existing_data
    else:
        data_to_write = [(time, results)]

    # Write the data to the file with custom encoding
    with open(file_path, "w") as json_file:
        json.dump(data_to_write, json_file, default=custom_encoder)


def custom_decoder(obj):
    """
    Custom decoder function that converts specific JSON values back to their original types.
    Converts:
    - 'Infinity' to np.inf
    """
    if isinstance(obj, dict):
        for key, value in obj.items():
            if value == "Infinity":
                obj[key] = np.inf
            # elif isinstance(value, list):
                # Convert lists back to arrays
                # obj[key] = np.array(value)
            elif isinstance(value, dict):
                obj[key] = custom_decoder(value)
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            if value == "Infinity":
                obj[i] = np.inf
            # elif isinstance(value, list):
                # obj[i] = np.array(value)
            elif isinstance(value, dict):
                obj[i] = custom_decoder(value)
    return obj


def load_result(file_path):

  # Loading the JSON file with custom decoding
  with open(file_path, "r") as json_file:
      loaded_results = json.load(json_file, object_hook=custom_decoder)

  return loaded_results

def mutate_matrix(_matrix, _upper, _print):
    matrix = _matrix.copy()
    number1, number2 = 0, 0

    while number1 == number2:
        number1, number2 = np.random.randint(0,matrix.shape[0]), np.random.randint(0,matrix.shape[0])
    previous_number = matrix[number1,number2]
    while matrix[number1,number2] == previous_number:
        matrix[number1,number2] = np.random.randint(1,_upper)
    if _print:
        print(_matrix[number1,number2].round(1), "at", (number1,number2), "becomes", matrix[number1,number2].round(1))

    return matrix

def experiment(_cities, _ranges, _mutations, _continuations):
    for citysize in _cities:
        for rang in _ranges:
            range_results = {}

            # Record the start time
            start_time = time.time()

            if f"{citysize},{rang}" in _continuations:
                try:
                    hardest, matrix = load_result(f"Progress/continue{citysize}_{rang}.json")
                    matrix = np.array(matrix)
                except Exception as e:
                    print(f"{e}\n {citysize}_{rang} matrix not loaded, generating random matrix", flush=True)
                    # initialize the matrix with ints, but convert it to a floating-point type to enable np.inf
                    matrix = np.random.randint(1,rang,((citysize, citysize))).astype(float)
                    for x in range(citysize):
                        matrix[x, x] = np.inf
                    hardest = 0
            else:
                matrix = np.random.randint(1,rang,((citysize, citysize))).astype(float)
                for x in range(citysize):
                    matrix[x, x] = np.inf
                hardest = 0
        
            hardest_matrix = matrix
            
            for j in range(_mutations):
                iterations, optimal_tour, optimal_cost = algorithm.get_minimal_route(matrix)
                # save results of interest
                # in order: iterations Little took on this instance, hardest instance so far, 
                # optimal_tour, optimal_cost, matrix
                range_results[j] = (iterations, hardest, optimal_tour, optimal_cost, matrix)
                
                # hillclimb
                # only considers the current mutation harder if it has MORE OR SAME iterations
                if iterations >= hardest:
                    hardest_matrix = matrix
                    matrix = mutate_matrix(hardest_matrix, rang, False)
                    hardest = iterations
                else:
                    matrix = mutate_matrix(hardest_matrix, rang, False)

                if j > 0 and (j+1) % 100 == 0:
                    # Calculate elapsed time
                    elapsed_time = time.time() - start_time
                    # save to json file
                    save_partial(range_results, citysize, rang, elapsed_time, f"{citysize},{rang}" in _continuations)
                    range_results = {}
    
    elapsed_time = time.time() - start_time
    print(f"Done with cities = {citysize}, randMax = {rang}\nElapsed Time: {elapsed_time:.2f} seconds", flush=True)

experiment(sizes, ranges, args.mutations, continuations)