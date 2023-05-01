from cs50 import get_float

# Ask for change
while True:
    cents = get_float("Change owed: ")*100
    if cents > 0:
        break

# Define the dictionary
coin_types = {
    "quarters": 25,
    "dimes": 10,
    "nickels": 5,
    "pennies": 1,
}

coin_count = 0

# Calculate the coins
for coin in coin_types:
    coin_count_loop = (cents - cents % coin_types[coin]) / coin_types[coin]
    coin_count += coin_count_loop
    cents = cents - coin_count_loop * coin_types[coin]

print(coin_count)