   # mettre en place un password validator :
      # creer une fonction qui va nous permettre d'indiquer a l'utilisateur si son mot de passe est securise
      # 3 criteres : minimum 8 caracteres, des chiffres et des lettres, au moins une majuscule
import re
# regular expression (regex), c'est une expression qui permet de faire une recherche a l'interieur d'une string

def validate_password(password):
#cette fonction doit nous renvoyer True ou False
	valid = True
	if len(password) < 8:
		valid = False
	# print("Make sure your password is at lest 8 letters")
	elif re.search('[0-9]',password) is None:
		valid = False
	# print("Make sure your password has a number in it")
	elif re.search('[A-Z]',password) is None:
		valid = False
	# print("soit sur que ce sera en majuscule")
	elif re.search('[a-z]',password) is None:
		valid = False    

	return valid
	# print("Your password seems fine")