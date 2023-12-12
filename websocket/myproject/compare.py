from evaluate import load

wer = load("wer")

f1 = []
with open('output.txt') as f:
    f1 = f.readlines()

f2 = []
with open('output_2.txt') as f:
    f2 = f.readlines()

wer_score = wer.compute(predictions=f1, references=f2)
print(wer_score)