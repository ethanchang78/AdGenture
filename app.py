import tkinter as tk
from novelizer import Novelizer
import torch
from transformers import GPT2LMHeadModel, BertTokenizer, GPT2Tokenizer
from functools import partial
import warnings
import logging
from transformers import logging as hf_logging
# from inference import 

# Suppress non-essential python warnings
warnings.filterwarnings("ignore")
hf_logging.set_verbosity_error()
logging.getLogger().setLevel(logging.ERROR)

# Get Trained Model for Generating the Situations
novelizer = Novelizer(generator=GPT2LMHeadModel.from_pretrained('gpt2'), device='cpu')
novelizer.load_state_dict(torch.load('weights/model5.pth', map_location=torch.device('cpu')))
# Get Trained Model for Finishing the Story
concluder = Novelizer(generator=GPT2LMHeadModel.from_pretrained('gpt2'), device='cpu')
concluder.load_state_dict(torch.load('weights/Conclusionizer3.pth', map_location=torch.device('cpu')))

# Constants
NUM_STEPS = 5

# Count number of game steps
step_num = 0

def generate_intro(prompt):
    # Destroy start button once clicked
    start_button.destroy()

    # Create two new buttons labeled "Option A" and "Option B"
    option_a_button.pack(pady=10)
    option_b_button.pack(pady=10)

    # Generate the next step
    generate(prompt)

def generate_ending(prompt):
    # Destroy remaining buttons
    option_a_button.destroy()
    option_b_button.destroy()
    optionA_label.config(text='')
    optionB_label.config(text='')

    # Generate and display ending
    ending = concluder.generate_story_intro(story_type=prompt)[-1]
    ending = ending[:ending.rfind('.')+2]
    display_label.config(text=ending)

def generate(prompt):
    global step_num
    if step_num>=NUM_STEPS:
        generate_ending(prompt)
        return
    else:
        step_num += 1
    intro_text = novelizer.generate_story_intro(story_type=prompt)[-1]
    # End text on a period
    intro_text = intro_text[:intro_text.rfind('.')+2]
    show_text = intro_text + " What should happen next? "
    # print(text)
    # Set the text to display only the first 50 characters
    display_label.config(text=show_text)

    last_sentence = intro_text[:-2]
    last_sentence = last_sentence[last_sentence.rfind('. '):]

    # Generate options
    optionA, optionB = generate_options(last_sentence)
    if optionA[-1] == '.':
        showA = "Option A: " + optionA + ".."
    else:
        showA = "Option A: " + optionA + "..."
    if optionB[-1] == '.':
        showB = "Option B: " + optionB + ".."
    else:
        showB = "Option B: " + optionB + "..."
    optionA_label.config(text=showA)
    optionB_label.config(text=showB)

    # Update the string options
    option_a_button.configure(command=partial(generate, optionA))
    option_b_button.configure(command=partial(generate, optionB))

def generate_options(input_text):
    optionA = novelizer.generate_story_intro(input_text, num_return_sequences=1)[0]
    optionA = optionA[optionA.rfind('. ')+2:]
    optionB = novelizer.generate_story_intro(input_text, num_return_sequences=2)[0]
    optionB = optionB[optionB.rfind('. ')+2:]
    return optionA, optionB

# Initialize the main window
root = tk.Tk()
root.title("AdGenture: A Generative Adventure Game")
root.geometry("400x700")  # Set initial window size (width x height)

# Create the "Start" button and assign the callback function
intro_prompt = 'A world of dragons and monsters'
start_button = tk.Button(root, text="Start", command=partial(generate_intro, intro_prompt))
start_button.pack(pady=20)

# Create two new buttons labeled "Option A" and "Option B"
option_a_button = tk.Button(root, text="Option A", command=None)
option_b_button = tk.Button(root, text="Option B", command=None)

# Create a Label to display the info text
display_label = tk.Label(root, text="", wraplength=300)
display_label.pack(pady=10)

# Create a Label to display the options text
optionA_label = tk.Label(root, text="", wraplength=300)
optionA_label.pack(pady=40)
optionB_label = tk.Label(root, text="", wraplength=300)
optionB_label.pack(pady=50)

# Start the Tkinter main event loop
root.mainloop()
