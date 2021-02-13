"""
Author: Cristina Mata, February 12, 2021

This script uses web-scraped info to rate a list of ingredients.

"""
import numpy as np
import pandas as pd

def get_rating(info, ingredient):
	"""
	@param info (pandas DataFrame): contains ingredient name, rating, description, and categories
	@param ingredient (string): the name of the ingredient to query
	@return rating (int): ingredient rating, where poor = 0, average = 1, good = 2 and best = 4
	"""
	if len(info.loc[info['name'] == ingredient]["rating"]) > 0:
		rating = info.loc[info['name'] == ingredient]["rating"]
	elif len(info.loc[info['name'] == ingredient.lower()]["rating"]) > 0:
		rating = info.loc[info['name'] == ingredient.lower()]["rating"]
	else:
		print("Could not find ", ingredient, " in database.")
		rating = -1
	
	if type(rating) == int:
		rate_txt = None
	else:
		rate_txt = rating.tolist()[0]

	if rate_txt == "Poor":
		rating_int = 0
	elif rate_txt == "Average":
		rating_int = 1
	elif rate_txt == "Good":
		rating_int = 2
	elif rate_txt == "Best":
		rating_int = 3
	else:
		rating_int = -1
	return rating_int

if __name__ == "__main__":
	# The name of the json ingredients file
	ingredients_json_path = "all_ingredients.json"

	# Text of ingredients
	ing_dirty = "Water; Cyclopentasiloxane; Zinc Oxide; Propanediol; Titanium Dioxide; Butylene Glycol; Dicaprylate/Dicaprate; Lauryl Polyglyceryl-3 Polydimethylsiloxyethyl; Dimethicone; Methyl Methacrylate Crosspolymer; Butyloctyl Salicylate; Caprylyl Methicone; Citrus Aurantium Dulcis (Orange) Oil; Citrus Nobilis (Mandarin Orange) Peel Oil; Litsea Cubeba Fruit Oil; 1,2-Hexanediol; Disteardimonium Hectorite; Magnesium Sulfate; Stearic Acid; Aluminum Hydroxide; Polyglyceryl-3 Polydimethylsiloxyethyl Dimethicone; Triethoxycaprylylsilane; Sorbitan Caprylate; Glyceryl Caprylate; Ethylhexylglycerin; Tocopherol"

	# Clean the ingredients text into a list of ingredients
	ing_list_clean = ing_dirty.split(';')
	print(ing_list_clean)

	# Read ingredients info
	info = pd.read_json(ingredients_json_path)

	# Get rating for each ingredients
	ratings = [get_rating(info, ingredient.strip()) for ingredient in ing_list_clean]

	# Calculate average ingredient rating
	average_rating = np.mean([r for r in ratings if r > 0])
	print("Average rating of first product ", average_rating)

