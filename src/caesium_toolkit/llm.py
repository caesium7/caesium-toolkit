import os
import re
import warnings

warnings.filterwarnings("ignore", message=".*local_dir_use_symlinks.*")
os.environ.setdefault("HF_HUB_VERBOSITY", "error")

_llm = None


def _clean_latex(text: str) -> str:
  """Converts LaTeX math to clean plain text without mangling exponents."""
  text = re.sub(r"\\\[|\\\]|\\\(|\\\)|\$\$|\$", "", text)
  text = re.sub(r"\\boxed\{([^{}]+)\}", r"\1", text)
  text = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"(\1/\2)", text)
  text = re.sub(r"\\sqrt\{([^{}]+)\}", r"sqrt(\1)", text)
  text = re.sub(r"\\text\{([^{}]+)\}", r"\1", text)
  text = re.sub(r"([\^_])\{([^{}]+)\}", r"\1\2", text)

  replacements = {
      r"\qquad": "  ",
      r"\quad": " ",
      r"\int": "∫",
      r"\infty": "∞",
      r"\pi": "π",
      r"\theta": "θ",
      r"\cdot": "*",
      r"\times": "*",
      r"\pm": "±",
      r"\leq": "≤",
      r"\geq": "≥",
      r"\neq": "≠",
      r"\approx": "≈",
      r"\left": "",
      r"\right": "",
  }
  for k, v in replacements.items():
    text = text.replace(k, v)
  return re.sub(r"\n{3,}", "\n\n", text)


def _get_model(n_ctx: int = 2048, n_gpu_layers: int = 0):
  global _llm
  if _llm is None:
    from llama_cpp import Llama

    _llm = Llama.from_pretrained(
        repo_id="bartowski/Qwen2.5-Math-1.5B-Instruct-GGUF",
        filename="*Q4_K_M.gguf",
        n_ctx=n_ctx,
        n_threads=os.cpu_count() or 4,
        n_gpu_layers=n_gpu_layers,
        verbose=False,
    )
  return _llm


def ask_ai(
    problem: str | None = None,
    max_tokens: int = 1500,
) -> None:
  """Solves a math problem step-by-step with live cleaned streaming output."""
  if problem is None:
    problem = input("Enter your math problem or question: ").strip()
  if not problem:
    return

  llm = _get_model()
  stream = llm.create_chat_completion(
      messages=[
          {
              "role": "system",
              "content": (
                  "Solve concisely step-by-step. Use plain text math "
                  "(e.g., x^2, sqrt(x), a/b) and NEVER use LaTeX delimiters."
              ),
          },
          {"role": "user", "content": problem},
      ],
      max_tokens=max_tokens,
      temperature=0.1,
      stream=True,
  )

  raw_chunks = []
  printed_len = 0

  for chunk in stream:
    delta = chunk["choices"][0]["delta"].get("content", "")
    if delta:
      raw_chunks.append(delta)
      cleaned_so_far = _clean_latex("".join(raw_chunks))
      safe_end = len(cleaned_so_far)
      last_backslash = cleaned_so_far.rfind("\\")
      if last_backslash != -1 and len(cleaned_so_far) - last_backslash < 15:
        safe_end = last_backslash

      if safe_end > printed_len:
        print(cleaned_so_far[printed_len:safe_end], end="", flush=True)
        printed_len = safe_end

  final_answer = _clean_latex("".join(raw_chunks)).strip()
  if len(final_answer) > printed_len:
    print(final_answer[printed_len:], end="", flush=True)
  print()
