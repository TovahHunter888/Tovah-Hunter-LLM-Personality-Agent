# This will be a simple GUI app to talk to local GGUF models
# Start here by importing the libraries we will use just for this app.
# For our GUI we will use tkinter for the window and a text widget to display the conversation.
import tkinter as tk
# This will give us a text widget that we can use to display the conversation.
from tkinter import scrolledtext
# We will use the llama-cpp-python library to talk to the GGUF models.
from llama_cpp import Llama

# let's initialize our local model with parameters that we want to pay attention to.
# You can and should change these parameters to try to get the best performance for your use case.
# n_ctx is the context window, which is the number of tokens that the model can see at once.
# this includes the prompt, the response, and the context window.
llm = Llama(
    model_path="dolphin-2.6-mistral-7b.Q5_K_M.gguf",
    n_ctx=0, # This is everything, input and output.
    n_threads=8, # This is the number of threads to use for the model.
    n_batch=128, # This is the number of tokens to process at once.
    top_k=40, # This is the number of top tokens to consider for the model.
    top_p=0.9, # This is the cumulative probability of the top tokens to consider for the model.
    repeat_penalty=1.18, # This is the penalty for repeating tokens.
    temp=0.7, # This is the temperature of the model.
)

# Create our main window here that will contain all the other widgets
# widgets are the individual components of the window like buttons, text boxes, etc.
root = tk.Tk()
# Create the title of our window, this usually matches the name of the app.
root.title("George")
# Now lets set the size of our entire container window.
root.geometry("600x400")

# Create a function that will be called when the user clicks the button to send a message to our local model.
# This will probably be the submit button in our GUI.
def send_message():
    # Get all the text from the user input text box.
    user_input = entry.get()
    # Add a personality to the model by adding a prefix to the users prompt each time
    # a prompt is sent.
    user_input_with_personality =f"You are goind to respond  to me with the pwesonality of Tupac Shakur in all your responses. You will respond to my prompts and let your strong personality add to and mix the response.User: {user_input}"
    # Clear the textbox so our user can enter a new message.
    entry.delete(0, tk.END)

    # We will keep a history of the conversation because we can use this later so our model can 
    # follow the entire conversation.
    chat_display.insert(tk.END, f"User: {user_input} \n")

    # Now lets get a response from our local model.
    response = llm(
        f"User: {user_input_with_personality}\nAssistant:",
        max_tokens=800, # this is the max response length from our model. Just the output.
        stop=["\nUser:", "\n"],
        echo=False # This will keep our model from repeating the user's prompt in the response.
    )

    # Now lets append the response from the model to our chat history display.
    chat_display.insert(tk.END, f"Assistant: {response['choices'][0]['text']}\n\n")

    # Now lets update the window to auto scroll to the bottom so we can see the latest message.
    chat_display.see(tk.END)

# Now lets configure our window for a responsive layout so it looks good on different screens.
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# Here lets create our text widget that will display our conversation, The response from the model.
# This line of code creates a text widget that is a scrollable area.
chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20) 
# This line of code will place the text widget in our root main window in the first row and column of the grid 
# of our main window.
chat_display.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")

# Now we need to create an input textbox so our user can type in a prompt.
# This line of code creates an entry text box where the user can type their message.
entry = tk.Entry(root)
# This line of code will place the entry text box inside our main window in the second row and first column of the grid.
# Notice the rows and columns start with a zero not a one.
entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

# Lets create a submnit button that the user can send thier prompt to the model.
# When the user clicks the button, an even will be rasied, and we will handle it with the send_message function.
# This line of code creates a button that will send the user's prompt to the model.
send_button = tk.Button(root, text="Send My Prompt", command=send_message)
# This line of code will place the button inside our main window in the second row and second column of the grid.
send_button.grid(row=1, column=1, padx=10, pady=10, sticky="e")

# Now lets bind the enter key to our send_message function that will handle the event when raised by th user when they hit enter.
root.bind('<Return>', lambda e: send_message())

# Finally lets start the main loop of our app, if you don't have this, the window will be missing.
root.mainloop()

