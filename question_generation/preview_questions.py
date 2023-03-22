import json

q = json.load(open('/home/nlp/users/bkroje/clevr/output/CLEVR_questions.json'))
for i in q['questions']:
    print(f"{i['image_filename']}")
    print(f"Q: {i['question']}\nA: {i['answer']}\n")