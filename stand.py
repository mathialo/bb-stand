#! /usr/local/python3

def read_properties():
	user, password = None, None

	try:
		infile = open("email.properties", "r")

		for line in infile:
			key, val = line.split("=")
			key, val = key.strip(), val.strip()

			if key == "user":
				user = val
			elif key == "pass"
				password = val

	except FileNotFoundError:
		infile = open("email.properties", "w")
		infile.write("user=")
		infile.write("pass=")
		print("email.properties was created, please provide login info for UiO user")

	infile.close()

	return user, password


