from discord import Option
from g4f.models import Model

INFO_TEXT = '''- Создан `@kerherr`-ом на основе проекта GPT4Free.
- Пока что не поддерживает продолжение разговора.
**Модели**
- GPT 3.5 Turbo - оригинал, по умолчанию
- Falcon 7B - быстрая
- Falcon 40B - медленнее, но лучше
- LLama 13B - что-то среднее'''

MODELS = [Model.gpt_35_turbo.name, Model.falcon_40b.name, Model.falcon_7b.name, Model.llama_13b.name]