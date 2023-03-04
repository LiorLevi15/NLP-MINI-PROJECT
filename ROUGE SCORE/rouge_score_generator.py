import json
from rouge_metric import PyRouge
import matplotlib.pyplot as plt
from datasets import load_dataset

dataset = load_dataset("NLP-MINI-PROJECT/rabbi_kook")
split = 'validation'

# Load summaries
with open("/Users/llevi1/Desktop/personal/degree/Mini_Project/rouge_score/model_generated_summaries.json") as f:
    model_summaries = json.load(f)
human_summaries = [[summary] for summary in dataset[split]['summary']]

print(len(model_summaries))
print(len(human_summaries))
# Evaluate document-wise ROUGE scores
rouge = PyRouge(rouge_n=(1, 2, 4), rouge_l=True, rouge_w=True,
                rouge_w_weight=1.2, rouge_s=True, rouge_su=True, skip_gap=4)


# Compute the ROUGE scores for the summaries
# scores = rouge.get_scores(model_summaries, human_summaries, avg=True)
data = rouge.evaluate(model_summaries, human_summaries)
print(data)

# Extract the keys and values from the dictionary
keys = [f"{k}_{sk}" for k in data.keys() for sk in data[k]]
values = [data[k][sk] for k in data.keys() for sk in data[k]]

# Define a list of colors
colors = ['#1f77b4', '#1f77b4', '#1f77b4',
          '#ff7f0e', '#ff7f0e', '#ff7f0e',
          '#2ca02c', '#2ca02c', '#2ca02c',
          '#d62728', '#d62728', '#d62728',
          '#9467bd', '#9467bd', '#9467bd',
          '#8c564b', '#8c564b', '#8c564b',
          '#e377c2', '#e377c2', '#e377c2']

# Set up the figure and axis objects
fig, ax = plt.subplots(figsize=(8, 6))

# Create the bar plot with colors assigned to each bar
ax.bar(keys, values, color=colors[:len(keys)])
ax.set_xticklabels(keys, rotation=45, ha='right', fontsize=8)
ax.set_xlabel('Metric')
ax.set_ylabel('Values')
ax.set_title('Rouge Scores')

# Add numerical values on top of each bar
for i, v in enumerate(values):
    ax.text(i, v, str(round(v, 3)), ha='center', va='bottom', fontsize=8)

# Adjust the spacing between the bars and/or font size of the labels as needed
plt.subplots_adjust(bottom=0.2)
plt.show()





