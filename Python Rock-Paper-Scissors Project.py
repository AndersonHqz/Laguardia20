#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import random

def input_user_choice():
    choice = input("Enter rock, paper, or scissors: ")
    return choice
    
def input_computer_choice():
    return random.choice(["rock", "paper", "scissors"])

def winner(user, computer):
    if user == computer:
        return "tie game, smh"
    elif (user == "rock" and computer == "scissors") or \
         (user == "scissors" and computer == "paper") or \
         (user == "paper" and computer == "rock"):
        return "you win :D"
    else:
        return "computer wins :("

def play():
    user_choice = input_user_choice()
    computer_choice = input_computer_choice()
    print(f"computer selected: {computer_choice}")
    print(winner(user_choice, computer_choice))
    play_again = input("want to play again? (yes/no): ").lower()
    if play_again == "yes":
        play()

play()

