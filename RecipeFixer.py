from math import ceil

class Recipe():
    """
    Example use:

    recipe_x = Recipe("recipe_name")
    recipe_x = recipe_x.convert_recipe_to_grams()
    recipe_X = recipe_x.scale_recipe_size(200)
    recipe_x.save_recipe()

    """
    ingredient_conversions = {}
    ingredient_prices = {}
    merged = False

    def __init__(self, recipe_name):
        if recipe_name == "#MERGE#":
            self.name = "Merged recipe"
            self.batch_size = 0
            self.ingredients = {}
        elif recipe_name != "#CLONE#":
            self.load_ingredient_conversions()
            self.load_ingredient_prices()
            
            self.name, self.batch_size, self.ingredients = self.load_recipe(recipe_name)

    @classmethod
    def load_ingredient_prices(cls):
        """
        Loads ingredient prices from text file.
        """
        with open("./ingredient_prices.txt") as f:
            for line in f:
                (ingredient, amount, unit, price) = line.split()
                conversion_rate = 1
                if unit == 'kg':
                    conversion_rate = 1000
                if unit == 'dl':
                    conversion_rate = cls.ingredient_conversions[ingredient][0]
                if unit == 'msk':
                    conversion_rate = cls.ingredient_conversions[ingredient][1]
                if unit == 'tsk':
                    conversion_rate = cls.ingredient_conversions[ingredient][2]
                
                cls.ingredient_prices[ingredient] = float(amount)*conversion_rate, float(price)

    @classmethod
    def load_ingredient_conversions(cls):
        """
        Loads ingredient conversion rates. X to grams.
        """
        with open("./ingredient_conversions.txt") as f:
            for line in f:
                (ingredient, grams, amount, unit) = line.split()
                if unit == 'dl':
                    cls.ingredient_conversions[ingredient] = float(grams)/float(amount), float(grams)/(float(amount)*6.6), float(grams)/(float(amount)*20)
                if unit == 'msk':
                    cls.ingredient_conversions[ingredient] = float(grams)/(float(amount)/6.6), float(grams)/(float(amount)), float(grams)/(float(amount)*3)
                if unit == 'tsk':
                    cls.ingredient_conversions[ingredient] = float(grams)/(float(amount)/20), float(grams)/(float(amount)/3), float(grams)/(float(amount))

    def clone(self):
        clone = Recipe("#CLONE#")
        clone.name = self.name
        clone.batch_size = self.batch_size
        clone.ingredients = self.ingredients
        return clone

    def load_recipe(self, recipe_name):
        """
        Loads recipe from text file.
        Recipe example:
            Recipe_name batch_size
            ingredient_1 amount unit
            ...
            ingredient_n amount unit
        """
        ingredients = {}
        with open(recipe_name + ".txt") as f:
            (name, batch_size) = f.readline().split()
            for line in f:
                (ingredient, amount, unit) = line.split()
                ingredients[ingredient] = float(amount), unit
        return name, int(batch_size), ingredients

    def convert_recipe_to_grams(self):
        """
        Returns recipe with all ingredients converted to grams.
        """
        converted_ingredients = {}
        for ingredient in self.ingredients:
            conversion_rate = 99999999
            
            if self.ingredients[ingredient][1] == 'g':
                conversion_rate = 1

            elif self.ingredients[ingredient][1] == 'dl':
                conversion_rate = self.ingredient_conversions[ingredient][0]

            elif self.ingredients[ingredient][1] == 'msk':
                conversion_rate = self.ingredient_conversions[ingredient][1]

            elif self.ingredients[ingredient][1] == 'tsk':
                conversion_rate = self.ingredient_conversions[ingredient][2]
            
            grams = self.ingredients[ingredient][0] * conversion_rate
            converted_ingredients[ingredient] = grams, 'g'

        gram_recipe = self.clone()
        gram_recipe.ingredients = converted_ingredients
        return gram_recipe

    def scale_recipe_to_single(self):
        """
        Returns a version of the recipe scaled to batch size of one.
        """
        scaled_recipe = self.clone()
        scaled_recipe.batch_size = 1

        for ingredient in self.ingredients:
            scaled_recipe.ingredients[ingredient] = self.ingredients[ingredient][0]/self.batch_size, self.ingredients[ingredient][1]

        return scaled_recipe

    def scale_recipe_size(self, target_batch_size):
        """
        Returns a version of the recipe scaled to the given batch size.
        """
        single_recipe = self.scale_recipe_to_single()
        scaled_recipe = self.clone()
        scaled_recipe.batch_size = target_batch_size

        for ingredient in self.ingredients:
            scaled_recipe.ingredients[ingredient] = single_recipe.ingredients[ingredient][0] * target_batch_size, single_recipe.ingredients[ingredient][1]
        
        return scaled_recipe

    def calculate_recipe_cost(self):
        """
        Returns what it would cost to just the neccesary amount of ingredient packages needed for the recipe.
        """
        # ingredient, amount, unit, price
        total_cost = 0
        for ingredient in self.ingredients:
            ingredient_packages = self.ingredients[ingredient][0] / self.ingredient_prices[ingredient][0]
            total_cost += ingredient_packages * self.ingredient_prices[ingredient][1]
        return round(total_cost,2)
 
    def calculate_recipe_cost_whole_products(self):
        """
        Returns what it would cost to buy all ingredient packages needed for the recipe.
        """
        total_cost = 0
        for ingredient in self.ingredients:
            ingredient_packages = ceil(self.ingredients[ingredient][0] / self.ingredient_prices[ingredient][0])
            total_cost += ingredient_packages * self.ingredient_prices[ingredient][1]
        return round(total_cost,2)

    def calculate_recipe_ingredient_packages(self):
        """
        Returns a dictionary of how many packages of ingredients is needed for the recipe.
        """
        ingredient_packages = {}
        for ingredient in self.ingredients:
            ingredient_packages[ingredient] = ceil(self.ingredients[ingredient][0] / self.ingredient_prices[ingredient][0])

        return ingredient_packages

    def get_shopping_list(self):
        """
        Returns a string with how many packages of ingredients is needed for the recipe, with package price.
        """
        string = f"{'-'*70}\nInköpslista:\n"
        ingredient_packages = self.calculate_recipe_ingredient_packages()
        for ingredient in ingredient_packages:
            string += f"{ingredient:<20} |{round(ingredient_packages[ingredient],1):>4} st   | {int(self.ingredient_prices[ingredient][0]):>6} gram {self.ingredient_prices[ingredient][1]:>6} kr/st\n"
        return string

    def __str__(self) -> str:
        string = f"{'='*70}\n{self.name} {self.batch_size} st\n{'-'*70}\nIngredienser:\n"
        for ingredient in self.ingredients:
            string += f"{ingredient:<20} {int(round(self.ingredients[ingredient][0],0)) if self.ingredients[ingredient][1] == 'g' else round(self.ingredients[ingredient][0],1):>6} {self.ingredients[ingredient][1]}\n"
        string += self.convert_recipe_to_grams().get_shopping_list()
        string += f"{'-'*70}\nTotal kostnad: {self.convert_recipe_to_grams().calculate_recipe_cost()} kr\n"
        string += f"Total kostnad (hela produkter): {self.convert_recipe_to_grams().calculate_recipe_cost_whole_products()} kr\n"
        return string
    
    def save_recipe(self):
        """
        Saves current recipe to a text file as "RECIPE_NAME BATCH_SIZE st.txt".
        If recipe is a merged recipe it will save as ""Sammanslaget recept.txt".
        """
        filename = f"{self.name} {self.batch_size} st" if not self.merged else "Sammanslaget recept"
        with open(f"{filename}.txt", "w") as text_file:
            text_file.write(self.__str__())

    
    @classmethod
    def merge_recipes(cls, recipe_a, recipe_b):
        """
        Takes two recipes and combines them returning a recipe containing
        the total amount of ingridients for both recipes.
        """
        recipe_a = recipe_a.convert_recipe_to_grams()
        recipe_b = recipe_b.convert_recipe_to_grams()
        merged_recipe = Recipe("#MERGE#")
        merged_recipe.name = f"Sammanslaget: {recipe_a.name} {recipe_a.batch_size} st & {recipe_b.name}"
        merged_recipe.batch_size = recipe_b.batch_size
        merged_recipe.merged = True
        for ingredient in recipe_a.ingredients:
            if ingredient not in merged_recipe.ingredients:
                merged_recipe.ingredients[ingredient] = recipe_a.ingredients[ingredient]
        
        for ingredient in recipe_b.ingredients:
            if ingredient not in merged_recipe.ingredients:
                merged_recipe.ingredients[ingredient] = recipe_b.ingredients[ingredient]
            else:
                merged_recipe.ingredients[ingredient] = recipe_a.ingredients[ingredient][0] + recipe_b.ingredients[ingredient][0], recipe_a.ingredients[ingredient][1]
        return merged_recipe



# Single recipe, saved as "Hallongrottor 200 st.txt"
hallongrottor = Recipe("hallongrottor")
hallongrottor = hallongrottor.convert_recipe_to_grams()
hallongrottor = hallongrottor.scale_recipe_size(200)
hallongrottor.save_recipe()

# Merged recipes, saved as "Sammanslaget recept.txt"
kolakakor = Recipe("kolakakor")
kolakakor = kolakakor.convert_recipe_to_grams()
Recipe.merge_recipes(hallongrottor, kolakakor).save_recipe()
