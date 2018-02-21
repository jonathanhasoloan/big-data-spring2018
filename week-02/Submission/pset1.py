# A.1 Create a list containing any 4 strings
l_a = ['D','U','S','P']
# A.2 Print the 3rd item in the list
print(l_a[2])
# A.3 Print the 1st and 2nd item
print(l_a[0:2])
# A.4 Add a new string with text “last” to the end of the list
l_a.append('last')
print(l_a)
# A.5 Get the list length and print it
print(len(l_a))
# A.6 Replace the last item in the list with the string “new” and print
l_a=[word.replace('last','new')for word in l_a]
print(l_a)

# ---------------------------------------------------------------------------
# B.1 Convert the list into a normal sentence
sentence_words = ['I', 'am', 'learning', 'Python', 'to', 'munge', 'large', 'datasets', 'and', 'visualize', 'them']
" ".join(sentence_words)
# B.2 Reverse the order of this list
print(list(reversed(sentence_words)))
# B.3 Sort the list using the default sort order
print(list.sort(sentence_words))
print(sentence_words)
# B.4 Perform the same operation using the [`sorted()` function]
print(sorted(sentence_words))
    # The difference between list.sort and sorted is that:
    # list.sort modify the list itself (in-place), so changes can only be seen if we print the list again.
    # While sorted modify the list by creating a new list so the changes are visible as a result.
# B.5 case-insensitive alphabetical sort
print(sorted(sentence_words,key=lambda s: s.lower()))

# ---------------------------------------------------------------------------
# C

low = int(input("Lower-bound integer: ") or 0)
high = int(input("Higher-bound integer: "))

def randomize(low,high):
    from random import randint
    result = randint(low,high)
    assert(0<=result<=high)
    assert(low<=result<=high)

    return result

print(randomize(low,high))

# ---------------------------------------------------------------------------
# D.1

title = input('Booktitle:')
n = input('The position on the list:')

def bestseller(n,title):
    message = f"The number {n} bestseller today is: {title}"
    return message

print(bestseller(n,title))

# ---------------------------------------------------------------------------
# E.1 Password Verification
passw = input('Insert password here:')

spechar = ('!', '?', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=')
def passcheck(password):
    if 8 <= len(passw) <= 14 and sum(c.isdigit() for c in passw)>=2 and sum(c.isupper() for c in passw)>=1 and any (char in spechar for char in pasw):
        message = 'Strong Password'
    else:
        message = 'Error'
    return message

print(passcheck(password))

# ---------------------------------------------------------------------------
# F

num = 5
powr = 3

def exp(num,powr):
  res = 1
  for x in range(powr):
    res=res*num
  return res

print(exp(num,powr))

# ---------------------------------------------------------------------------
# G
A = [1,4,6,9,10,2,7,2,1]

def maxi(list):
    result = A[0]
    for i in range(len(A)-1):
        if A[(i+1)] > result:
            result = A[(i+1)]
    return result

print(maxi(list))
