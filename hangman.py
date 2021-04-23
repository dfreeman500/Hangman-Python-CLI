import random
from collections import Counter
from collections import defaultdict ### handles error no key present - fills in the value
import time
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
red = "\033[0;31m"
yellow="\033[0;33m"
blue="\033[0;34m"
end="\033[0m"

##
####House Keeping - Run Once ####
## Creates Lists within lists [0] is string/word, [1] is dictionary, [2] is list of lettes, [3] is set of letters
# ##defaultdict is used to fill in key value to handle error

word_list_5000 = defaultdict(list)
word_list_26K = defaultdict(list)
word_list_big = defaultdict(list)
word_list_combined = defaultdict(list)


list_of_filenames = ["5000EnglishWordsFrequency.txt", "26Kwords.txt", "words.txt", "combined.txt"]
print(list_of_filenames)
with open(dir_path+"/5000EnglishWordsFrequency.txt") as wordbook:
    words = (line.rstrip('\n') for line in wordbook)
    print(words)

for x in list_of_filenames:
    with open(dir_path+"/"+x) as wordbook:   #'with' opens file and then closes immediatly after
        words = (line.rstrip('\n') for line in wordbook)
        for word in words:
            if word.isalpha():
                if x == "5000EnglishWordsFrequency.txt":
                    word_list_5000[len(word)].append((word.lower(), dict(enumerate(word.lower())), list(word.lower()), set(list(word.lower()))))
                if x == "26Kwords.txt":
                    word_list_26K[len(word)].append((word.lower(), dict(enumerate(word.lower())), list(word.lower()), set(list(word.lower()))))
                if x == "words.txt":
                    word_list_big[len(word)].append((word.lower(), dict(enumerate(word.lower())), list(word.lower()), set(list(word.lower()))))
                if x == "combined.txt":
                    word_list_combined[len(word)].append((word.lower(), dict(enumerate(word.lower())), list(word.lower()), set(list(word.lower()))))

#print(word_list_combined[5])

