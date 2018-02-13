import json


class Ingredient:
    """ Ingredient class contains ingredient name, amount and unit of measurement. """

    def __init__(self, amount, unit, ing_name):
        self.name = ing_name.lower()
        self.unit = unit.lower()
        self.amount = float(amount)

    def __repr__(self):
        return "%.2f" % self.amount + ' ' + str(self.unit) + ' ' + str(self.name)


class Recipe:
    """ Recipe class contains all the information contained in a recipe, including name, source, categories, notes, \
            estimated time, rating, difficulty level, ingredients. """

    def __init__(self, rec_name, rec_source):
        self.name = rec_name.title()
        self.source = rec_source
        self.categories = []
        self.notes = []
        self.rating = ''
        self.level = ''
        self.ingredients = []
        self.time = ''
        self.serving_size = ''

    def set_categories(self, rec_categories):
        self.categories.append(rec_categories.title())

    def set_notes(self, rec_notes):
        self.notes.append(rec_notes)

    def set_rating(self, rec_rating):
        self.rating = rec_rating

    def add_ingredients(self, new_ingredients):
        if not self.ingredients:
            self.ingredients.append(new_ingredients)

        else:
            a = False
            for k in self.ingredients:
                if new_ingredients.name == k.name:
                    a = True
                else:
                    a = False
            if a:
                for k in self.ingredients:
                    if new_ingredients.name == k.name:
                        if new_ingredients.unit == k.unit or new_ingredients.unit == (k.unit + 's'):
                            k.amount += new_ingredients.amount
                        else:
                            print('Please enter ingredient amount in ' + str(k.unit) + ' units.')
            else:
                self.ingredients.append(new_ingredients)

    def set_level(self, skill_level):
        self.level = skill_level

    def set_time(self, rec_time):
        self.time = rec_time

    def set_serving_size(self, serving_size):
        self.serving_size = serving_size

    def __str__(self):
        return ('\033[1m' + 'Name: ' + '\033[0m' + str(self.name) + '\n' + '\033[1m' + 'Source(s): ' + '\033[0m'
                + str(self.source) + '\n' + '\033[1m' + 'Categorie(s): ' + '\033[0m' + str(self.categories) + '\n'
                + '\033[1m' + 'Rating: ' + '\033[0m' + str(self.rating) + ' out of 5 stars \n' + '\033[1m'
                + 'Skill Level: ' + '\033[0m' + str(self.level) + '\n' + '\033[1m' + 'Estimated Time: ' + '\033[0m'
                + str(self.time) + '\n' + '\033[1m' + 'Extra Notes: ' + '\033[0m' + str(self.notes) + '\n' + '\033[1m'
                + 'Ingredients List ' + 'for ' + str(self.serving_size) + ' servings:' + '\033[0m'
                + str(self.ingredients))

    def __repr__(self):
        return str(self.name)


class MyFridge:
    """ MyFridge class contains information about user's fridge inventory, specifically every ingredient name,
    amount and unit of measurement."""

    def __init__(self):
        self.name = ''
        self.amount = 0
        self.unit = ''
        self.inventory = json.load(open('fridgedata.txt'))

    def update_fridge(self, inv_name, amount, unit):
        # Update ingredient amount
        self.name = inv_name.lower()
        self.amount = amount
        self.unit = unit.lower()
        if self.name in self.inventory:
            if self.unit == self.inventory[self.name][1] or self.unit == self.inventory[self.name][1] + 's':
                current_inventory_value = float(self.inventory[self.name][0])
                adding_value = float(self.amount)
                current_inventory_value += adding_value
                self.inventory[self.name] = [current_inventory_value, self.unit]
            else:
                print('Please enter ingredient amount in ' + str(self.inventory[self.name][1]) + ' units.')
        else:
            self.inventory[self.name] = [self.amount, self.unit]
        return self.inventory

    def __str__(self):
        return 'Current inventory: ' + str(self.inventory)


