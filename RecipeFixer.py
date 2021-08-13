from math import ceil

class Recipe():
    ingredient_conversions = {}
    ingredient_prices = {}

    def __init__(self, recipe_name):
        if recipe_name != "#CLONE#":
            self.load_ingredient_conversions()
            self.load_ingredient_prices()
            
            self.name, self.batch_size, self.ingredients = self.load_recipe(recipe_name)

    @classmethod
    def load_ingredient_prices(cls):
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
        ingredients = {}
        with open(recipe_name + ".txt") as f:
            (name, batch_size) = f.readline().split()
            for line in f:
                (ingredient, amount, unit) = line.split()
                ingredients[ingredient] = float(amount), unit
        return name, int(batch_size), ingredients

    def convert_recipe_to_grams(self):
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
        scaled_recipe = self.clone()
        scaled_recipe.batch_size = 1

        for ingredient in self.ingredients:
            scaled_recipe.ingredients[ingredient] = self.ingredients[ingredient][0]/self.batch_size, self.ingredients[ingredient][1]

        return scaled_recipe

    def scale_recipe_size(self, target_batch_size):
        single_recipe = self.scale_recipe_to_single()
        scaled_recipe = self.clone()
        scaled_recipe.batch_size = target_batch_size

        for ingredient in self.ingredients:
            scaled_recipe.ingredients[ingredient] = single_recipe.ingredients[ingredient][0] * target_batch_size, single_recipe.ingredients[ingredient][1]
        
        return scaled_recipe

    def calculate_recipe_cost(self):
        # ingredient, amount, unit, price
        total_cost = 0
        for ingredient in self.ingredients:
            ingredient_packages = self.ingredients[ingredient][0] / self.ingredient_prices[ingredient][0]
            print(self.ingredients[ingredient][0] / self.ingredient_prices[ingredient][0])
            total_cost += ingredient_packages * self.ingredient_prices[ingredient][1]
        return round(total_cost,2)
 
    def calculate_recipe_cost_whole_products(self):
        total_cost = 0
        for ingredient in self.ingredients:
            ingredient_packages = ceil(self.ingredients[ingredient][0] / self.ingredient_prices[ingredient][0])
            print(self.ingredients[ingredient][0] / self.ingredient_prices[ingredient][0])
            total_cost += ingredient_packages * self.ingredient_prices[ingredient][1]
        return round(total_cost,2)

    def __str__(self) -> str:
        string = f"==================================\n{self.name} {self.batch_size}\n----------------------------------\nIngredienser:\n"
        for ingredient in self.ingredients:
            string += f"{ingredient:<20} {self.ingredients[ingredient][0]:>6} {self.ingredients[ingredient][1]}\n"
        string += f"----------------------------------\nTotal kostnad: {self.convert_recipe_to_grams().calculate_recipe_cost()} kr\n"
        string += f"Total kostnad (hela produkter): {self.convert_recipe_to_grams().calculate_recipe_cost_whole_products    ()} kr\n"
        return string



recipe = Recipe("test_recipe")
print(recipe)