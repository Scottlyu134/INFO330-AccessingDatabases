import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters

conn = sqlite3.connect("pokemon.sqlite")
cur = conn.cursor()

# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue

    # Analyze the pokemon whose pokedex_number is in "arg"

    # You will need to write the SQL, extract the results, and compare
    # Remember to look at those "against_NNN" column values; greater than 1
    # means the Pokemon is strong against that type, and less than 1 means
    # the Pokemon is weak against that type
    pokedex_number = int(arg)
    query = f"SELECT name, {' ,'.join([f'against_{t}' for t in types])} FROM pokemon WHERE pokedex_number = {pokedex_number}"
    cur.execute(query)
    pokemon_data = cur.fetchone()

    if pokemon_data is None:
        print(f"Pokemon was not found!")
        sys.exit(1)

    team.append(pokemon_data)

type_good = {t: 0 for t in types}
type_weak = {t: 0 for t in types}

for pokemon in team:
    name, *against_values = pokemon
    for t, value in zip(types, against_values):
        if value < 1:
            type_weak[t] += 1
        elif value > 1:
            type_good[t] += 1


print(f"The team is good against to type: ")
print(f"The team is weak against to type: ")

answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")

#In order to ensure that all of the changes were committed and all of the resources were released, cut off the connection.
conn.close()