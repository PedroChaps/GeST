import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def debug(*args):
    DEBUG = 1
    if DEBUG:
        print(*args)

def warn(*args):
    print('\033[93m' + "WARNING: ", *args, '\033[0m')

def error(*args):
    print('\033[91m' + "ERROR: ", *args, '\033[0m')


show_graphs = False
# -------------------------------------------------------


file_to_title = {
    "best_and_average.csv": "Best and Average Values",
    "instr_mix_best_per_gen.csv": "Instructions Best Mix",
    "instr_mix_per_gen.csv": "Instructions Mix",
    "type_mix_best_per_gen.csv": "Types Mix"
}


def process_best_and_average(filepath):

    global show_graphs

    df = pd.read_csv(filepath)
    
    plt.figure(figsize=(10, 6))

    plt.plot(df['generation'], df['best'], label='Best')
    plt.plot(df['generation'], df['average'], label='Average')

    plt.xlabel('Generation')
    plt.ylabel('Value')
    plt.title('Evolution of Best and Average Values Across Generations')
    plt.legend()

    # Set integer ticks for the x-axis
    plt.xticks(df['generation'])

    # Display y-axis values in full format
    plt.ticklabel_format(style='plain', axis='y')

    plt.grid(True)
    
    plt.savefig(filepath.replace(".csv", ".svg"))
    
    if show_graphs:
        plt.show()



def process_instrs_or_types(filepath, file):
    
    global show_graphs
    
    df = pd.read_csv(filepath)

    # Extract the "Generation" column
    generations = df['Generation']
    df = df.drop(columns=['Generation'])

    # Extract initial and final generations
    initial_generation = df.iloc[0]
    final_generation = df.iloc[-1]

    # Create a comparison graph for the initial and final generations
    plt.figure(figsize=(12, 8))
    x = np.arange(len(df.columns))  # the label locations
    width = 0.35  # the width of the bars

    # Plot the initial and final generations
    plt.bar(x - width/2, initial_generation.values, width, label='Initial Generation')
    plt.bar(x + width/2, final_generation.values, width, label='Final Generation', color='orange')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    plt.ylabel('Value')
    plt.xticks(x, df.columns, rotation=90)
    plt.title('Comparison of Initial and Final Generations')
    plt.suptitle(file_to_title[file])
    plt.legend()

    plt.tight_layout()
    plt.savefig(filepath[:-4] + "-bars_cmp.svg")



    # Create a bar graph just with the final generation
    plt.figure(figsize=(12, 8))
    x = np.arange(len(df.columns))  # the label locations
    width = 0.7  # the width of the bars

    # Plot the initial and final generations
    plt.bar(x, final_generation.values, width, label='Final Generation', color='orange')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    plt.ylabel('Value')
    plt.xticks(x, df.columns, rotation=90)
    plt.title('Final Generation')
    plt.suptitle(file_to_title[file])
    plt.legend()

    plt.tight_layout()
    plt.savefig(filepath[:-4] + "-bars_last.svg")



    # Create a line graph showing the evolution of each column across generations
    plt.figure(figsize=(12, 8))
    for column in df.columns:
        plt.plot(generations, df[column], label=column)

    # Add labels and title
    plt.xlabel('Generation')
    plt.ylabel('Value')
    plt.title('Evolution of Operations Across Generations')
    plt.suptitle(file_to_title[file])
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.xticks(rotation=90)
    plt.tight_layout()

    plt.savefig(filepath[:-4] + "-line.svg")
    
    if show_graphs:
        plt.show()



if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        error("Usage: python3 generateGraphFromGeneticResults.py <show_graphs? yes : no> <path>")
        error("Example: python3 generateGraphFromGeneticResults.py yes /path/to/folder")
        sys.exit(1)

    show_graphs = False
    if sys.argv[1] in ("Yes", "yes", "Y", "y", "True", "true", "1"):
        show_graphs = True
        
    # The path to the folder containing the genetic results in .csv files
    path = sys.argv[2]

    for file in os.listdir(path):
        
        if not file.endswith(".csv"):
            error("There is a weird file in the folder: " + file)
            print("Skipping that one...")
        
        print("Processing file: `" + file + "`...")
        full_path = path + "/" + file
        # To make it modular, every .csv file might be processed differently.
        # So, we have a switch case:
        match file:
            case "best_and_average.csv":
                process_best_and_average(full_path)
                
            case "instr_mix_best_per_gen.csv" | "instr_mix_per_gen.csv" | "type_mix_best_per_gen.csv":
                process_instrs_or_types(full_path, file)
                
            case _:
                warn("Unknown processing for the file. Skipping!")
        





