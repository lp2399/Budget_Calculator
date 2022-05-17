import math
class Category:
    def __init__(self,category):
        self.category = category 
        self.ledger = []

    def __str__(self):
        asterik_quantity = (30-(len(self.category)))//2 # right_side + len(middle)+ left_side = 30 therefore if len(middle)=5 then 30-5 = 25, 25//2 then check is even
        if(len(self.category)%2==0):# Checking if is even for formatting
            formatted_title = """{0}{1}{2}""".format("*"*asterik_quantity,self.category,"*"*asterik_quantity)
        else:
            formatted_title = """{0}{1}{2}""".format("*"*asterik_quantity,self.category,"*"*(asterik_quantity+1))     
        formatted_list = [] # the formatted list that will be returned
        formatted_list.append(formatted_title)# appending out title
        total = 0 # helps us track the total
        description = "" # placeholder
        amount = 0 # used for tracking amount initally 0
        for i in self.ledger: # iterate through the ledger list to obtain info
            for key,val in i.items():
                if(key=="description"):
                    description = val  # getting the val for key'description' 
                if(key=="amount"):
                    amount = val # getting the int val from key'amount'
                    total = val+total  # here we add all values from keys'amount'  
            formatted_amount_description="""
{0:23}{1:7} """.format(description[0:22],amount)# [0:22] helps truncate the len of descrpiton so that it fits consisintly
            formatted_list.append(formatted_amount_description)
        formatted_total = """\nTotal: {}\n""".format(total)
        formatted_list.append(formatted_total)     
        return ''.join([''.join(i) for i in zip(formatted_list)]) #finally we us list comprension and join to return a string

    def deposit(self,amount, description=""):
        return self.ledger.append({"amount":amount,"description":description}) # creating 2 dicts for deposit

    def withdraw(self,amount, description=""):
        if(self.check_funds(amount)): # funds will return true if suffienct funds to make withdrawl
            self.ledger.append({"amount":-amount,"description":description})# the amount is negative for eventual summation
            return True # returns true so we dont have to use else statement since if this conditon fails it will just return false
        return False

    def get_balance(self):
        return sum([i["amount"] for i in self.ledger]) # gets the total sum of values from keys'amount'

    def transfer(self,amount, category):
        if(self.check_funds(amount)): #checks if there are suffiecnt funds to transfer
            self.withdraw(amount, f"Transfer to {category}") # we use the withdraw method
            category.deposit(amount, f"Transfer from {self.category}")# transfers to category obj
            return True        
        return False

    def check_funds(self,amount):
        if(amount>self.get_balance()): # get out balance and compare the amount if amount>balance= true than insuffiecnt funds
            return False
        return True 
        
def create_spend_chart(catergories_list):
    formatted_list = [] # final formatted list used in printing
    withdraws = [] # tracks our withdraws
    total = 0
    title = """Percentage spent by category 100% {0} """.format("|"*100) # helps visualize 100% for comparison to the rest of the graph
    formatted_list.append(title)
    for category in catergories_list:
        withdrawn_amount = 0
        for action in category.ledger:
            if action["amount"] < 0: # we want to get all negative or withdrawls
                withdrawn_amount -= action["amount"]
                categ = category.category # grabbing the name of the category
                categ_withdrawn_amount_dict = {categ: math.ceil(withdrawn_amount * 1000) / 1000} # creating a dictionary with {name:amount_spent}
        withdraws.append(categ_withdrawn_amount_dict)
    total = get_total(withdraws) # this static method helps get the total for the percentage it adds the total from dict {name:amount_spent} amount_spent
    for i in withdraws:
        for key,val in i.items():# now iterate through our dicts
            percentage = val/total # getting the percentage for each obj
            formatted_str = """
{0:29} {1}% {2}""".format(key,int((math.ceil(percentage * 1000) / 1000)*100),'|'*int((math.ceil(percentage * 1000) / 1000)*100)) # some rounding error occurs and we may get 99% instead of 100            
        formatted_list.append(formatted_str)   
    return '\n'.join([''.join(i) for i in zip(formatted_list)])# 

def get_total(withdraws):
    total = 0
    for i in withdraws:
        for key,val in i.items():
            total = val+total
    return total      
  
# TESTING CODE 
food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
print(food.check_funds(100))
clothing = Category("Clothing")
food.transfer(50, clothing)
print(clothing.get_balance())
clothing.withdraw(25.55)
clothing.withdraw(100)

auto = Category("Auto")
auto.deposit(1000, "initial deposit")
auto.withdraw(15)

print(food)
print(clothing)
print(auto)

print(create_spend_chart([food, clothing, auto]))

""" 
                                                                          OUTPUT
*************Food*************
initial deposit           1000
groceries               -10.15
restaurant and more fo  -15.89
Transfer to **********     -50
Total: 923.96
***********Clothing***********
Transfer from Food          50
                        -25.55
Total: 24.45
*************Auto*************
initial deposit           1000
                           -15
Total: 985
Percentage spent by category 100% ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
Food                          65% ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
Clothing                      22% ||||||||||||||||||||||
Auto                          12% |||||||||||||
"""

