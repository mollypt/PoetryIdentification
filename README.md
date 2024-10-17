Character-level Poetry Detection 

The Princeton Prosody Archive's For Use in Schools Collection contains ~200 19th-century books used to teach English language, 
literature, and rhetoric. Many volumes include poetry, and, as part of a research effort to trace poets' influence over time, the Center for 
Digital Humanities (CDH) wants to know which poems are most prevalent throughtout the collection. To answer this question, we first need 
to *find* poetry in the collection. 

Ahead of the CDH's attempt to detect poetry using machine learning, I was tasked with seeing how far we could get by working at the character level. Given the OCR text of a page, how can we tell if it contains poetry? 

I started by asking, what does a poem look like? Usually—and almost always in the 19th century—each line starts with a capital letter. Most but not all lines end in commas, and, in general, there are fewer words in a line of poetry than in a line of prose. Sometimes, poems will start and end with quotation marks. 

Page.py uses these considerations to identify line sequences that might be poetry, looking for just the right combination of  of uppercase start characters, end-line commas, stanza numbers, and total words. Volume.py is organizes page data and can provide all of the identified poems in a volume. This code is intended to be run within a HathiTrust Reserach Data Capsule.

Because we don't have ground-truth labels for actual poetry (CDH annotators are working on it!), I tuned parameters based on the results of my test cases. For example, before I added an upper threshold for lines that end in periods, the program was falsely identifying lists of sentences (e.g. using vocabulary words) as poetry because each line began with an uppercase character. 

Similarly, I performed my evaluation based on just a few test volumes. The character-level approach generally worked well, identifying many true postives and only 1-2 false positives per volume. Still, many true poems were missed, and I observed several limitations to the character-level approach. For one, capturing short exerpts (e.g. one or two lines) was difficult because the strongest indicator of a poem is the number of lines beginning with an uppercase character. When tuning parameters, it is important a consider the tradeoff between using broad and specific critera: relaxing the criteria prevents false negatives but produces many more false positives. And, of course, this character-level approach does not allow for much variation in what a poem looks like. 

Project completed summer 2023. 
