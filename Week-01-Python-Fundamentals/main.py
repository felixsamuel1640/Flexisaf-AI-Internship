import csv
def analyze_text_pipeline(raw_text, stopwords):
   # Clean text, removes stopwords, count frequencies

   clean_counts = {}

   for sentence in raw_text:
       # Step 1: Normalization(Lowering and stripping punctuation)
       clean_text = sentence.replace("!", "").replace(",", "").replace(".", 
"").lower().strip()
       tokens = clean_text.split()

       # Step 2: Filtering (The Stopword move)
       for word in tokens:
           if word not in stopwords:
               # Step 3: Counting The frequency move
               if word in clean_counts:
                   clean_counts[word] += 1
               else:
                   clean_counts[word] = 1

       return clean_counts

my_sentence = [
    "AI is the future of engineering!",
    "Python is the best language for AI.",
    "Data science requires clean data and Python."
]

my_stopwords = ["is", "the", "of", "and", "for", "a", "in", "to"]

# EXECUTION
final_results = (analyze_text_pipeline(my_sentence, my_stopwords))

# EXPORT TO CSV

with open('cleaned_ai_report.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Word", "Frequency"])
    for key, value in final_results.items():
        writer.writerow([key, value])

print("Analysis complete. File 'cleaned_ai_report.csv' is ready for GitHub!")