### End House Keeping ###
def computer_guess_word (length,partial_word, ):
    already_guessed = []
    filename = "words.txt"  ## This if for debugging purposes
    large_words = word_list_big[length]
    #print(len(large_words), " | ", large_words)

    # if len(large_words) == 0:
    #     large_words =word_list_26K[length]
    #     #print(large_words)
    #     #print("26K list")
    #     filename = "26Kwords.txt"
    #
    # if len(large_words)==0 and filename=="26Kwords.txt":
    #     large_words =word_list_big[length]
    #     #print(large_words)
    #     #print("Big list")
    #     filename = "words.txt"
    #
    if len(large_words)==0 and filename != "words.txt":
        print("going to large words")
        large_words =word_list_big[length]
        filename = "words.txt"

    while True:
        print("this is the filename ", filename)
        list_of_sets_of_letters = []
        print("")
        print("---------------------------------------------------------------")
        print("")

        compare_dict={}
        user_supplied_letters = list(''.join(filter(str.isalpha, partial_word.lower()))) #takes the alpha only items in partial_word and stores it into user supplied letters
        already_guessed_incorrect = set(already_guessed) - set(user_supplied_letters)

        x=0
        for item in partial_word: # iterate through item in partial word that is supplied by the user
            if item.isalpha():  # if the item is alphabetic
                compare_dict[x]=item.lower()    #take it and store it as a value in a dictionary where key, value is index,
            x+=1


        new_word_list = [] #This list has all of the words that are of the correct length and also have the guessed letters in the correct location
        for word in large_words:    #go through all of the words in the large_words list,
            isCandidate = True
            if set(compare_dict.items()) <= set(word[1].items()) and word[3].isdisjoint(already_guessed_incorrect):  # # For each word it takes the 2 dictionaries and if the dictionary of user given index,letters is within the dictionary of the index,letters for the word of the same length it is saved
                for (key, value) in (word[1].items()):
                    if (key, value) not in compare_dict.items() and value in user_supplied_letters:  ### DO i need after the 'and'
                        isCandidate = False
                        break
                if isCandidate:
                    new_word_list.append(word)
                    list_of_sets_of_letters.extend(word[3])  # Gets the set of letters from the word and puts in list_of_letters for word frequency

        ## try sorting counter - don't need .most_common. Can use 'sorted' function
        letter_frequency=Counter(list_of_sets_of_letters).most_common(26) #Gets the  26 most frequent letters (lower case)
        # print("***letter frequency : ", letter_frequency)
        # letter_frequency=Counter(list_of_sets_of_letters) #Gets the  26 most frequent letters (lower case)
        # print("***letter frequency : ", letter_frequency)

        print(len(new_word_list)," words that match criteria in ", filename)
        for x in new_word_list:
            print(x[0], " ", end = '')
        print()

        letter_frequency_just_letters_in_order=[]

        for x in letter_frequency:
            letter_frequency_just_letters_in_order.append(x[0])
        print("letter frequency : ", letter_frequency)

        print("letter frequency just letters in order : ", letter_frequency_just_letters_in_order)

        addon=""
        lastword=""
        if len(new_word_list)==1:
            addon="... because I'm thinking that your word is ..."
            lastword=new_word_list[0][0]

        if large_words == word_list_5000[length] and len(new_word_list)==0:
            large_words = word_list_26K[length]
            filename = "26Kwords.txt"
            continue            #Goes to the top of the While loop
        if large_words == word_list_26K[length] and len(new_word_list)==0:
            large_words = word_list_big[length]
            filename = "words.txt"
            continue            #Goes to the top of the While loop

        if filename == "words.txt" and len(new_word_list)==0:  #asks user to check on inputs - a likely input error was made
            print(red + "Woah, Something doesn't seem right! Please look at the letters I've already guessed and make sure they are in the correct spots." + end)

        #for x in letter_frequency_just_letters_in_order: # original goes through in forward order
        for x in letter_frequency_just_letters_in_order: 
            if x not in compare_dict.values() and x not in already_guessed:
                    print(yellow + "Does your word have the letter: {}? ".format(str(x[0]))+ end)
                    print(" {} {}".format(addon, lastword), " | ", letter_frequency)
                    already_guessed.append(x)
                    break

        print("I have guessed {} times, and {} guesses have been incorrect".format(len(already_guessed),len(already_guessed_incorrect)))
        print("I have already guessed these letters: {},".format(already_guessed))
        if partial_word in lastword:
            win_lose()
        # place_holder="1234567890123456789"
        print("so far you've given me", partial_word)
        int_of_length=int(length)
        print("_"*int_of_length)
        print(compare_dict)

        partial_word = input("Type the word, and use '_'' for any characters unless I have guessed the right one above: ")




######



## This function gets the word for when the human guesses the word

def get_word (min_word_length, max_word_length, hyphen_choice, capital, filename=dir_path+"/words.txt"):
    with open(filename) as wordbook:
        words = (line.rstrip('\n') for line in wordbook)
        large_words = [word for word in words if len(word) >= min_word_length and len(word) <= max_word_length]
    computer_word=random.choice(large_words)
    if hyphen_choice=="no":
        if "-" in computer_word:
            print("There's a hyphen and there is not supposed to be one")
            computer_word=""
            get_word(min_word_length, max_word_length, hyphen_choice, capital, filename=dir_path+"/words.txt")
    if capital =="no":
        if computer_word.isupper():
            print("There was an upper case")
            computer_word = ""
            get_word(min_word_length, max_word_length, hyphen_choice, capital, filename=dir_path+"/words.txt")
    if "'" in computer_word:
        print("there was an invalid character")
        computer_word = ""
        get_word(min_word_length, max_word_length, hyphen_choice, capital, filename=dir_path+"/words.txt")
    print(len(computer_word))
    return computer_word


