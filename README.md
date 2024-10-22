## BiblioTTS : Text-To-Speech for twitch.tv redemptions

warning : many details of the program is still work-in-progress  

This program is a Text-To-Speech(TTS) program to read user input from reward redemptions in twitch.  
The main goal of this program is to be a free to use and easily customizable alternative TTS for redeems in twitch.tv . One side goal from this program is to be a simple practice material for beginners in programming python.  

Features include customizable profanity filter by editing the custom_profanity_wordlist.txt , customizable limit of text length from user input in redeems. This program only connects to twitch API website for authorization and reading redemption data, and does not connect to any other third party website.

Please install Python 3.x stable version for using this program  

### How to use :
1. Fill the config.ini file with appropriate data
2. Run launch.bat
3. To force stop, press CTRL+C
  
single_modules .py files are just examples on how to use better_profanity and python tts (pyttsx3) libraries.  
To run singular example programs :
1. Run example_launch.bat
2. To change program, open example_launch.bat Using Notepad or similar word edit programs, change the ****.py file name to use another .py file
  
### Credits :
1. Thank you to the authors of all libraries being used in this program
2. custom profanity wordlist is combination from better_profanity v0.7.0 library and https://github.com/surge-ai/profanity/tree/main
3. bibliotaffy for motivating and helping in creation of this program
