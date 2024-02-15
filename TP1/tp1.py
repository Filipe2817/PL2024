import sys
import itertools

BOLD_RED = "\033[1;91m"
BOLD_GREEN = "\033[1;92m"
BOLD_BLUE = "\033[1;94m"
WHITE = "\033[0;97m"

def parse_csv():
    athletes = []
    total = 0
    line = sys.stdin.readline() # skip csv header
    for line in sys.stdin:
        line = line.rstrip()
        athlete = line.split(',')
        athletes.append(athlete)
        total += 1   
    return (athletes, total)

def percentage_apt_athletes(athletes, total):
    apt = sum(1 for athlete in athletes if athlete[12] == "true")
    return (apt / total) * 100

def find_age_range(athletes):
    min_age = 128
    max_age = 0
    for athlete in athletes:
        age = int(athlete[5])
        if age < min_age:
            min_age = age
        elif age > max_age:
            max_age = age
    return (min_age, max_age)

def generate_age_group_distribution(athletes, age_range, total):
    (min_age, max_age) = age_range
    age_groups = {}
    start = min_age - (min_age % 5)

    for age in range(start, max_age + 1, 5):
        age_groups[(age, age + 4)] = [0, 0]

    for athlete in athletes:
        age = int(athlete[5])
        group = (age - (age % 5), age - (age % 5) + 4)
        age_groups[group][0] += 1

    for group in age_groups:
        age_groups[group][1] = (age_groups[group][0] / total) * 100

    return age_groups

def print_dynamic_tabular_modalities(modalities):
    num_modalities = len(modalities)
    rows_needed = num_modalities // 5 if num_modalities % 5 == 0 else (num_modalities // 5) + 1
    
    for row in range(rows_needed):
        for col in range(5):
            index = (row * 5) + col
            if index < num_modalities:
                modality = modalities[index]
                spaces = 18 - len(modality)
                if spaces % 2 == 0:
                    print(" " * (spaces // 2) + modality + " " * (spaces // 2), end = "|")
                else:
                    print(" " * (spaces // 2) + modality + " " * (spaces // 2 + 1), end = "|")
            else:
                print(" " * 18, end = "|")
        if row < rows_needed - 1:
            print("\n+------------------+------------------+------------------+------------------+------------------+", end = "\n|")
        else:
            print()

def print_aptitude(apt_athletes):
    (apt_string, inapt_string) = (f"Apt: {apt_athletes:.2f}%", f"Inapt: {100 - apt_athletes:.2f}%")
    (spaces_apt, spaces_inapt) = (46 - len(apt_string), 47 - len(inapt_string))
    print(" " * (spaces_apt // 2) + apt_string + " " * (spaces_apt // 2 + 1) + "|" + " " * (spaces_inapt // 2) + inapt_string + " " * (spaces_inapt // 2), end = "|\n")

def print_dynamic_tabular_age_distribution(age_groups):
    num_groups = len(age_groups)
    rows_needed = num_groups // 3 if num_groups % 3 == 0 else (num_groups // 3) + 1

    for row in range(rows_needed):
        for col in range(3):
            index = (row * 3) + col
            if index < num_groups:
                group = list(age_groups.keys())[index]
                count, percentage = age_groups[group]
                string = f"{group[0]}-{group[1]}: ({count}, {percentage:.2f}%)"
                spaces = 31 - len(string) if col % 2 == 0 else 30 - len(string)
                if spaces % 2 == 0:
                    print(" " * (spaces // 2) + string + " " * (spaces // 2), end = "|")
                else:
                    print(" " * (spaces // 2) + string + " " * (spaces // 2 + 1), end = "|")
            elif col % 2 == 0:
                print(" " * 31, end = "|")
            else:
                print(" " * 30, end = "|")
        if row < rows_needed - 1:
            print("\n+-------------------------------+------------------------------+-------------------------------+", end = "\n|")
        else:
            print()

def main():
    (athletes, total) = parse_csv()
    modalities = [k for k, _ in itertools.groupby(sorted([athlete[8] for athlete in athletes], key = lambda x: x.lower()))]
    apt_athletes = percentage_apt_athletes(athletes, total)
    athlete_distribution = generate_age_group_distribution(athletes, find_age_range(athletes), total)
    
    print("+==============================================================================================+")
    print(f"|{' ' * 42}{BOLD_RED}CATEGORIES{WHITE}{' ' * 42}|")
    print("+==============================================================================================+", end = "\n|")
    print_dynamic_tabular_modalities(modalities)
    print("+==============================================================================================+")
    print(f"|{' ' * 43}{BOLD_BLUE}APTITUDE{WHITE}{' ' * 43}|")
    print("+==============================================================================================+", end = "\n|")
    print_aptitude(apt_athletes)
    print("+==============================================================================================+")
    print(f"|{' ' * 39}{BOLD_GREEN}AGE DISTRIBUTION{WHITE}{' ' * 39}|")
    print("+==============================================================================================+", end = "\n|")
    print_dynamic_tabular_age_distribution(athlete_distribution)
    print("+==============================================================================================+")

if __name__ == '__main__':
    main()

# 1234,100,2023-01-13,Glenn,Best,50,M,Graball,abc,AVCfamalicão,glenn.best@avcfamalicão.ca,true,true
