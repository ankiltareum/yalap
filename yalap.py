#!/usr/bin/python3

import argh
import os.path
import json

debts = {}
history = []

def loadDebts(file = "debts.json"):
	global debts
	if (os.path.isfile(file)):
		with open(file, "r") as f:
			debts = json.loads(f.read())

def saveDebts(file = "debts.json"):
	with open(file, "w") as f:
		f.write(json.dumps(debts))

def loadHist(file="history.json"):
	global history
	if (os.path.isfile(file)):
		with open(file, "r") as f:
			history = json.loads(f.read())

def saveHist(file="history.json"):
	with open(file, "w") as f:
		f.write(json.dumps(history))

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

def show():
	for k, v in debts.items():
		for l, u in v.items():
			if (u):
				print(k + " -> " + l + ": " + str(u))

def hist():
	for index, item in enumerate(history):
		people = ""
		for p in item["people"]:
			people += p + ", "
		print(str(index+1) + " | " + item["buyer"] + ": " + str(item["amount"]) + " -> " + people[:-2])

@argh.arg('buyer', type=str, help='The one who payes')
@argh.arg('amount', type=int, help='The amount spent')
@argh.arg('people', type=str, nargs='*', help='The ones who owe money')
def add(buyer, amount, people):
	global history
	history.append({'buyer': buyer, 'amount': amount, 'people': people})
	computeTicket(buyer, amount, people)

@argh.arg('index', type=int, help='ID of ticket to remove (use "hist" command)')
def rm(index):
	global history
	global debts
	del history[args.index-1]
	debts = dict()
	for ticket in history:
		computeTicket(ticket["buyer"], ticket["amount"], ticket["people"])


if __name__ == '__main__':
	loadDebts()
	loadHist()
	parser = argh.ArghParser()
	parser.add_commands([add, show, hist, rm])
	parser.dispatch()
	
	saveDebts()
	saveHist()
