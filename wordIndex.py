#imports the json module
import json

def jsoncheck(fileName)-> bool:
    try:
        #open the file
        with open(fileName, encoding = 'UTF-8') as file:
            characterSet = json.load(file)

        #check if certain keys refference to correct types
        if type(characterSet) != dict:
            raise
        elif type(characterSet['order']) != list:
            raise
        elif type(characterSet['reverseAppend']) != bool:
            raise
        elif characterSet['minLen'] < 0:
            raise
        elif abs(characterSet['caseSensitive']) > 1 :
            raise

        #check if insides of 'order' have type string and are exactly one character long    
        else:
            for i in range(len(characterSet['order'])):
                if type(characterSet['order'][i]) != str:
                    raise
                if len(characterSet['order'][i]) != 1:
                    raise

    #returning boolean
    except:
        print(f'{fileName} either doesn\'t exist or has invalid json')
        return False
    else:
        return True


def forward(string: str, fileName: str) -> int:
    #checks if file is valid
    if not jsoncheck(fileName):
        print(f'Error: {fileName} is invalid')

    else:
        #opens the json file and converts it to dictionary
        with open(fileName, encoding = 'UTF-8') as file:
            characterSet = json.load(file)
        
        try:
            #if the json isnt case sensitive, it turns everythings into lowercase
            if not characterSet['caseSensitive']:
                for i in range(len(characterSet['order'])):
                    characterSet['order'][i] = characterSet['order'][i].lower()
                string = string.lower()
            
            #calculates the smallest index of the minimal length
            excludeLenAddition = len(characterSet['order'])**characterSet['minLen'] - (len(characterSet['order'])-2)*(len(characterSet['order'])**characterSet['minLen']-1)/(len(characterSet['order'])-1) - 1
            
            #sets variables
            posi = 0
            numRepres = 0

            #changes the appending system if the json appends in reverse
            if characterSet['reverseAppend']:
                iRange = range(len(string) - 1, -1, -1)
            else:
                iRange = range(len(string))

            #starts making number represenation of the string
            for i in iRange:
                numRepres += characterSet['order'].index(string[i])*(len(characterSet['order'])**posi)
                posi += 1

            #adds a magic formula to the number representation and subtracts the smallest index of minimal length
            result = int(numRepres + len(characterSet['order'])**posi - (len(characterSet['order'])-2)*(len(characterSet['order'])**posi-1)/(len(characterSet['order'])-1) - 1 - excludeLenAddition)

            #checks if the result is negative, in that case it raises an error
            if result < 0:
                raise
            else:
                return result
            
        #error returns -1
        except:
            return -1


def backward(num: int, fileName: str) -> str:
    #checks if json file is valid
    if not jsoncheck(fileName):
        print(f'Error: {fileName} is invalid')

    else:
        #opens the json file and converts it to dictionary
        with open(fileName, encoding = 'UTF-8') as file:
            characterSet = json.load(file)

        try:
            #if the index is negative than it raises an error
            if num < 0:
                raise

            #converts everything to lowercase if json isnt case sensitive
            if not characterSet['caseSensitive']:
                for i in range(len(characterSet['order'])):
                    characterSet['order'][i] = characterSet['order'][i].lower()

            #calculates the smallest index of minimal length
            excludeLenAddition = len(characterSet['order'])**characterSet['minLen'] - (len(characterSet['order'])-2)*(len(characterSet['order'])**characterSet['minLen']-1)/(len(characterSet['order'])-1) - 1

            #looks for the length of the string
            length = 0
            while int(len(characterSet['order'])**(length + 1) - (len(characterSet['order'])-2)*(len(characterSet['order'])**(length + 1)-1)/(len(characterSet['order'])-1) - 1 - excludeLenAddition) <= num:
                length += 1

            #generates the number represenation of the string
            numRepres = num - int(len(characterSet['order'])**length - (len(characterSet['order'])-2)*(len(characterSet['order'])**length-1)/(len(characterSet['order'])-1) - 1 - excludeLenAddition)

            #converts the number represantion from decimal to its original base, and then converts to the number and appends it
            result = ''
            for i in range(length):
                if characterSet['reverseAppend']:
                    result = characterSet['order'][int(numRepres % len(characterSet['order']))] + result
                else:
                    result = result + characterSet['order'][int(numRepres % len(characterSet['order']))]
                numRepres = numRepres // len(characterSet['order'])
            return result
        
        #error returns -1, but in a string form
        except:
            return '-1'



