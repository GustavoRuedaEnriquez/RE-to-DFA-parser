def M0(str):
    replacement  = '(a,b,c,d,e,f,g,h,i,j,k,l,m,n,ñ,o,p,q,r,s,t,u,v,w,x,y,z,á,é,í,ó,ú,'
    replacement += 'A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,Á,É,Í,Ó,Ú,'
    replacement += '1,2,3,4,5,6,7,8,9,0, ,\n)'

    # replacement = getReplacement(alphabet)
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


if __name__ == '__main__':
    alphabet = ['a','b','c']
    str = "ab&+(a,b,&)"
    print("Input: " + str)
    print("Output: " + M0(str))
