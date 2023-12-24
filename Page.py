# Given list of String lines and int min_length, return tuple (int, int)
# specifying:
#   1.) the index of list lines that begins a sequence of consecutive lines
#        such that each line begins with a capital letter, number, or quotation
#   2.) the sequence length, which is at least min_length
def _get_potential_poem(lines, min_length):
    upper_seq = []  # a list of tuples (start line, length)
    start_index = -1
    i = -1

    # Iterate through lines
    for line in lines:
        i += 1

        # Check that current line is not empty
        if len(line) > 0:
            # Line begins with uppercase, number, or quote
            if line[0].isupper() or line[0].isnumeric() or line[0] == '"':
                # Enter sequence if not already in one
                if start_index == -1:
                    start_index = i

                # Account for the last line on page staring with uppercase
                elif i == len(lines) - 1:
                    length = i - start_index + 1
                    upper_seq.append((start_index, length))

            # Line does not begin with uppercase, number, or quote
            else:
                # End of uppercase sequence
                if start_index != -1:
                    length = i - start_index
                    # Sequence has at least four lines
                    if length > min_length:
                        upper_seq.append((start_index, length))
                    # Reset sequence
                    start_index = -1

    return upper_seq


# Apply poem criteria to groupings of size min_length of consecutive lines
# provided in String list lines. If poem identified, return the index of
# lines where the poem starts. If no grouping of lines meets the criteria, return -1.
def _verify_poem(lines, min_length):
    num_lines = len(lines)
    start_chars = [' '] * num_lines
    end_chars = [' '] * num_lines

    # Get array with the first characters of each line
    for i in range(num_lines):
        if len(lines[i]) > 0:
            start_chars[i] = lines[i][0]
            end_chars[i] = lines[i][-1]

    # Iterate over each group of size min_length in list lines
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


class Page:
    def __init__(self, vol_id, number):
        file = open("/media/secure_volume/workset/" + vol_id + "/" + number)
        self.contents = file.read()

        # Format page number by removing  leading zeroes and ".txt"
        number = number.replace('00000', '')
        number = number.replace('.txt', '')
        self.number = number

        self.line_count = self.contents.count('\n')
        self.has_poetry = self.has_poetry()

    # Returns the number of occurrences of String phrase on Page
    def count_phrase(self, phrase):
        return self.contents.lower().count(phrase.lower())

    # Returns True if poetry is identified, otherwise False
    def has_poetry(self):
        # Return False if page has no lines
        if self.line_count == 0:
            return False

        # Get list of lines on page
        lines = self.contents.splitlines()

        # Specify poems must be at least four lines long
        min_length = 4
        potential_poems = _get_potential_poem(lines, min_length)

        # Check each sequence of uppercase characters for poem
        for seq in potential_poems:
            seq_lines = [lines[seq[0] + i] for i in range(seq[1])]
            poem_found = _verify_poem(seq_lines, min_length)
            if poem_found > -1:
                return True

        return False

