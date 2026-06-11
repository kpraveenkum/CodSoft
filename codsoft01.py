import re
import random
from datetime import datetime
class AdvancedChatbot:
    def __init__(self):
        self.simple_responses = {
            "hi": "hi sir, What help do you need?",
            "hello": "hello sir, What help do you need",
            "bye": "Thank you sir",
            "goodbye": "goodbye, have a nice day ",
            "ok": "OK, ask me anything that you want to ask"
        }
        self.regex_rules = [
            (re.compile(r"\b(hi|hello|hey)\b", re.I), self.greet),
            (re.compile(r"\b(bye|goodbye|see you|exit)\b", re.I), self.farewell),
            (re.compile(r"\b(thank you|thanks|thankyou|thanx|thanks for the help)\b", re.I), self.thanks),
            (re.compile(r"\b(what is your name|what's your name)\b", re.I), self.give_name),
            (re.compile(r"\b(how are you)\b", re.I), self.how_are_you),
            (re.compile(r"\bmy name is (\w+)\b", re.I), self.remember_name),
            (re.compile(r"\b(help|assist|support)\b", re.I), self.help),
            (re.compile(r"\b(weather|temperature)\b", re.I), self.weather),
            (re.compile(r"\b(what day is today|what is the date|today's date)\b", re.I), self.get_date),
            (re.compile(r"\b(what time is it|current time)\b", re.I), self.get_time)
        ]
        self.intents = {
            "greet": {
                "patterns": [r"\b(hello|hi|hey)\b", r"good(morning|afternoon|evening)"],
                "responses": ["hi", "hello", "hey", "what's up", "greetings!"]
            },
            "farewell": {
                "patterns": [r"\b(exit|bye|see you later|goodbye)\b"],
                "responses": ["good bye", "have a good day", "bye", "see you later", "take care"]
            },
            "thanks": {
                "patterns": [r"\b(thank you|thanks|thanx)\b"],
                "responses": ["you're welcome", "my pleasure", "happy to help"]
            },
            "identify": {
                "patterns": [r"who are you", r"what are you", r"what is your name"],
                "responses": ["I am an advanced chatbot with three different modes",
                              "I am a chatbot for friendly conversations"]
            },
            "help": {
                "patterns": [r"\b(help|support|assist)\b", r"what can you do"],
                "responses": ["let me help you", "I can assist you", "lets see",
                              "I can chat, answer simple questions, tell time, remember your name, and more!"]
            },
            "emotion": {
                "patterns": [r"\b(happy|sad|angry|bored)\b"],
                "responses": ["I see it's interesting", "tell me more about it", "thanks for sharing your opinion"]
            }
        }
        self.user_name = None
        self.conversation_history = []
        self.default_responses = [
            "I don't quite understand. Can you rephrase?",
            "Interesting! Tell me more.",
            "I'm not sure about that. Ask me something else?",
            "Could you please rephrase that?",
            "I'm still learning. Can you try asking differently?"
        ]
        self.response_index = 0
    def greet(self, match=None):
        return random.choice(self.intents["greet"]["responses"])
    def farewell(self, match=None):
        return random.choice(self.intents["farewell"]["responses"])
    def thanks(self, match=None):
        return random.choice(self.intents["thanks"]["responses"])
    def give_name(self, match=None):
        return "I am a chatbot for friendly talk, an advanced rule-based chatbot!"
    def how_are_you(self, match=None):
        responses = [
            "I'm just code, but I'm running smoothly! How are you?",
            "I'm doing great! Thanks for asking!",
            "All systems operational! How can I help you?"
        ]
        return random.choice(responses)
    def get_date(self, match=None):
        now = datetime.now()
        return f"today is {now.strftime('%Y-%m-%d')}"
    def get_time(self, match=None):
        now = datetime.now()
        return f"it's {now.strftime('%H:%M:%S')}"
    def weather(self, match):
        conditions = ["sunny", "rainy", "windy", "snowy"]
        temperatures = ["hot", "cold", "warm", "cool"]
        return f"I can't check real weather, but I hope it's {random.choice(conditions)} and {random.choice(temperatures)} wherever you are"
    def remember_name(self, match):
        self.user_name = match.group(1)
        return f"nice meeting you {self.user_name}! I will try to remember you"
    def help(self, match=None):
        return """I can help you with:
        • Greetings (hi, hello, hey)
        • Farewells (bye, goodbye)
        • Telling time and date
        • Remembering your name
        • Answering questions about myself
        • Basic conversation
        Just type naturally and I'll do my best!"""
    def check_simple_responses(self, user):
        user_lower = user.lower().strip()
        if user_lower in self.simple_responses:
            return self.simple_responses[user_lower]
        return None
    def check_regex_rules(self, user):
        for pattern, response_func in self.regex_rules:
            match = pattern.search(user)
            if match:
                return response_func(match)
        return None
    def check_intents(self, user):
        for intent, data in self.intents.items():
            for pattern in data["patterns"]:
                if re.search(pattern, user, re.I):
                    return random.choice(data["responses"])
        return None
    def get_response(self, user):
        original_input = user
        user_input = user.lower().strip()
        self.conversation_history.append({"user": original_input, "bot": None})
        if user_input in ["quit", "exit", "q"]:
            return None
        simple_response = self.check_simple_responses(user)
        if simple_response:
            response = simple_response
        else:
            regex_response = self.check_regex_rules(original_input)
            if regex_response:
                response = regex_response
            else:
                intent_response = self.check_intents(original_input)
                if intent_response:
                    response = intent_response
                else:
                    response = self.default_responses[self.response_index]
                    self.response_index = (self.response_index + 1) % len(self.default_responses)
        if self.user_name and "name" not in user_input and len(response) < 100:
            if random.random() < 0.3:
                response = f"{self.user_name}, {response.lower()}"
        self.conversation_history[-1]["bot"] = response
        return response
    def show_status(self):
        print("-" * 50)
        print(f"Total conversations: {len(self.conversation_history)}")
        print(f"Thank you {self.user_name if self.user_name else 'user'}")
        print("-" * 50)
    def start_chat(self):
        print("\n" + "=" * 50)
        print("Advanced ChatBot - with pattern matching approaches!")
        print("=" * 50)
        print("\nFeatures from all three chatbots:")
        print("$ Simple dictionary responses")
        print("$ Regex pattern matching with function")
        print("$ Intent-based system with random responses")
        print("$ Name memory and conversation context")
        print("\nType 'quit' or 'exit' to end the conversation")
        print("-" * 50 + "\n")
        while True:
            user = input("You: ").strip()
            if not user:
                print("Bot: Please say something")
                continue
            response = self.get_response(user)
            if response is None:
                print("Bot: Thank you for chatting, goodbye!")
                self.show_status()
                break
            print(f"Bot: {response}")

