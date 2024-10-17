class Page:
    def __init__(self, vol_id, number):
        file = open("/media/secure_volume/workset/" + vol_id + "/" + number)

        contents = file.read()
        self.lines = contents.splitlines()

        # Format page number by removing leading zeroes and ".txt"
        number = number.replace('00000', '')
        number = number.replace('.txt', '')
        self.number = number

        self.line_count = self.lines.count('\n')
        self.poems = self.find_poetry()

    # Returns the number of occurrences of String phrase on Page
    def count_phrase(self, phrase):
        return self.contents.lower().count(phrase.lower())

    # Return True if poetry identified on page, otherwise return False
    def has_poetry(self):
        return len(self.poems) > 0

    # Return all poems associated with a page
    def get_poems(self):
        return self.poems

    # Given a page, print length number of lines on the page from the provided start index
    def print_lines(self, start, length):
        end = start + length
        # Ensure you don't try to print beyond the end of the page
        if len(self.lines) < end:
            end = len(self.lines) - 1
        for i in range(start, start + end):
            print(self.lines[i])

    # Given a page and int min_length, return a list of tuples (int, int)
    # specifying:
    #   1.) the index of the line that begins a sequence of consecutive lines
    #      that begin with a capital letter, number, or quotation
    #   2.) the sequence length, which is at least min_length.
    def _get_potential_poem(self, min_length):
        upper_seq = []  # a list of tuples (start line, length)
        start_index = -1
        i = -1

        for line in self.lines:
            i += 1

            # Check that current line is not empty
            if len(line) > 0:
                # If line begins with uppercase, number, or quote
                if line[0].isupper() or line[0].isnumeric() or line[0] == '"':
                    # Begin counting sequence if not already in one
                    if start_index == -1:
                        start_index = i

                    # Account for the last line on page staring with uppercase
                    elif i == len(self.lines) - 1:
                        length = i - start_index + 1
                        upper_seq.append((start_index, length))

                # If line does not begin with uppercase, number, or quote
                else:
                    # End of uppercase sequence
                    if start_index != -1:
                        length = i - start_index
                        # If sequence has at least four lines, save it
                        if length > min_length:
                            upper_seq.append((start_index, length))
                        # Reset sequence
                        start_index = -1

        return upper_seq

    # Given a page with potential poems, represented in the seq list, apply additional 
    # crtieria to verify the poems. If a poem is verified, return 1 and a tuple of length 
    # two containing indices where the poem starts and ends. 
    # If no grouping of lines meets the criteria, return -1.
    def _verify_poem(self, seq, min_length):
        seq_lines = [self.lines[seq[0] + i] for i in range(seq[1])]
        num_lines = len(seq_lines)
        start_chars = [' '] * num_lines
        end_chars = [' '] * num_lines

        # Get array with the first characters of each line
        for i in range(num_lines):
            start_chars = [line[0] for line in seq_lines if len(line) > 0]
            end_chars = [line[-1] for line in seq_lines if len(line) > 0]

        # Iterate over each group of min_length number of consecutive lines
        for i in range(num_lines - min_length):
            numbers, quotes, commas, short = 0, 0, 0, 0
            for j in range(min_length):
                # At most two lines can begin in a number
                if start_chars[i + j].isnumeric():
                    numbers += 1
                # At most one line can begin with a quote
                if start_chars[i + j] == '"':
                    quotes += 1
                # At least two lines must end in commas
                if end_chars[i + j] == ',':
                    commas += 1
                # At most one line can be short
                words = seq_lines[i + j].split()
                if len(words) < 4:
                    short += 1

            # Passes checks for start and end chars and line length
            if numbers < 3 and quotes < 2 and commas > 1 and short < 2:
                # Most lines start with uppercase chars
                if len(seq_lines[i])/2 > quotes + numbers:
                    return 1, (i, i+min_length)
            print()

        return -1

    # Returns True if poetry is identified, False if not. 
    def find_poetry(self):
        # Return False if page has no lines
        if self.line_count == 0:
            return False

        # Poems must be at least four lines long
        min_length = 4

        potential_poems = self._get_potential_poem(min_length)

        poems = []
        # Verify each sequence of uppercase characters as potential poem
        for seq in potential_poems:
            poem_found, poem_index = self._verify_poem(seq, min_length)
            if poem_found > -1:
                poems.append(poem_index)

        return poems





