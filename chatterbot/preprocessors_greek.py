"""
Statement pre-processors for Greek language.
"""
def fix_final_sigma(statement):
    '''
    If there is a word that ends with "σ" it replaces it with "ς".
    '''
    
    data = statement.text.split()
    text = ""
    
    for word in data:
        if word[-1]=="σ":
            word = word[:-1] + "ς" 
        text = text + word + " "
    statement.text = text
    
    return statement
