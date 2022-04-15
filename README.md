# FeistelCipher
## Description: 
    Feistel Cipher encoder and decoder. A filepath for the text and string for the key must be specified, along with whether the user wishes an encoded or decoded output and the output filepath. This Feistel algorithm runs with F(R,K) function being the xor of the right side of the input and key for that round. The keys are derived by creating sha256 functions of the prior key, with the first key being a sha256 hash of the inputted key. This way all keys are different.

## Design Decisions:
    In order to make all the keys unique, each key is a sha256 hash derived from the previous key. These 4 keys are then repeated or clipped to match the same length of the binary of half the input string. The function used is f(right, key) = xor(right, key), which I found to be effective in encrypting the text without making it too complicated. When reading or writing to the file, the open() method must contain the parameter "newline=''", as this will ensure python does not automatically translate newline characters (\r, \n) to os.newline, which will end up in python reading it as \n when it is next inputted. This can cause incorrect characters appearing when decoded, as anything translated to "\r" is lost as "\n". I had to have the output of the encoding write to a text file as if the encoded message was printed on terminal to be copy and pasted, it could cause errors depending on the terminal's encoding method. 

## How to use:
    The command to call this script should look like this:
        python FeistelCipher.py InputFilepath Key Codetype OutputFilepath

    InputFilepath = This should be the filepath of a textfile containing text you wish to encode or decode

    Key = This should contained a string of text to be used as the key for encoding or decoding

    Codetype = If this is "encode" to encode, and "decode" to decode. Will print an error message and end the program if anything else is inputted in this field.

    OutputFilepath = This should be the filepath with the filename to which the script should write the encoded/decoded text. NOTE: It was create the respective file if it does not exist. NOTE: If the file does already exist, the contents will be overwritten with the output of this script.

## Example test:
    duck.txt contained the full plaintext lyrics to "The Duck Song".

###    To encode:
        Input:
            python .\FeistalCipher.py .\duck.txt apple encode .\ducked.txt
    
        Output:
            Output written to specified file. Please use this file to decode
        
        ducked.txt now contains the encoded text for duck.txt. Here is the first line:
            Jf!rfoegn.*=8f-,te.g=&9mx*{m3xfk%k?i`6U`l.&>ch85&;(0ai*sY})b|aa!a+flq%b~sZl_}Y;*}h/9`6dr0-&"+>TbPw\s&t{0'v?+r2z5Jado,!2yr<i[J

###    To decode:
        Input:
            python .\FeistalCipher.py ducked.txt apple decode ducker.txt 

        Output:
            Decoded text written to specified file

        ducker.txt now contains the decoded text for ducked.txt. It matches duck.txt. Here are the first 5 lines:
            A duck walked up to a lemonade stand
            And he said to the man runnin' the stand
            "Hey! [(bam bam bam)] Got any grapes?"
            The man said: "No, we just sell lemonade
            But it's cold, and it's fresh, and it's all home-made!

    These text files have been included for your reference.
