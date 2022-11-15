import os
from pygments.lexers import (PythonLexer, CLexer, CppLexer, JavaLexer, CssLexer, JavascriptLexer, HtmlDjangoLexer, CSharpLexer)

class SyntaxAndThemes:

		def __init__(self, master):

			self.master = master

			self.monokai_theme_path = master.parent.loader.resource_path(
				os.path.join('data', 'theme_configs/monokai.yaml'))
			self.dark_theme_path = master.parent.loader.resource_path(
				os.path.join('data', 'theme_configs/dark.yaml'))
			self.desert_theme_path = master.parent.loader.resource_path(
				os.path.join('data', 'theme_configs/desert.yaml'))

		def load_default(self):
			self.master.load_new_theme(self.default_theme_path)

		def load_monokai(self):
			self.master.load_new_theme(self.monokai_theme_path)

		def load_dark(self):
			self.master.load_new_theme(self.dark_theme_path)

		def load_desert(self):
			self.master.load_new_theme(self.desert_theme_path)

		def load_csharp_syntax(self):
			self.master.lexer = CSharpLexer()
			self.master.initial_highlight()

		def load_python3_syntax(self):
			self.master.lexer = PythonLexer()
			self.master.initial_highlight()
            
		def load_c_syntax(self):
			self.master.lexer = CLexer()
			self.master.initial_highlight()

		def load_javascript_syntax(self):
			self.master.lexer = JavascriptLexer()
			self.master.initial_highlight()

		def load_cpp_syntax(self):
			self.master.lexer = CppLexer()
			self.master.initial_highlight()

		def load_html_syntax(self):
			self.master.lexer = HtmlDjangoLexer()
			self.master.initial_highlight()

		def load_css_syntax(self):
			self.master.lexer = CssLexer()
			self.master.initial_highlight()

		def load_java_syntax(self):
			self.master.lexer = JavaLexer()
			self.master.initial_highlight()


		# pt: loading themes from settings file
		def load_theme_from_config(self):
			theme = self.master.parent.loader.load_settings_data()["theme"]
			self.master.load_new_theme(theme)

		def save_theme_to_config(self, path):
			loader = self.master.parent.loader
			data = loader.load_settings_data()
			data["theme"] = path

			loader.store_settings_data(data)
