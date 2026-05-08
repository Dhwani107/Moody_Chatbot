from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

model = ChatMistralAI(model="mistral-small-2506", temperature=0.9)

print("Choose a mood for the chatbot:")
print("1. Happy")
print("2. Sad")
print("3. Angry")
print("4. Funny")
mood = input("Enter your choice (1-4): ")

if mood == "1":
    system_message = SystemMessage(content="You are a happy ai agent and reply in a happy tone")
elif mood == "2":
    system_message = SystemMessage(content="You are a sad ai agent and reply in a sad tone")
elif mood == "3":
    system_message = SystemMessage(content="You are an angry ai agent and reply in an angry tone")
elif mood == "4":
    system_message = SystemMessage(content="You are a funny ai agent and reply in a funny tone")
else:
    print("Invalid choice. Using default tone.")
    system_message = SystemMessage(content="You are a sad ai agent and reply in a sad tone")

message = [system_message]


print("----------WELCOME TO THE CHATBOT----------")
print("Type 0 to end the conversation.")
while True:

    prompt = input("You:")
    if prompt == "0":
        print("Goodbye!")
        break

    message.append(HumanMessage(content=prompt))
    response = model.invoke(message)
    message.append(AIMessage(content=response.content))
    print("Bot:", response.content)

print(message)