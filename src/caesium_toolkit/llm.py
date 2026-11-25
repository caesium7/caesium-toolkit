_llm = None


def _get_model():
  global _llm
  if _llm is None:
    from llama_cpp import Llama
    _llm = Llama.from_pretrained(
        repo_id='Qwen/Qwen2.5-Math-1.5B-Instruct-GGUF',
        filename='qwen2.5-math-1.5b-instruct-q4_k_m.gguf',
        n_ctx=2048,
        verbose=False,
    )
  return _llm


def ask_ai(problem=None):
  if problem is None:
    problem = input('Enter your math problem or question: ')

  llm = _get_model()
  response = llm.create_chat_completion(
      messages=[
          {'role': 'system', 'content': 'You are a concise math tutor.'},
          {'role': 'user', 'content': problem},
      ],
      max_tokens=512,
      temperature=0.1,
  )
  answer = response['choices'][0]['message']['content'].strip()
  print(answer)
  return answer
