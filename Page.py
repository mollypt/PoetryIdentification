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

        # Format page number
        number = number.replace('000', '')
        number = number.replace('.txt', '')
        self.number = number

        # Note to self: may need to add 1?
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

        # Get list of lines on page
        lines = self.contents.splitlines()

        # Get consecutive lines of uppercase and numeric chars
        upper_seq = []
        start_seq = -1

        # Get sequences of lines that begin with upper chars
        for i in range(len(lines)):
            if len(lines[i]) > 0:

                # Line begins with upper char or number
                if lines[i][0].isupper() or lines[i][0].isnumeric():
                    # Entering sequence
                    if start_seq == -1:
                        start_seq = i
                    # Last line on page starts with upper char
                    elif i == len(lines) - 1:
                        difference = i - start_seq
                        upper_seq.append((start_seq, difference + 1))

                # Line begins with lower char
                else:
                    # End of upper sequence
                    if start_seq != -1:
                        difference = i - start_seq
                        # Sequence has at least two lines
                        if difference > 1:
                            upper_seq.append((start_seq, difference))
                        # Reset sequence
                        start_seq = -1

        has_poem = False
        for seq in upper_seq:
            seq_lines = [lines[seq[0] + i] for i in range(seq[1])]
            is_poem = __verify_poem__(seq_lines)
            if is_poem:
                print()
                for line in seq_lines:
                    print(line)
                has_poem = True

        return has_poem

