"""
Author: Cristina Mata, February 7, 2021

This script scrapes the ingredient dictionary at paulaschoice.com for information about ingredients found in skincare products.

"""
import requests
import requests_cache
import bs4
from bs4 import BeautifulSoup
import pandas as pd


if __name__ == "__main__":
	page = requests.get("https://www.paulaschoice.com/ingredient-dictionary")
	
	# If status code starts with 2 then it loaded successfully.
	# If it starts with 4 or 5 then there was an error.
	assert page.status_code == 200

	soup = BeautifulSoup(page.content, 'html.parser')

	# Get a set of all ingredient info
	ingredient_results = soup.find_all("tr", "ingredient-result")

	# There are four attributes we want to extract for each ingredient
	# Ingredient name
	# Ingredient description
	# Ingredient categories
	# Ingredient rating
	# We'll put these in a Pandas dataframe
	names_list, description_list, categories_list, rating_list = [], [], [], []
	for ingredient in ingredient_results:
		name = ingredient.find(class_="ingredient-name").get_text().strip()
		print(name)
		rating = ingredient.find(class_="ingredient-rating").get_text().strip()
		categories = ingredient.find(class_="ingredient-categories").get_text().strip().replace('\n', '').split(':')[1]

		# We need to scrape another page to get the full description
		description_page = requests.get(ingredient.find(class_="ingredient-name").a.get('href'))
		description_soup = BeautifulSoup(description_page.content, 'html.parser')
		# Case: No description provided
		if len(description_soup.find_all("div", "upper-body")) == 0:
			description = ""
		else:
			# Case: Several sections of information in description – we just want the first paragraph
			try:
				description = description_soup.find_all("div", "upper-body")[0].p.get_text().strip()
			# Case: Only one section of info
			except:
				description = description_soup.find_all("div", "upper-body")[0].get_text().strip()

		names_list.append(name)
		description_list.append(description)
		categories_list.append(categories)
		rating_list.append(rating)

	# Create the DataFrame and save it for analysis
	all_ingredients = pd.DataFrame({
	    "name": names_list,
	    "description": description_list,
	    "categories": categories_list,
	    "rating": rating_list
	})

	all_ingredients.to_json("all_ingredients.json")

	