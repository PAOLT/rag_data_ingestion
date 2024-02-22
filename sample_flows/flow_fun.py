from promptflow import load_flow
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--flow_path', default='.', type=str, help="PromptFlow flow directory")
args = parser.parse_args()

f = load_flow(source=args.flow_path)
history = []
q=None

print("Welcome! Start asking questions, when done just say 'bye")
while True:
    q = input("User: ")
    if q == 'bye':
        break
    result = f(history=history,question=q)
    print(f"Bot: {result}")
    history.append({"inputs": {"question": q}, "outputs": {"answer": result}})
print("Goodbye!")
