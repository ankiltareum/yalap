import argparse
import os.path
import json

debts=dict()

def load(file="debts.json"):
	global debts
	if (os.path.isfile(file)):
		with open(file, "r") as f:
			debts = json.loads(f.read())

def save(file="debts.json"):
	global debts
	with open(file, "w+") as f:
		f.write(json.dumps(debts))

def display():
	global debts
	for k, v in debts.items():
		for l, u in v.items():
			if (u):
				print(k + " -> " + l + ": " + str(u))

def addTicket(buyer, amount, people):
	amountPerPerson = amount/(len(people))
	for person in people:
		if person != buyer:
			if person in debts: # si person a des dettes
				if buyer in debts[person]:	#si person a déjà une dette envers buyer
					debts[person][buyer] += amountPerPerson
				else:
					debts[person][buyer] = amountPerPerson
			else:
				debts[person] = {buyer: amountPerPerson}

			if buyer in debts and person in debts[buyer]: # si buyer a deja une dette envers person
				if debts[buyer][person] >= debts[person][buyer]: # si la dette est plus grande que l'achat
					debts[buyer][person] -= debts[person][buyer]
					debts[person][buyer] = 0
				else: # si la dette est plus petite
					debts[person][buyer] -= debts[buyer][person]
					debts[buyer][person] = 0

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("buyer", type=str, nargs="?", help="The person paying")
	parser.add_argument("amount", type=float, nargs="?", help="The amount payed")
	parser.add_argument("people", type=str, metavar='N', nargs='*', help="People eating")
	parser.add_argument("-i", "--include", help="Count buyer in people", action="store_true")
	args = parser.parse_args()
	
	load()
	if args.buyer and args.amount and args.people:
		people=args.people
		if args.include: 
			people.append(args.buyer)
		addTicket(args.buyer, args.amount, people)
		save()
	elif not args.buyer and not args.amount and not args.people: 
		display()
	else:
		print("Command not recognized")
