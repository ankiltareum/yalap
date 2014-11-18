#!/usr/bin/python3

import argparse
import os.path
import json

debts = dict()
hist = []

class Ticket:
	def __init__(self, buyer, amount, people):
		self.buyer = buyer
		self.amount = amount
		self.people = people


def loadDebts(file = "debts.json"):
	global debts
	if (os.path.isfile(file)):
		with open(file, "r") as f:
			debts = json.loads(f.read())

def saveDebts(file = "debts.json"):
	with open(file, "w+") as f:
		f.write(json.dumps(debts))

def computeTicket(buyer, amount, people):
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

def showDebts():
	for k, v in debts.items():
		for l, u in v.items():
			if (u):
				print(k + " -> " + l + ": " + str(u))

def loadHist(file="history.json"):
	global hist
	if (os.path.isfile(file)):
		with open(file, "r") as f:
			hist = json.loads(f.read())

def saveHist(file="history.json"):
	with open(file, "w") as f:
		f.write(json.dumps(hist))

def showHist():
	for index, item in enumerate(hist):
		people = ""
		for p in item["people"]:
			people += p + ", "
		print(str(index+1) + " | " + item["buyer"] + ": " + str(item["amount"]) + " -> " + people[:-2])

def addTicket(buyer, amount, people):
	global hist
	hist.append(Ticket(buyer, amount, people))


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("command", type=str, help="The command to send")
	parser.add_argument("-b", "--buyer", type=str, help="The person paying")
	parser.add_argument("-a", "--amount", type=float, help="The amount payed")
	parser.add_argument("-p", "--people", type=str, metavar='N', nargs='*', help="People sharing")
	parser.add_argument("-c", "--include", help="Count buyer in people", action="store_true")
	parser.add_argument("-i", "--index", type=int, help="Index of ticket to delete")
	args = parser.parse_args()
	
	loadDebts()
	loadHist()
	if args.command == "add" and args.buyer and args.amount and args.people:
		people=args.people
		if args.include: 
			people.append(args.buyer)
		hist.append({"buyer": args.buyer, "amount": args.amount, "people": args.people})
		computeTicket(args.buyer, args.amount, people)
		saveDebts()
		saveHist()
	elif args.command == "show":
		showDebts()
	elif args.command == "hist":
		showHist()
	elif args.command == "del" and args.index:
		del hist[args.index-1]
		debts = dict()
		for ticket in hist:
			computeTicket(ticket["buyer"], ticket["amount"], ticket["people"])
		saveDebts()
		saveHist()
	else:
		print("Command not recognized")