def main(targetFile: str = '', banRefile: bool = False) -> None:
    try:
        #if targetfile was set, then it skips inital targetFile entering an
        if targetFile != '':

            #checks if the entered file is valid
            if jsoncheck(targetFile):
                print(f'The file {targetFile} has been found and used')
            else:
                return
        else:
            #if changing the file is banned, it will use the default one or one inputed in the targetFile argument
            if banRefile:
                if targetFile == '':
                    targetFile = 'printableCharacters.json'

                #checks if the entered file is valid
                if jsoncheck(targetFile):
                    print(f'The file {targetFile} has been found and used')
                else:
                    return
                
            else:
                #asks user which characterset file they want to use
                while True:
                    targetFile = input('Enter the file you want to use (leave blank for default) - ')
                    if targetFile == '':
                        targetFile = 'printableCharacters.json'

                    #checks if the entered file is valid
                    if jsoncheck(targetFile):
                        print(f'The file {targetFile} has been found and used')
                        break
                    else:
                        print(f'Error: {targetFile} is invalid, please enter a different file name (maybe a typo?)')
        
        while True:
            #asks for a command input, and it auto corrects the command to contain '!' if user forgot about it
            consoleInput = input('-- ')
            if len(consoleInput) != 0:
                if consoleInput[0] != '!':
                    consoleInput = '!' + consoleInput[0:-1] + consoleInput[-1]

            #runs !help command        
            if consoleInput == '!help':
                print('all currently supported commands:')
                print('!help')
                print('!translate')
                if banRefile:
                    print('!refile (not supported in current situation)')
                else:
                    print('!refile')
                print('!jsoninfo')
                print('!eof')
                print()
                print('to be added:')
                print('wordindexinfo')
                print('jsoncreateinfo')

            #runs !translate command
            elif consoleInput == '!translate':

                #asks user if they want to translate forward or backward
                translationToggle = input('Write "f" to translate forward, "b" to toggle translation backwards - ')
                
                #forward path
                if translationToggle == 'f':
                    stringInput = input('Enter the input string - ')
                    resultIndex = str(forward(stringInput, targetFile))
                    print('The string "' + stringInput + '" has an index ' + resultIndex + "# according to " + targetFile)
                
                #backward path
                elif translationToggle == 'b':
                    try:
                        indexInput = int(input('Enter the input index -. '))
                        print('The string with index ' + str(indexInput) + '# is "' + (backward(indexInput, targetFile)) + '" according to ' + targetFile)
                    except:
                        print('error occured')

                else:
                    print('Skipping the translation due to invalid input')

            #runs !jsoninfo command
            elif consoleInput == '!jsoninfo':

                #opens the json and converts it to dictionary
                with open(targetFile, encoding = 'UTF-8') as file:
                    characterSet = json.load(file)

                #prints out the json info
                print(json.dumps(characterSet)[0:-1] + ', "charaNo": ' + str(len(characterSet['order'])) + '}')

            #runs !refile command
            elif consoleInput == '!refile':
                if banRefile:
                    print('Sorry, the !refile command is not being supported in current situation')
                else:
                    #runs the loop which gets the file from user
                    while True:
                        targetFile = input('Enter the file you want to use (leave blank for default) -')
                        if targetFile == '':
                            targetFile = 'printableCharacters.json'
                        
                        #checks if the file is valid
                        if jsoncheck(targetFile):
                            print(f'The file {targetFile} has been found and set')
                            break
                        else:
                            print(f'Error: {targetFile} is invalid, please enter a different file name (maybe a typo?)')

            #runs EOF command
            elif consoleInput == '!eof':
                print('Do either CTRL + Z (windows) or CTRL + D, depending on where you are running this code')

            #if user enters invalid command, then it prints out advice
            else:
                print('!help')
            print()

    #checks for EOF
    except EOFError:
        print('!!!')
        return

#runs the main() command if the file isnt ran as a module
if __name__ == '__main__':
    main()