class RecipeOrganizerController:
    """ RecipeOrganizerController class contains the user's recipe database and carries out any action that seeks to
    edit or access the recipe database"""

    def __init__(self):
        self.recipecollection = []
        json_load = json.load(open('recipedata.txt'))
        for j in json_load:
            recipe_obj = Recipe(j["Name"], j["Source"])
            recipe_obj.set_serving_size(j["Serving Size"])
            recipe_obj.set_time(j["Time"])
            recipe_obj.set_rating(j["Rating"])
            recipe_obj.set_level(j["Level"])
            for n in j["Notes"]:
                recipe_obj.set_notes(n)
            for cat in j["Categories"]:
                recipe_obj.set_categories(cat)
            for d in j["Ingredients"]:
                ingredient_obj = Ingredient(d["Amount"], d["Units"], d["Name"])
                recipe_obj.add_ingredients(ingredient_obj)
            self.recipecollection.append(recipe_obj)

    def add_recipes(self, recipe):
        self.recipecollection.append(recipe)

    def find_by_ingredient(self, ingredient_searched):
        # Given a list of recipes and an ingredient, returns list of recipes that contain that ingredient. If user
        # inputs a general query such as "cheese," all recipes with any kind of cheese ingredient will be returned.
        found_recipes = []
        for collection_item in self.recipecollection:
            for ing_in_collection in collection_item.ingredients:
                if ingredient_searched.lower() in ing_in_collection.name:
                    found_recipes.append(collection_item)
                else:
                    continue
        return found_recipes

    def find_by_category(self, category):
        # Given a list of recipes and a category, returns list of recipes within that category.
        found_recipes = []
        for recipe_item in self.recipecollection:
            for rec_item in recipe_item.categories:
                if rec_item == category.title():
                    found_recipes.append(recipe_item)
                else:
                    continue
        return found_recipes

    def create_shopping_list(self, recipe_list):
        # User selects the recipes they want and create_shopping_list creates a list of everything they
        # need to buy
        shopping_list = []
        final_shopping_list = {}
        recipe_name_list = []
        for y in self.recipecollection:
            recipe_name_list.append(y.name)
        for p in recipe_list:
            if p.title() not in recipe_name_list:
                print(str(p) + ' ingredients unknown. Please return to main menu to add recipe to database.')
            else:
                for y in self.recipecollection:
                    if p.title() == y.name:
                        shopping_list.append(y.ingredients)
                    else:
                        continue
        for shopping_item in shopping_list:
            for z in shopping_item:
                # If a list for ingredient name already exists, add z to that list
                if z.name in final_shopping_list:
                    total_list = final_shopping_list[z.name]
                    for element in total_list:
                        # Set total to original amount of ingredient then add amounts from total list
                        if isinstance(element, float):
                            total = final_shopping_list[z.name][0]
                            total += element
                            final_shopping_list[z.name] = [total, z.unit, z.name]
                else:
                    # If ingredient is not in the list, create new key-value pair in final_shopping_list
                    final_shopping_list[z.name] = [z.amount, z.unit, z.name]
        return final_shopping_list

    def update_shopping_list(self, current_inventory, shopping_list):
        # Updates shopping list by looking at fridge inventory and gives the user the option to use what's available.
        updated = {'Ingredients': 'Amount'}
        for f in shopping_list:
            for e in current_inventory.inventory:
                # If ingredient name found in inventory, prompt user to choose whether they want to use available
                # inventory. If yes, subtract needed amount from inventory and subtract amount needed from shopping
                # list.
                if e == f:
                    updated[f] = shopping_list[f]
                    needed = shopping_list[f][0]
                    existing = float(current_inventory.inventory[e][0])
                    if existing >= needed:
                        print(str(e).title() + ' found. Fridge inventory for ' + str(e) + ': '
                              + str(existing) + ' ' + str(current_inventory.inventory[e][1]))
                        update_inv_option = input('Would you like to use the available inventory? Yes or No: ')
                        if update_inv_option.lower() == "yes":
                            existing -= needed
                            current_inventory.inventory[e][0] = existing
                            del updated[f]
                            print('\nFridge inventory updated. You have ' + str(current_inventory.inventory[e])
                                  + ' remaining \n')
                        elif update_inv_option.lower() == "no":
                            continue
                        else:
                            print('Invalid entry. Please enter Yes or No')
                            continue
                    else:
                        needed -= existing
                        current_inventory.inventory[e][0] = 0
                        updated[f] = [needed, shopping_list[f][1], shopping_list[f][2]]
                elif f not in current_inventory.inventory:
                    updated[f] = shopping_list[f]
                else:
                    continue
        if len(updated) == 1:
            recipe_shopping = ' No items needed. All ingredients availabe in fridge.'
        else:
            recipe_shopping_list = []
            for u in updated:
                recipe_shopping_list.append(str(updated[u]))
            recipe_shopping = ' '.join(recipe_shopping_list[1:])
        return 'Here\'s the shopping list based on your current inventory: ' + str(recipe_shopping) + '\n'

    def check_inventory(self, current_inventory, recipe):
        # Check if inventory has enough for a selected recipe
        for product in recipe.ingredients:
            for t in current_inventory.inventory:
                if product.name not in current_inventory.inventory:
                    print('Missing from fridge: ' + str(product) + '\n')
                    break
                if product.name == t:
                    inventory_value = float(current_inventory.inventory[t][0])
                    if inventory_value >= product.amount:
                        original_amount = inventory_value
                        print(str(t).title() + ' found. Fridge inventory for ' + str(t) + ': '
                              + str(original_amount) + ' ' + str(current_inventory.inventory[t][1]))
                        update_inv_option = input('Would you like to use the available inventory? Yes or No: ')
                        if update_inv_option.lower() == "yes":
                            inventory_value -= product.amount
                            current_inventory.inventory[t][0] = inventory_value
                            print('Fridge inventory updated. You have ' + str(current_inventory.inventory[t])
                                  + ' remaining \n')
                        elif update_inv_option.lower() == "no":
                            continue
                        else:
                            print('Invalid entry. Please enter Yes or No')
                            continue
                    else:
                        print('Current fridge inventory only has ' + str(current_inventory.inventory[t])
                              + '. ' + str(product) + ' needed \n')
        return 'Your updated fridge inventory: ' + str(current_inventory.inventory) + '\n'

    def __str__(self):
        return str(self.recipecollection)