def draw_board_hangman(computer_word, list_of_guesses):
    guessed_so_far = []
    for x in list(computer_word):
        if x.lower() in list_of_guesses or x == "-":
            print(x + " ", end="")
            guessed_so_far.append(x)
        else:
            print("_" + " ", end="")
            guessed_so_far.append("_")
    if guessed_so_far == list(computer_word):
        win_lose()

def win_lose():
    print(red + """

    The word has been guessed!!!

    """+ end)
    cont_quit = input("'C'ontinue or 'Q'uit? ")
    if cont_quit.upper() == "C":
        start_game()
    elif cont_quit.upper() == "Q":
        quit()
    else:
        win_lose()

def get_min_word_length():
    try:
        min_word_length = int(
            input("What should the minimum length of the word be? (Choose a whole number from 1 to 45"))
    except ValueError:
        get_min_word_length()
    if min_word_length < 0 or min_word_length >= 46:
        print("Over-under")
        min_word_length = ""
        get_min_word_length()
    print(min_word_length)
    return min_word_length

def get_max_word_length():
    try:
        max_word_length = int(
            input("What should the maximum length of the word be? (Choose a whole number from 1 to 45"))
    except ValueError:
        get_max_word_length()
    if max_word_length <= 0 or max_word_length >= 46:
        print("Over-under")
        max_word_length = ""
        get_max_word_length()
    print(max_word_length)
    return max_word_length

def get_proper_name_decision(capital):
    capital = (input("Will you allow the computer to choose a word with a capital letter in it? 'Y' or 'N': "))
    if capital.upper() == "Y":
        capital = "yes"
    elif capital.upper() == "N":
        capital = "no"
    else:
        get_proper_name_decision(capital)
    return capital

def get_hyphen_choice(hyphen_choice):
    hyphen_choice = input(
        "There won't be any words with spaces, but can the computer choose a word with a hyphen? 'Y' or 'N'")
    if hyphen_choice.upper() == "Y":
        hyphen_choice = "yes"
    elif hyphen_choice.upper() == "N":
        hyphen_choice = "no"
    else:
        get_hyphen_choice(hyphen_choice)
    return hyphen_choice

def human_guess(min_word_length, max_word_length, capital, hyphen_choice):
    print("You are the Guesser. First, let's have you set the parameters for a word that you will guess.")
    min_word_length = get_min_word_length()
    max_word_length = get_max_word_length()
    capital = get_proper_name_decision(capital)
    hyphen_choice = get_hyphen_choice(hyphen_choice)
    computer_word = get_word(min_word_length, max_word_length, capital, hyphen_choice)
    # print(computer_word)
    word_length = len(computer_word)
    print("Your word has {} spaces in it".format(word_length))
    print("_" * word_length)
    list_of_guesses = []

    while True:
        print("""

        """)

        # if guess in set of already guessed - print that it was already guessed
        print("You've guessed {} times so far.".format(len(list_of_guesses)))
        print("You've guessed these items so far: {}".format(list_of_guesses))
        list_of_guesses.append(input("Guess a letter: "))
        draw_board_hangman(computer_word, list_of_guesses)

    quit()


def computer_guess():
    print("""

    OK, I am the world's greatest guesser of word's. Pick a word - any word.

Write your word out on a peice of paper so I CAN'T see it (I'm not a cheater - I'm just really good).

Then count how many characters there are. I'm counting on you to be honest.

    """)

    how_many_spaces = int(input("How many characters are there?"))

    underscores = "_" * how_many_spaces
    while True:
        computer_guess_word(how_many_spaces, underscores)
        print("The def_computer_guess is actually running")

def start_game():
    min_word_length=0
    max_word_length=45
    capital=""
    hyphen_choice=""
    guess_vs_choose=input(("Do you want to 'G'euss the word or 'C'hoose the word? 'G' or 'C': "))
    if guess_vs_choose.upper() =='G':
        human_guess(min_word_length, max_word_length, capital, hyphen_choice)
    if guess_vs_choose.upper() =='C':
        computer_guess()
    else:
        start_game()

print(red + "Well aren't you lucky? You are about to play the most amazing game of Hangman...ever."+ end)
start_game()