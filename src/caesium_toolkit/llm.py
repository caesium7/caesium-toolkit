import os
import re

try:
  from pylatexenc.latex2text import LatexNodes2Text

  _latex_converter = LatexNodes2Text()
except ImportError:
  _latex_converter = None

_llm = None


def _clean_latex(text: str) -> str:
  """Converts LaTeX math to readable plain text, with a zero-dependency fallback."""
  if _latex_converter is not None:
    return _latex_converter.latex_to_text(text).strip()

  # Fallback if pylatexenc is not installed
  text = re.sub(r'\\\[|\\\]|\\\(|\\\)|\$\$|\$', '', text)
  text = re.sub(r'\\boxed\{([^{}]+)\}', r'\1', text)
  text = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'(\1/\2)', text)
  text = re.sub(r'\\sqrt\{([^{}]+)\}', r'sqrt(\1)', text)
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
  }
  for k, v in replacements.items():
    text = text.replace(k, v)
  return re.sub(r'\n{3,}', '\n\n', text).strip()


def _get_model(n_ctx: int = 1024, n_gpu_layers: int = -1):
  """Lazy-loads the model once and adapts automatically to the user's hardware."""
  global _llm
  if _llm is None:
    from llama_cpp import Llama

    physical_cores = max(2, (os.cpu_count() or 4) // 2)
    _llm = Llama.from_pretrained(
        repo_id='bartowski/Qwen2.5-Math-1.5B-Instruct-GGUF',
        filename='*Q4_K_M.gguf',
        n_ctx=n_ctx,
        n_threads=physical_cores,
        n_batch=512,
        n_gpu_layers=n_gpu_layers,  # Uses GPU if available, otherwise falls back to CPU
        verbose=False,
    )
  return _llm


def ask_ai(
    problem: str | None = None,
    max_tokens: int = 400,
    quiet: bool = False,
) -> str:
  """Solves a math or calculus problem step-by-step in plain text.

  Args:
      problem: The math question. Prompts via input() if None.
      max_tokens: Maximum response length.
      quiet: If True, returns the string without printing to stdout.
  """
  if problem is None:
    problem = input('Enter your math problem or question: ').strip()
  if not problem:
    return ''

  llm = _get_model()
  response = llm.create_chat_completion(
      messages=[
          {
              'role': 'system',
              'content': 'Solve step-by-step concisely. Keep each step short.',
          },
          {'role': 'user', 'content': problem},
      ],
      max_tokens=max_tokens,
      temperature=0.1,
  )

  raw_answer = response['choices']['message']['content']
  answer = _clean_latex(raw_answer)

  if not quiet:
    print(answer)
  return answer
