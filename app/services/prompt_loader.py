from pathlib import Path

from jinja2 import Environment, FileSystemLoader

_prompts_dir = Path(__file__).resolve().parent.parent.parent / "prompts"
_env = Environment(loader=FileSystemLoader(str(_prompts_dir)))


def load_prompt(template_name: str, **variables: str) -> str:
    template = _env.get_template(template_name)
    return template.render(**variables)
