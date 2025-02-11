import requests
import random
import time
import logging
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("chatbot.log"),
        logging.StreamHandler()
    ]
)

# Configuration
BASE_URL = "https://tweet-writer.gaia.domains"
MODEL = "qwen2-0.5b-instruct"
MAX_RETRIES = 100  # Essentially infinite retries
RETRY_DELAY = 5  # Seconds between retries
QUESTION_DELAY = 1  # Seconds between successful questions

QUESTIONS = [
    "What is no-code?",
    "Why use no-code for websites?",
    "Which no-code tools are popular for websites?",
    "What to look for in a no-code platform?",
    "How to start a no-code website?",
    "How to add pages in no-code?",
    "How to customize a no-code site's look?",
    "Can no-code integrate with other services?",
    "How to make a no-code site mobile-friendly?",
    "How to launch a site with no-code?",
    "Can no-code handle e-commerce?",
    "What are no-code platform limitations?",
    "How to manage SEO on a no-code site?",
    "Where to learn about no-code web building?",
    "Can professionals help with no-code websites?",
    "How much does no-code website building cost?",
    "Can I use custom domains with no-code?",
    "How to get support for no-code issues?",
    "How to update a no-code website?",
    "Examples of no-code built websites?",
    "What types of sites can no-code build?",
    "How to add custom code in no-code?",
    "How to add forms using no-code?",
    "What hosting options does no-code offer?",
    " What is the capital of France?",
" Who wrote Hamlet?",
" What is the largest ocean?",
" How many continents are there?",
" Who painted the Mona Lisa?",
" What is the tallest mountain in the world?",
" What year did World War II end?",
" Who discovered gravity?",
" What is the longest river in the world?",
" How many planets are in the solar system?",
" What is the smallest country in the world?",
" Who invented the telephone?",
" What is the chemical symbol for gold?",
" How many states are in the United States?",
" What is the fastest land animal?",
" What is the capital of Japan?",
" Who was the first president of the United States?",
" What is the hardest natural substance?",
" Who discovered America?",
" What is the largest desert in the world?",
" What is your favorite color?",
" Can you tell me a joke?",
" What’s the meaning of life?",
" Do you like pizza?",
" Can you dance?",
" What’s the best superpower?",
" If you could time travel, where would you go?",
" What’s your favorite movie?",
" Can you sing?",
" What’s the funniest word?",
" What is artificial intelligence?",
" How do computers learn?",
" What is machine learning?",
" Who created the first AI?",
" Can AI think like humans?",
" What is deep learning?",
" Do robots have emotions?",
" What is the Turing test?",
" Can AI write books?",
" Will AI replace jobs?",
" What is gravity?",
" How does the sun produce energy?",
" What is the speed of light?",
" What is DNA?",
" How do airplanes fly?",
" What is a black hole?",
" How far is the moon?",
" What are atoms made of?",
" What causes earthquakes?",
" What is the water cycle?",
" Can you feel emotions?",
" What do you think about humans?",
" Do you have dreams?",
" What is your purpose?",
" Do you have a favorite book?",
" What is the best advice you can give?",
" Can AI be creative?",
" What makes someone intelligent?",
" Do you believe in free will?",
" Can AI have consciousness?",
" What is Artificial Intelligence?",
" How does AI work?",
" What are the main types of AI?",
" What is the difference between AI and machine learning?",
" How is AI different from human intelligence?",
" What are the main goals of AI?",
" What are the applications of AI?",
" What is strong AI vs",
" How does AI impact our daily lives?",
" What are some examples of AI-powered devices?",
" What is machine learning?",
" How does supervised learning work?",
" What is the difference between supervised and unsupervised learning?",
" What is reinforcement learning?",
" What is deep learning?",
" How do neural networks work?",
" What are some popular machine learning algorithms?",
" What is overfitting in machine learning?",
" What is underfitting in machine learning?",
" What is a decision tree in machine learning?",
" What is natural language processing (NLP)?",
" How does NLP work?",
" What are some real-world applications of NLP?",
" What is sentiment analysis?",
" What is tokenization in NLP?",
" What are stop words in NLP?",
" What is the difference between stemming and lemmatization?",
" What is named entity recognition (NER)?",
" What are some common NLP models?",
" How does a chatbot use NLP?",
" What is computer vision?",
" How does image recognition work?",
" What is object detection?",
" What is facial recognition?",
" How does AI generate images?",
" What is image segmentation?",
" What is the difference between CNNs and RNNs?",
" What are some real-world applications of computer vision?",
" What is OCR (Optical Character Recognition)?",
" What datasets are used in computer vision?",
" What is a neural network?",
" What is the difference between a CNN and an RNN?",
" What is backpropagation?",
" What is a loss function in deep learning?",
" What is gradient descent?",
" What are activation functions in neural networks?",
" What is transfer learning?",
" What is dropout in deep learning?",
" What are some popular deep learning frameworks?",
" How does AI learn from data?",
" How is AI used in healthcare?",
" What are the benefits of AI in finance?",
" How does AI help in marketing?",
" How is AI used in e-commerce?",
" What are AI applications in cybersecurity?",
" How is AI transforming education?",
" What industries benefit the most from AI?",
" What is the role of AI in automation?",
" How does AI improve customer service?",
" What are the challenges of AI adoption in businesses?",
" What are the ethical concerns of AI?",
" How does AI impact privacy?",
" Can AI be biased?",
" How can we prevent AI bias?",
" What are the dangers of AI?",
" Will AI replace human jobs?",
" How can AI be regulated?",
" What is the impact of AI on society?",
" What are the risks of deepfake technology?",
" How can AI be made more ethical?",
" What is the future of AI?",
" How will AI change the job market?",
" Can AI become conscious?",
" Will AI surpass human intelligence?",
" What are the upcoming breakthroughs in AI?",
" What is AGI (Artificial General Intelligence)?",
" What are some futuristic applications of AI?",
" How will AI impact transportation?",
" How does AI influence scientific research?",
" What are some AI trends to watch in the next decade?",
" What is AI in robotics?",
" How do AI-powered robots work?",
" What are some real-world examples of AI in robotics?",
" What is the role of AI in industrial automation?",
" How is AI used in autonomous vehicles?",
" What are the challenges of AI in robotics?",
" What are some ethical concerns in AI-driven automation?",
" How does AI contribute to smart manufacturing?",
" What are some AI-powered robotic assistants?",
" How is AI revolutionizing supply chain management?",
" How is AI used in video games?",
" What are AI-generated characters in gaming?",
" How does AI improve NPC behavior?",
" What is procedural generation in AI gaming?",
" How do game developers use AI for storytelling?",
" How does AI enhance game difficulty adjustment?",
" What are AI-driven cheat detection systems?",
" How do reinforcement learning agents perform in games?",
" What is the future of AI in gaming?",
" Can AI create entire games on its own?",
    "How to create a landing page with no-code?",
    "How to ensure site accessibility with no-code?",
    "How to manage media in no-code?",
    "How to add a blog with no-code?",
    "Can no-code build business websites?",
    "How to add email forms with no-code?",
    "How to track analytics in no-code?",
    "Can no-code make a portfolio site?",
    "How to integrate social media with no-code?",
    "Can no-code be used for non-profits?",
    "How to add search functionality in no-code?",
    "How to secure a no-code website?",
    "How to publish a site with no-code?",
    "How to add payments with no-code?",
    "Can no-code make local business sites?",
    "How to optimize speed in no-code?",
    "How to add a favicon in no-code?",
    "How to add Google Maps with no-code?",
    "How to integrate email marketing in no-code?",
    "How to add reviews with no-code?",
    "How to add a contact form in no-code?",
    "Where to find no-code troubleshooting help?",
    "Can no-code create community websites?",
    "How to add a photo gallery with no-code?",
    "How to customize fonts with no-code?",
    "How to use no-code for app development?",
    "What are the benefits of no-code apps?",
    "What kinds of apps can no-code make?",
    "Which no-code platforms are best for apps?",
    "How to pick a no-code app platform?",
    "How to start designing an app with no-code?",
    "How to manage data in no-code apps?",
    "How to integrate services in no-code apps?",
    "How to customize app UI with no-code?",
    "How to manage users in no-code apps?",
    "How to secure no-code apps?",
    "How to authenticate users in no-code apps?",
    "How to test no-code apps?",
    "How to deploy no-code apps?",
    "How to migrate data in no-code apps?",
    "Can I add custom code to no-code apps?",
    "How to add user content in no-code apps?",
    "How to scale no-code apps?",
    "Can no-code make mobile apps?",
    "How to handle payments in no-code apps?",
    "How to send notifications in no-code apps?",
    "How to use push notifications in no-code?",
    "How to track usage in no-code apps?",
    "How to handle errors in no-code apps?",
    "How to gather feedback on no-code apps?",
    "How to integrate APIs in no-code apps?",
    "Where to learn more about no-code apps?",
    "How to manage databases in no-code apps?",
    "Can no-code make real-time apps?",
    "How to manage roles in no-code apps?",
    "How to ensure privacy in no-code apps?",
    "How to collaborate on no-code projects?",
    "How to backup no-code apps?",
    "How to maintain no-code apps?",
    "Can no-code make enterprise apps?",
    "How to integrate with other systems in no-code?",
    "How to link to social media in no-code apps?",
    "How to optimize no-code app performance?",
    "How to engage users in no-code apps?",
    "How to segment users in no-code apps?",
    "How to personalize no-code apps?",
    "How to onboard users in no-code apps?",
    "How to retain users in no-code apps?",
    "How to support users in no-code apps?",
    "How to integrate CRM in no-code apps?",
    "How to use marketing automation in no-code?",
    "How to localize no-code apps?",
    "How to comply with data laws in no-code?",
    "How to visualize data in no-code apps?",
    "How to manage file storage in no-code apps?",
    "How to manage tasks in no-code apps?"
]

