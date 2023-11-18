import json
from difflib import get_close_matches

hard_reset ={
      "questions": [ 

      ]
}

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data



def save_knowledge_base(file_path:str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data,file,indent=2)


def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


def get_answer_for_question(question: str, conhecimento: dict) -> str | None:
    for q in conhecimento["questions"]:
        if q["question"] == question:
            return q["answer"]


def chat_bot():
    conhecimento: dict = load_knowledge_base('conhecimento.json')

    while True:
        user_input: str = input('Você: ')

    # comandos

        if user_input.lower() == '>quit':
            break
        if user_input.lower() == '>hard reset':
            with open("conhecimento.json",'w') as file:
                pass
            out_file = open("conhecimento.json", "w") 
            json.dump(hard_reset, out_file, indent = 1) 
            out_file.close()
            print('A base de conhecimento foi resetada.')
            break

    # respostas
            
        best_match: str | None = find_best_match(user_input, [q["question"] for q in conhecimento["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, conhecimento)
            print(f'Eu: {answer}')
        else:
            print(f'Bot: Não sei a resposta, me ensine.')
            new_answer: str = input('Digite a resposta (deixe vazio para pular)... ')

            if new_answer.lower() != '':
                conhecimento["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('conhecimento.json', conhecimento)
                print('Bot: Resposta amarzenada.')

if __name__ == '__main__':
    chat_bot()