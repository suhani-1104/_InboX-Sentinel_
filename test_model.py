from transformers import pipeline

classifier = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-sms-spam-detection")

texts = [
    "WINNER!! As a valued network customer you have been selected to receivea £900 prize reward! To claim call 09061701461. Claim code KL341.",
    "Free entry in 2 a wkly comp to win FA Cup final tkts 21st May 2005. Text FA to 87121 to receive entry question(std txt rate)T&C's apply 08452810075over18's",
    "Hello darling how are you today?"
]

for t in texts:
    print(classifier(t))
