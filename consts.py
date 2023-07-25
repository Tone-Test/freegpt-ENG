from discord import Option
from g4f.models import Model

VERSION = '1.2'

INFO_TEXT = '''- Created by `@kerherr` based on the GPT4Free project.
- Supports conversation continuation.
**Models**
- GPT 3.5 Turbo - original, default
- Falcon 7B - fast
- Falcon 40B - slower, but better
- LLama 13B - something in between'''

MODELS = [Model.gpt_35_turbo.name, Model.falcon_40b.name, Model.falcon_7b.name, Model.llama_13b.name]
DEFAULT_MODEL = Model.gpt_35_turbo

STORAGE = 'storage/'
