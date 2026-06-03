from jinja2 import Environment, BaseLoader, TemplateSyntaxError

class ConfigTemplater:
    def __init__(self):
        # Используем базовый загрузчик, так как шаблоны берем из строки, а из файлов
        self.env = Environment(loader=BaseLoader())

    def render_config(self, template_str: str, variables: dict) -> str:
        try:
            template = self.env.from_string(template_str)
            return template.render(**variables)
        except TemplateSyntaxError as e:
            raise ValueError(f"Ошибка синтаксиса шаблона: {e}")
        except Exception as e:
            raise ValueError(f"Ошибка рендеринга: {e}")

# Экземпляр класса для использования в API
templater_service = ConfigTemplater()
