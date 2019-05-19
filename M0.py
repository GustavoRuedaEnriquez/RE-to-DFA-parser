def replaceWildcard(str,alphabet):
    replacement = getReplacement(alphabet)
    new_str = str.replace('&',replacement)
    return new_str

def getReplacement(alphabet):
    result_str = "("
    i = 0
    j = len(alphabet) - 1
    for alpha in alphabet:
        result_str += alpha
        if(i < j):
            i += 1
            result_str += ","
    result_str += ")"
    return result_str

alphabet = ['a','b','c']
str = "ab&+(a,b,&)"
print("Input: " + str)
print("Output: " + replaceWildcard(str,alphabet))