#############################################
#          Sample Recipe Directory          #
#############################################

SampleRecipeDirectory = RecipeOrganizerController()

#############################################
#          Sample Inventory                 #
#############################################

SampleFridge = MyFridge()

#############################################
#              User Interface               #
#############################################
border = '-'
print(border.center(75, '-'))
welcome = 'Welcome to your Recipe Organizer!'
print('\033[1m' + welcome.center(75))
print('\033[0m' + border.center(75, '-'))
organizer = True
while organizer:
    print('What would you like to do? \n')
    print('1-add recipe\n')
    print('2-search recipes by category\n')
    print('3-search recipes by ingredient\n')
    print('4-check or update my fridge\n')
    print('5-create shopping list\n')
    print('6-end program')
    command = input('Enter one of the selections above to continue: ')
    if command not in {'1', '2', '3', '4', '5', '6'}:
        print('Invalid entry. Please enter a number between 1 - 6. ')
        continue
    if command == '1':
        user_recipe_name = input('Please enter a recipe name: ')
        for rec in SampleRecipeDirectory.recipecollection:
            if rec.name == user_recipe_name:
                user_prompt = input('Error: Recipe already exists. Type \'1\' to see recipe details or \'return\' to '
                                    'return to main menu: ')
                if user_prompt == '1':
                    print(rec)
            else:
                user_prompt = ''
        if user_prompt == '1':
            continue
        if user_prompt == 'return':
            continue
        if user_recipe_name == '':
            print('No recipe name was entered. Please try again.')
            continue
        user_recipe_source = input('Please enter a URL (followed by a space), or enter None: ')
        if user_recipe_source == '':
            print('No URL was entered. Please try again or enter None')
            continue
        user_recipe = Recipe(user_recipe_name, user_recipe_source)
        SampleRecipeDirectory.add_recipes(user_recipe)
        prompt = input('Would you like to fill out any more details for the recipe? Press any key for yes or enter '
                       'n for no. \n')
        while prompt != 'n':
            start = 'Let\'s fill out more details for this recipe!'
            print(start.center(75, '-') + '\n')
            options = [['a-set recipe category', 'b-give recipe a rating', 'c-set skill level'],
                       ['d-set estimated time', 'e-add ingredients', 'f-set serving size'],
                       ['g-add extra notes', 'h-see recipe', '']]
            col_width = max(len(word) for row in options for word in row) + 2  # padding
            for row in options:
                print("".join(word.ljust(col_width) for word in row))

            next_command = input("\nSelect from the menu above. (To exit, enter \"exit.\") ")
            if next_command not in {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'exit'}:
                print('Invalid entry. Please enter a letter between a-h, or exit to return to main menu.')
                continue
            if next_command == 'a':
                user_recipe_category = input('Enter the category for this recipe (i.e. Meat, Pasta, Beverage, Dinner, '
                                             'Lunch), or type \'skip\' to skip: ')
                if user_recipe_category == '':
                    print('No category was entered. Please enter a category such as Meat, Vegetable, Dinner, etc.')
                while user_recipe_category != 'skip':
                    if user_recipe_category.isdigit():
                        print('Invalid entry. Please enter a category such as Meat, Vegetable, Party, etc.')
                        continue
                    else:
                        user_recipe.set_categories(user_recipe_category)
                        user_recipe_category = input('Enter another category, or enter 1 to exit. ')
                        if user_recipe_category == '1':
                            break
            if next_command == 'b':
                user_recipe_rating = input('Enter the rating for this recipe. Rating is based on a 5 star scale, '
                                           'or type \'end\' to skip. ')
                if user_recipe_rating == 'end':
                    continue
                elif user_recipe_rating == '':
                    print('Error: No rating was entered. Please try again.\n')
                elif not user_recipe_rating.isdigit():
                    print('Error: Rating must be a number between 1-5.\n')
                else:
                    if float(user_recipe_rating) > 5 or float(user_recipe_rating) < 1:
                        print('Error: Rating must be between 1-5, for this 5 star scale system.\n')
                        continue
                    else:
                        user_recipe.set_rating(user_recipe_rating)

            if next_command == 'c':
                user_recipe_level = input('Enter skill level for this recipe. Skill level scale: Easy, Medium, '
                                          'Difficult. To skip, type \'skip\'. ')
                if user_recipe_level == 'skip':
                    continue
                elif user_recipe_level == '':
                    print('Error: No skill level was entered. Please try again.\n')
                elif user_recipe_level.title() == 'Easy' or user_recipe_level.title() == 'Medium' \
                        or user_recipe_level.title() == 'Difficult':
                    user_recipe.set_level(user_recipe_level)
                else:
                    print('Error: Invalid entry. Skill level must be Easy, Medium or Difficult.\n')
                    continue
            if next_command == 'd':
                user_recipe_time = input('Enter estimated time for this recipe. (i.e. 1 hour, 40 minutes) Please sum '
                                         'up both prep time and cooking time. To skip, type \'skip\': ')
                if user_recipe_time == 'skip':
                    continue
                elif user_recipe_time == '':
                    print('Error: No time was entered. Please try again.\n')
                elif not user_recipe_time[0].isdigit():
                    print('Error: Invalid format. Please enter amount of time plus unit of time i.e 5 minutes, '
                          '3 hours\n')
                elif len(user_recipe_time.split()) < 2:
                    print('Error: Invalid entry. Please enter amount of time plus unit of time i.e 5 minutes, '
                          '3 hours\n')
                    continue
                else:
                    user_recipe.set_time(user_recipe_time)
            if next_command == 'e':
                prompt2 = input('Let\'s get started! Press enter to continue or \'return\' for previous menu: ')
                while prompt2 != 'return':
                    ingredient_name = input('Enter name of ingredient (i.e. salmon, broccoli, rice) or type \'skip\' '
                                            'to skip: ')
                    if ingredient_name == '':
                        print('Error: Invalid entry. Please try again.\n')
                        continue
                    if ingredient_name == 'skip':
                        break
                    ingredient_amount = input('Enter amount of ingredient with units: '
                                              '(i.e. 8 oz, 1.56 lb, 2 tsp, 2 whole (for eggs/fruits) or type '
                                              '\'skip\' to skip: ').split()
                    if ingredient_amount != ['skip'] and len(ingredient_amount) < 2:
                        print('Error: Invalid entry. Please try again with the following format: 8 oz, 1.56 lb.\n')
                        continue
                    if ingredient_amount == ['skip']:
                        break
                    elif not ingredient_amount[1].isalpha():
                        print('Error: Invalid unit of measurement. Please try again\n')
                        continue
                    ingredient_amt = ingredient_amount[0]
                    if len(ingredient_amount) < 2:
                        ingredient_unit = input('Please enter the unit of measurement for this ingredient.')
                        ingredient_amount.append(ingredient_unit)
                    else:
                        ingredient_unit = ingredient_amount[1]
                    user_recipe_ingredients = Ingredient(ingredient_amt, ingredient_unit, ingredient_name.lower())
                    user_recipe.add_ingredients(user_recipe_ingredients)
            if next_command == 'f':
                user_recipe_serving = input(
                    'Enter serving size for this recipe (i.e. 1, 2, 3), or type \'skip\' to skip: ')
                if user_recipe_serving == 'skip':
                    continue
                elif user_recipe_serving == '':
                    print('No serving size was entered. Please try again.')
                elif len(user_recipe_serving) > 1:
                    print('Please enter an integer.')
                    continue
                else:
                    user_recipe.set_serving_size(user_recipe_serving)
            if next_command == 'g':
                user_recipe_notes = input('Enter additional notes for this recipe. (If none, type \'skip\' to skip): ')
                while user_recipe_notes != 'skip':
                    user_recipe.set_notes(user_recipe_notes)
                    user_recipe_notes = input('Would you like to add anything else? (If no, type \'skip\' to skip): ')
                if user_recipe_notes == 'skip':
                    continue
            if next_command == 'h':
                print(str(user_recipe) + '\n')
            if next_command == 'exit':
                break
    if command == '2':
        # Search recipes by category
        category_list = []
        for r in SampleRecipeDirectory.recipecollection:
            for c in r.categories:
                category_list.append(c)
        category_list = set(category_list)
        user_category = (input('Enter category (Available options: ' + str(category_list) + '): ')).title()
        if SampleRecipeDirectory.find_by_category(user_category):
            print('Found Recipes: ' + str(SampleRecipeDirectory.find_by_category(user_category)))
            next_question = input('To see full recipe details, enter 1. To exit, enter "exit" ')
            if next_question not in {'1', 'exit'}:
                print('Invalid entry. Please enter 1 to see full recipe details or "exit" to exit. ')
            if next_question == '1':
                for x in SampleRecipeDirectory.find_by_category(user_category):
                    print(str(x) + '\n')
            if next_question == 'exit':
                continue
        else:
            category_list = []
            for r in SampleRecipeDirectory.recipecollection:
                for c in r.categories:
                    category_list.append(c)
            category_list = set(category_list)
            print('There were no matches. Here are the current categories in the database: '
                  + str(category_list) + '\n')

    if command == '3':
        # Search recipes by ingredient
        user_ingredient = input('Enter ingredient: ')
        if SampleRecipeDirectory.find_by_ingredient(user_ingredient):
            print('Found Recipes: ' + str(SampleRecipeDirectory.find_by_ingredient(user_ingredient)))
            next_prompt = input('To see full recipe details, enter 1. To exit, enter "exit" ')
            if next_prompt == '1':
                for x in SampleRecipeDirectory.find_by_ingredient(user_ingredient):
                    print(str(x) + '\n')
            else:
                continue
        else:
            print('There were no matches.')
    if command == '4':
        # Check fridge for recipe ingredients and allow user to update fridge inventory
        user_action = input("What would you like to do?\na: Check the fridge for a recipe\nb: Update what's in your "
                            "fridge\nEnter selection: ")
        if user_action == 'a':
            requested_recipe = input('Which recipe are you checking the fridge for? \nAvailable '
                                     'options: '
                                     + str(SampleRecipeDirectory.recipecollection) + str(' '))
            for item in SampleRecipeDirectory.recipecollection:
                if requested_recipe.title() not in str(SampleRecipeDirectory.recipecollection):
                    print("Requested recipe is not in this database. Please select from the available "
                          "options below or return to the main menu to add new recipe. \nHere is the "
                          "current recipe database: " + str(SampleRecipeDirectory.recipecollection))
                    break
                for ingredient in item.ingredients:
                    if item.name == requested_recipe.title():
                        print('Needed ingredients for ' + str(item.name) + ': ' + str(item.ingredients)
                              + '\n')
                        user_inventory = SampleRecipeDirectory.check_inventory(SampleFridge, item)
                        print(user_inventory)
                        break
                    else:
                        break
        if user_action == 'b':
            print('\nLet\'s update what\'s in the fridge!\n')
            inventory_prompt = ''
            while inventory_prompt != 'q':
                inventory_prompt = input('Enter the name of ingredient, or q to quit: ')
                if inventory_prompt == 'q':
                    break
                for v in SampleFridge.inventory:
                    if inventory_prompt.lower() == v:
                        print('Current inventory for ' + str(v) + ': ' + str(SampleFridge.inventory[v][0])
                              + ' ' + str(SampleFridge.inventory[v][1]))
                inv_amt = input('Enter the amount with units you\'d like to add to the fridge (Enter q to quit): '
                                '').split()
                if inv_amt[0] == 'q':
                    break
                else:
                    SampleFridge.update_fridge(inventory_prompt, inv_amt[0], inv_amt[1])
                    print('Updated inventory ' + str(SampleFridge.inventory[inventory_prompt]))
                    continue
            if inventory_prompt == 'q':
                continue
    if command == '5':
        # Create a shopping list
        print('Let\'s create a shopping list! Here\'s the current recipe collection: '
              + str(SampleRecipeDirectory.recipecollection))
        selected_option = input('Please enter the recipe(s) you\'d like to shop for (i.e. Sous Vide Salmon, Latte), '
                                'separated by ** (i.e. Latte ** Pork Chop, or q to quit: \n').split(' ** ')
        if selected_option == 'q':
            break
        else:
            initial_shopping_list = SampleRecipeDirectory.create_shopping_list(selected_option)
            updated_shopping_list = SampleRecipeDirectory.update_shopping_list(SampleFridge, initial_shopping_list)
            print(updated_shopping_list)
    if command == '6':
        json_data = []
        for r in SampleRecipeDirectory.recipecollection:
            json_ing = []
            json_category = []
            json_notes = []
            name = r.name
            source = r.source
            categories = r.categories
            notes = r.notes
            ingredients = r.ingredients
            rating = r.rating
            level = r.level
            time = r.time
            serving = r.serving_size
            for i in ingredients:
                ing = {"Name": i.name, "Amount": i.amount, "Units": i.unit}
                json_ing.append(ing)
            for c in categories:
                json_category.append(c)
            for note in notes:
                json_notes.append(note)
            item = {"Name": name, "Source": source, "Categories": json_category, "Ingredients": json_ing,
                    "Notes": json_notes,
                    "Rating": rating, "Level": level, "Time": time, "Serving Size": serving}
            json_data.append(item)
        with open('recipedata.txt', 'w') as outfile:
            json.dump(json_data, outfile)
        with open('fridgedata.txt', 'w') as outputfile:
            json.dump(SampleFridge.inventory, outputfile)
        border = '-'
        print(border.center(75, '-'))
        thankyou = 'Thank you for using Recipe Organizer!'
        print('\033[1m' + thankyou.center(75))
        print('\033[0m' + border.center(75, '-'))
        organizer = False
