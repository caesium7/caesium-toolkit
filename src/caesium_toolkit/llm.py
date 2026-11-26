import os
import re

_llm = None


def _clean_latex(text: str) -> str:
  """Lightly cleans stray LaTeX delimiters without mangling exponents or fractions."""
  text = re.sub(r'\\\[|\\\]|\\\(|\\\)|\$\$|\$', '', text)
  text = re.sub(r'\\boxed\{([^{}]+)\}', r'\1', text)
  text = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'(\1/\2)', text)
  text = re.sub(r'\\sqrt\{([^{}]+)\}', r'sqrt(\1)', text)
  text = re.sub(r'([\^_])\{([^{}]+)\}', r'\1\2', text)

  replacements = {
      r'\int': '∫',
      r'\infty': '∞',
      r'\pi': 'π',
      r'\theta': 'θ',
      r'\cdot': '*',
      r'\times': '*',
      r'\pm': '±',
      r'\leq': '≤',
      r'\geq': '≥',
      r'\neq': '≠',
      r'\approx': '≈',
      r'\left': '',
      r'\right': '',
      r'\text': '',
  }
  for k, v in replacements.items():
    text = text.replace(k, v)
  return text


def _get_model(n_ctx: int = 2048, n_gpu_layers: int = 0):
  """Lazy-loads the model once. Set n_gpu_layers=-1 if you have a CUDA/Metal GPU."""
  global _llm
  if _llm is None:
    from llama_cpp import Llama

    _llm = Llama.from_pretrained(
        repo_id='bartowski/Qwen2.5-Math-1.5B-Instruct-GGUF',
        filename='*Q4_K_M.gguf',
        n_ctx=n_ctx,
        n_threads=os.cpu_count() or 4,
        n_gpu_layers=n_gpu_layers,
        verbose=False,
    )
  return _llm


def ask_ai(
    problem: str | None = None,
    max_tokens: int = 1024,
    quiet: bool = False,
) -> str:
  """Solves a math problem step-by-step with real-time streaming output."""
  if problem is None:
    problem = input('Enter your math problem or question: ').strip()
  if not problem:
    return ''

  llm = _get_model()
  stream = llm.create_chat_completion(
      messages=[
          {
              'role': 'system',
              'content': (
                  'Solve step-by-step clearly. Use plain text math notation '
                  '(like x^2, sqrt(x), and a/b) instead of LaTeX.'
              ),
          },
          {'role': 'user', 'content': problem},
      ],
      max_tokens=max_tokens,
      temperature=0.1,
      stream=True,
  )

  chunks = []
  for chunk in stream:
    delta = chunk['choices'][0]['delta'].get('content', '')
    if delta:
      chunks.append(delta)
      if not quiet:
        print(delta, end='', flush=True)

  if not quiet:
    print()

  return _clean_latex(''.join(chunks)).strip()