def chat_with_ai(api_key: str, question: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    messages = [
        {"role": "user", "content": question}
    ]

    data = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7
    }

    for attempt in range(MAX_RETRIES):
        try:
            logging.info(f"Attempt {attempt+1} for question: {question[:50]}...")
            response = requests.post(
                f"{BASE_URL}/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]

            logging.warning(f"API Error ({response.status_code}): {response.text}")
            time.sleep(RETRY_DELAY)

        except Exception as e:
            logging.error(f"Request failed: {str(e)}")
            time.sleep(RETRY_DELAY)

    raise Exception("Max retries exceeded")

def run_bot(api_key: str):
    while True:  # Outer loop to repeat the questions indefinitely
        random.shuffle(QUESTIONS)
        logging.info(f"Starting chatbot with {len(QUESTIONS)} questions in random order")

        for i, question in enumerate(QUESTIONS, 1):
            logging.info(f"\nProcessing question {i}/{len(QUESTIONS)}")
            logging.info(f"Question: {question}")

            start_time = time.time()
            try:
                response = chat_with_ai(api_key, question)
                elapsed = time.time() - start_time

                # Print the entire response
                print(f"Answer to '{question[:50]}...':\n{response}")

                logging.info(f"Received full response in {elapsed:.2f}s")
                logging.info(f"Response length: {len(response)} characters")

                # Ensure the script waits for the full response before proceeding
                time.sleep(QUESTION_DELAY)  # Wait before asking next question

            except Exception as e:
                logging.error(f"Failed to process question: {str(e)}")
                continue

def main():
    print("Title: GaiaAI Chatbot")
    print("Twitter: https://twitter.com/abe_sten")
    api_key = input("Enter your API key: ")
    run_bot(api_key)

if __name__ == "__main__":
    main()
