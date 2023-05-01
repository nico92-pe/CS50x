import csv
import sys


def main():

    # Check for command-line usage:
    if len(sys.argv) != 3:
        print("Usage: python dna.py FILENAME TEXT_FILE")
        sys.exit(1)

    # Read database file into a variable:
    file_info = []
    with open(sys.argv[1]) as f:
        reader = csv.DictReader(f)
        for dna in reader:
            file_info.append(dna)

    # Read DNA sequence file into a variable
    dna_text = ""
    with open(sys.argv[2]) as file:
        reader2 = csv.reader(file)
        for row in reader2:
            dna_text = row[0]

    # Find longest match of each STR in DNA sequence and create a dictionary
    dna_dic = {}
    for code in file_info[0]:
        if code != "name":
            code_value = longest_match(dna_text, code)
            dna_dic[code] = code_value
            # print(f"{code}: {code_value}")

    # Check database for matching profiles
    for person in file_info:
        bool = ""
        for i in person:
            if i != 'name':
                example = int(person.get(i))
                example2 = dna_dic.get(i)
                if example != example2:
                    bool = "No match"
                    break
        if bool != "No match":
            print(person["name"])
            return person.get(1)

    print(bool)
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0
        count_max = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            evaluator = sequence[start:end]
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                count_max = count
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count_max)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()