def simple_combined_chatbot():
    simple_greetings = ["hi", "hello", "hey"]
    name_pattern = re.compile(r"my name is (\w+)", re.I)
    user_name = None
    intent_patterns = {
        r"\b(bye|goodbye|see you|later)\b": ["Goodbye!", "See you later!", "Take care!"],
        r"\b(thanks|thank you|thnx)\b": ["You're welcome!", "Happy that I helped you!", "My pleasure!"],
        r"\b(what can you do|help)\b": ["I am a simple chatbot", "I can talk to you", "I can remember your name",
                                        "I can tell time and date"]
    }
    def get_response(user):
        nonlocal user_name
        user_lower = user.lower().strip()
        if user_lower in simple_greetings:
            return random.choice(["Hi there!", "Hello!", "Hey!"])
        name_match = name_pattern.search(user)
        if name_match:
            user_name = name_match.group(1)
            return f"Nice to meet you {user_name}!"
        if "time" in user_lower:
            return f"It's {datetime.now().strftime('%H:%M:%S')}"
        if "date" in user_lower:
            return f"It's {datetime.now().strftime('%Y-%m-%d')}"
        for pattern, responses in intent_patterns.items():
            if re.search(pattern, user, re.I):
                return random.choice(responses)
        if user_name and random.random() < 0.5:
            return f"Sorry {user_name}, I can't understand. Please repeat it again once more"
        return "I can't understand what you mean. Try asking differently please"
    print("\n===== Sample Chatbot with Sample Data =====")
    print("Type 'quit' or 'exit' to end the conversation\n")
    while True:
        user = input("You: ")
        if user.lower() in ["quit", "exit"]:
            print("Bot: Goodbye!")
            break
        print(f"Bot: {get_response(user)}")

def healthcare_chatbot():
    print("\n===== Healthcare Chatbot =====")
    print("-" * 50)
    print("Bot: Hi! I'm here to help with health concerns. (type 'quit' to exit)")
    while True:
        user = input("You: ").lower().strip()
        if user == 'quit':
            print("Bot: Take care and stay healthy! Goodbye!")
            break
        elif user in ['hi', 'hello', 'hey']:
            print("Bot: Hello! How can I help with your health today?")
        elif 'how are you' in user:
            print("Bot: I'm functioning well, ready to help you with health advice!")
        elif 'your name' in user:
            print("Bot: I'm HealthBot, here to assist with your health concerns!")
        elif 'temperature' in user or 'fever' in user:
            try:
                temp = float(input("Bot: What is your body temperature in Cels? "))
                if temp > 37.5:
                    print(
                        "Bot: You may have a fever. Please rest and stay hydrated. visit a doctor if temperature persists.")
                elif temp < 35.0:
                    print("Bot: Your temperature seems low. Please keep warm and monitor your condition.")
                else:
                    print("Bot: Your temperature appears normal. That's good!")
            except ValueError:
                print("Bot: Please enter a valid number for temperature.")
        elif 'help' in user:
            print("Bot: I can help with fever assessment, general health queries, and basic medical information.")
        elif 'bye' in user or 'goodbye' in user:
            print("Bot: Stay healthy! Goodbye!")
            break
        else:
            print(
                "Bot: I'm a healthcarr assistant. You can ask me about fever, temperature, or general health concerns!")
if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("CHATBOT SELECTION MENU")
    print("=" * 50)
    print("1. Advanced Chatbot (with pattern matching and intents)")
    print("2. Sample Chatbot (with basic responses)")
    print("3. Healthcare Chatbot ")
    print("=" * 50)
    choice = int(input("Select option (1, 2, or 3): "))
    if choice == 1:
        bot = AdvancedChatbot()
        bot.start_chat()
    elif choice == 2:
        simple_combined_chatbot()
    elif choice == 3:
        healthcare_chatbot()
    else:
        print("Invalid option! Please select 1, 2, or 3.")