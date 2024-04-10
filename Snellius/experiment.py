<<<<<<< Updated upstream
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

# Parse arguments
args = parser.parse_args()

# Convert string representations of lists to actual lists
sizes = ast.literal_eval(args.sizes)
ranges = ast.literal_eval(args.ranges)

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

def save_partial(results, citysize, range, time):

    x = 0
    while True:
        file_path = f"results{citysize}_{range}_{x}.json"
        if not os.path.exists(file_path):
            break
        x += 1

    # Dumping the nested_dict to a json file with custom encoding
    with open(file_path, "w") as json_file:
        json.dump(results, json_file, default=custom_encoder)

    print(f"Results saved to JSON file successfully as {file_path}\nElapsed Time: {time:.2f} seconds")


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

def experiment(_cities, _ranges, _mutations):
    for citysize in _cities:
        for rang in _ranges:
            range_results = {}
            hardest = 0

            # Record the start time
            start_time = time.time()
            
            # initialize the matrix with ints, but convert it to a floating-point type to enable np.inf
            matrix = np.random.randint(1,rang,((citysize, citysize))).astype(float)
            for x in range(citysize):
                matrix[x, x] = np.inf
            hardest_matrix = matrix
            
            for j in range(_mutations):
                iterations, optimal_tour, optimal_cost = algorithm.get_minimal_route(matrix)
                # save results of interest
                # in order: iterations Little took on this instance, hardest instance so far, 
                # optimal_tour, optimal_cost, matrix
                range_results[j] = (iterations, hardest, optimal_tour, optimal_cost, matrix)
                
                # hillclimb
                # only considers the current mutation harder if it has MORE iterations
                if iterations > hardest:
                    hardest_matrix = matrix
                    matrix = mutate_matrix(hardest_matrix, rang, False)
                    hardest = iterations
                else:
                    matrix = mutate_matrix(hardest_matrix, rang, False)

                if j > 0 and (j+1) % 100 == 0:
                    # Calculate elapsed time
                    elapsed_time = time.time() - start_time
                    # save to json file
                    save_partial(range_results, citysize, rang, elapsed_time)

=======
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

# Parse arguments
args = parser.parse_args()

# Convert string representations of lists to actual lists
sizes = ast.literal_eval(args.sizes)
ranges = ast.literal_eval(args.ranges)

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

def save_partial(results, citysize, range, time):

    x = 0
    while True:
        file_path = f"results{citysize}_{range}_{x}.json"
        if not os.path.exists(file_path):
            break
        x += 1

    # Dumping the nested_dict to a json file with custom encoding
    with open(file_path, "w") as json_file:
        json.dump(results, json_file, default=custom_encoder)

    print(f"Results saved to JSON file successfully as {file_path}\nElapsed Time: {time:.2f} seconds")


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

def experiment(_cities, _ranges, _mutations):
    for citysize in _cities:
        for rang in _ranges:
            range_results = {}
            hardest = 0

            # Record the start time
            start_time = time.time()
            
            # initialize the matrix with ints, but convert it to a floating-point type to enable np.inf
            matrix = np.random.randint(1,rang,((citysize, citysize))).astype(float)
            for x in range(citysize):
                matrix[x, x] = np.inf
            hardest_matrix = matrix
            
            for j in range(_mutations):
                iterations, optimal_tour, optimal_cost = algorithm.get_minimal_route(matrix)
                # save results of interest
                # in order: iterations Little took on this instance, hardest instance so far, 
                # optimal_tour, optimal_cost, matrix
                range_results[j] = (iterations, hardest, optimal_tour, optimal_cost, matrix)
                
                # hillclimb
                # only considers the current mutation harder if it has MORE iterations
                if iterations > hardest:
                    hardest_matrix = matrix
                    matrix = mutate_matrix(hardest_matrix, rang, False)
                    hardest = iterations
                else:
                    matrix = mutate_matrix(hardest_matrix, rang, False)

                if j > 0 and (j+1) % 100 == 0:
                    # Calculate elapsed time
                    elapsed_time = time.time() - start_time
                    # save to json file
                    save_partial(range_results, citysize, rang, elapsed_time)

>>>>>>> Stashed changes
experiment(sizes, ranges, args.mutations)