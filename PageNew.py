# Apply poem criteria to groups of size min_length among consecutive lines.
# If poem identified, return the index of lines where the poem starts.
# If no grouping of lines meets the criteria, return -1.x
def __find_poem__(lines, min_length):
    num_lines = len(lines)
    start_chars = [' '] * num_lines
    end_chars = [' '] * num_lines

    # Get array with the first characters of each line
    for i in range(num_lines):
        if len(lines[i]) > 0:
            start_chars[i] = lines[i][0]
            end_chars[i] = lines[i][-1]

    for i in range(num_lines-min_length):
        num_num = 0
        num_quote = 0
        num_commas = 0
        num_short = 0
        for j in range(min_length):
            # At most one line can begin in a number
            if start_chars[i+j].isnumeric():
                num_num += 1
            # At most one line can begin with a quote
            if start_chars[i+j] == '"':
                num_quote += 1
            # At least two lines must end in commas
            if end_chars[i + j] == ',':
                num_commas += 1
            # At most one line can be short
            words = lines[i+j].split()
            if len(words) < 4:
                num_short += 1

        # Passes checks for start and end chars and line length
        if num_num < 2 and num_quote < 2 and num_commas > 1 and num_short < 2:
            # print poem lines
            for j in range(i, i+min_length):
                print(lines[j])
            return i

    return -1

def __verify_poem__(lines):
    num_lines = len(lines)
    punctuation = ['.', '?', '!']
    score = 0

    # Count end-sentence punctuation in each line
    sentence_count = 0
    # Count lines with fewer than 4 words
    short = 0
    # Count lines that begin with a number
    num_start = 0

    for line in lines:
        # Count sentences per line
        for char in line:
            if char in punctuation:
                sentence_count += 1
        words = line.split()
        # Count short lines
        if len(words) < 4:
            short += 1
        if len(line) > 0:
            if line[0].isnumeric():
                num_start += 1

    # Fewer sentences than lines
    if sentence_count < num_lines:
        score += 1

    # Fewer than half of lines are short
    if short < num_lines * (1/2):
        score += 1

    # Fewer than 20 percent of lines begin with a number
    if num_start < num_lines * (1/5):
        score += 1

    result = score == 3

    # Print identified poems
    if result:
        print(lines)

    return result


class Page:
    def __init__(self, vol_id, number):
        file = open("/media/secure_volume/workset/" + vol_id + "/" + number)
        self.contents = file.read()

        # Format page number by removing  leading zeroes and ".txt"
        number = number.replace('00000', '')
        number = number.replace('.txt', '')
        self.number = number

        self.line_count = self.contents.count('\n')

        self.has_poetry = self.__has_poetry__()

    # Returns the number of occurrences of String phrase on Page
    def count_phrase(self, phrase):
        return self.contents.lower().count(phrase.lower())

    # Returns True if poetry is identified, otherwise False if not
    def __has_poetry__(self):
        # Page has no lines
        if self.line_count == 0:
            return False

        new_lines = [-1, self.contents.find('\n')]
        seq_ct = 0
        seqs = []

        # Find sequences of four or more lines that might be poetry
        for line_num, index in enumerate(new_lines):
            if len(self.contents) > line_num:
                start_char = self.contents[1 + line_num]
                # In sequence
                if start_char.isupper() or start_char.isnumeric() or start_char == '"':
                    seq_ct += 1

                # End of sequence
                elif seq_ct > 3:
                    start_seq = new_lines[index-seq_ct]
                    end_seq = line_num
                    seqs.append(self.contents[start_seq:end_seq])
                    seq_ct = 0

                # No sequence
                elif seq_ct != 0:
                    seq_ct = 0

            # Apply poetry criteria to uppercase sequences
            for seq in seqs:
                # Split sequence into lines
                new_lines = seq.find("\n")


                    if lines.length >
                #TO DO

        # Check each sequence of uppercase characters for poem
        for seq in potential_poems:
            seq_lines = [lines[seq[0] + i] for i in range(seq[1])]
            poem_found = __find_poem__(seq_lines, min_length)
            if poem_found > -1:
                return True

        return False

