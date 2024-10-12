from better_profanity import profanity

if __name__ == "__main__":
    profanity.load_censor_words() # load default list of words
    # profanity.load_censor_words_from_file('updated_profanity_wordlist.txt')

    text = "You p1ec3 of sh1t."
    censored_text = profanity.censor(text)
    print(censored_text)
    # You **** of ****.
