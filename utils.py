import openai
import time

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    success = False
    retry = 0
    max_retries = 30
    while retry< max_retries and not success:
      try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature, # this is the degree of randomness of the model's output
            )
        success = True
      except Exception as e:
        print(f"Error: {e}\nRetrying...")
        retry+=1
        time.sleep(0.5)

    return response.choices[0].message["content"]