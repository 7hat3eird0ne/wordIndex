import json

def jsoncheck(file: str)-> bool:
    try:
        with open(file, encoding = 'UTF-8') as openedFile:
            pythJson = json.load(openedFile)
        if type(pythJson) != dict:
            raise
        elif type(pythJson['order']) != list:
            raise
        elif type(pythJson['reverseAppend']) != bool:
            raise
        elif pythJson['minLen'] < 0:
            raise
        elif abs(pythJson['caseSensitive']) > 1 :
            raise
        else:
            for i in range(len(pythJson['order'])):
                if type(pythJson['order'][i]) != str:
                    raise
                if len(pythJson['order'][i]) != 1:
                    raise
    except:
        print(f'{file} either doesn\'t exist or has invalid json')
        return False
    else:
        return True

def forward(string: str, charaSetFile: str) -> int:
    if not jsoncheck(charaSetFile):
        print(f'Error: {charaSetFile} is invalid')
    else:
        with open(charaSetFile, encoding = 'UTF-8') as file:
            characterSet = json.load(file)
        try:
            if not characterSet['caseSensitive']:
                for i in range(len(characterSet['order'])):
                    characterSet['order'][i] = characterSet['order'][i].lower()
                string = string.lower()
            excludeLenAddition = len(characterSet['order'])**characterSet['minLen'] - (len(characterSet['order'])-2)*(len(characterSet['order'])**characterSet['minLen']-1)/(len(characterSet['order'])-1) - 1
            posi = 0
            wordRepres = 0
            if characterSet['reverseAppend']:
                iRange = range(len(string) - 1, -1, -1)
            else:
                iRange = range(len(string))
            for i in iRange:
                wordRepres += characterSet['order'].index(string[i])*(len(characterSet['order'])**posi)
                posi += 1
            result = int(wordRepres + len(characterSet['order'])**posi - (len(characterSet['order'])-2)*(len(characterSet['order'])**posi-1)/(len(characterSet['order'])-1) - 1 - excludeLenAddition)
            if result < 0:
                return -1
            else:
                return result
        except:
            return -1

def backward(num: int, charaSetFile: str) -> str:
    if not jsoncheck(charaSetFile):
        print(f'Error: {charaSetFile} is invalid')
    else:
        with open(charaSetFile, encoding = 'UTF-8') as file:
            characterSet = json.load(file)
        try:
            if num < 0:
                print('changed the sign of target index')
                abs(num)
            if not characterSet['caseSensitive']:
                for i in range(len(characterSet['order'])):
                    characterSet['order'][i] = characterSet['order'][i].lower()
                string = string.lower()
            excludeLenAddition = len(characterSet['order'])**characterSet['minLen'] - (len(characterSet['order'])-2)*(len(characterSet['order'])**characterSet['minLen']-1)/(len(characterSet['order'])-1) - 1
            length = 0
            while int(len(characterSet['order'])**(length + 1) - (len(characterSet['order'])-2)*(len(characterSet['order'])**(length + 1)-1)/(len(characterSet['order'])-1) - 1 - excludeLenAddition) <= num:
                length += 1
            finalNum = num - int(len(characterSet['order'])**length - (len(characterSet['order'])-2)*(len(characterSet['order'])**length-1)/(len(characterSet['order'])-1) - 1 - excludeLenAddition)
            result = ''
            for i in range(length):
                if characterSet['reverseAppend']:
                    result = characterSet['order'][int(finalNum % len(characterSet['order']))] + result
                else:
                    result = result + characterSet['order'][int(finalNum % len(characterSet['order']))]
                finalNum = finalNum // len(characterSet['order'])
            return result
        except:
            return -1



def main():
    while True:
        targetFile = input('Enter the file you want to use (leave blank for default) - ')
        if targetFile == '':
            targetFile = 'printableCharacters.json'
        if jsoncheck(targetFile):
            print(f'The file {targetFile} has been found and used')
            break
        else:
            print(f'Error: {targetFile} is invalid, please enter a different file name (maybe a typo?)')
    while True:
        try:
            continueLoop = input('-- ')
            if len(continueLoop) != 0:
                if continueLoop[0] != '!':
                    continueLoop = '!' + continueLoop[0:-1] + continueLoop[-1]

        except EOFError:
            print('Ending the loop')
            return

        if continueLoop == '!help':
            print('all currently supported commands:')
            print('!help')
            print('!translate')
            print('!refile')
            print('!jsoninfo')
            print('!eof')
            print()
            print('to be added:')
            print('wordindexinfo')
            print('jsoncreateinfo')

        elif continueLoop == '!translate':
            translationToggle = input('Write "f" to translate forward, "b" to toggle translation backwards - ')
            if translationToggle == 'f':
                stringInput = input('Enter the input string - ')
                resultIndex = str(forward(stringInput, targetFile))
                print('The string "' + stringInput + '" has an index ' + resultIndex + "# according to " + targetFile)
            elif translationToggle == 'b':
                indexInput = int(input('Enter the input index -. '))
                print('The string with index ' + str(indexInput) + '# is "' + (backward(indexInput, targetFile)) + '" according to ' + targetFile)
            else:
                print('Skipping the translation due to invalid input')

        elif continueLoop == '!jsoninfo':
            with open(targetFile, encoding = 'UTF-8') as gainFile:
                fileJson = json.load(gainFile)
            print(json.dumps(fileJson)[0:-1] + ', "charaNo": ' + str(len(fileJson['order'])) + '}')

        elif continueLoop == '!refile':
            while True:
                targetFile = input('Enter the file you want to use (leave blank for default) -')
                if targetFile == '':
                    targetFile = 'printableCharacters.json'
                if jsoncheck(targetFile):
                    print(f'The file {targetFile} has been found and set')
                    break
                else:
                    print(f'Error: {targetFile} is invalid, please enter a different file name (maybe a typo?)')

        elif continueLoop == '!eof':
            print('Do either CTRL + Z (windows) or CTRL + D, depending on where you are running this code')

        else:
            print('do !help')
        
        print()

if __name__ == '__main__':
    main()