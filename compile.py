"""
	This program compiles the static blog

"""

from jinja2 import Environment, FileSystemLoader, select_autoescape
import codecs
import os
import json
import markdown
from datetime import datetime
import PyRSS2Gen

class TemplateEngine:
	def __init__(self):
		self.env = Environment(
			loader = FileSystemLoader("templates"),
			autoescape = select_autoescape([])
		)

	def get_template(self, name):
		return self.env.get_template(name)


class PostLoader:
	def __init__(self, folder):
		self.folder = folder

	def load_posts(self):
		posts = []
		for file in os.listdir(self.folder):
			if not os.path.isfile(self.folder + "/" + file):
				continue
			with open(self.folder + "/" + file, "r") as stream:
				post_data = json.load(stream)
				posts.append(Post(post_data["title"], post_data["date"], post_data["content_file"], post_data["author"]))

		return posts

class Post:
	def __init__(self, title, date, content_md_filename, author):
		self.title = title
		self.date = date
		self.datetime = datetime.strptime(self.date, "%d-%m-%Y")
		self.content_md_filename = content_md_filename
		self.author = author
		self.load_content()

	def load_content(self):
		content_md = ""
		with codecs.open(self.content_md_filename, "r", "utf8") as md_file:
			content_md = md_file.read()
		self.content_md = content_md
		self.content_html = markdown.markdown(content_md, extensions=["codehilite", "mdx_math"])

	def get_link(self):
		words = self.title.lower().split(" ")
		return self.date + "-" + "-".join(words)

	def get_full_link(self):
		return "https://ekardnam.github.io/posts/{}.html".format(self.get_link())

class PostCompiler:
	def __init__(self, folder, template_engine, post_template_name):
		self.folder = folder
		self.template_engine = template_engine
		self.post_template = template_engine.get_template(post_template_name)

	def compile_post(self, post):
		with codecs.open(self.folder + "/" + post.get_link() + ".html", "w", "utf8") as output:
			output.write(self.post_template.render(post = post))

if __name__ == "__main__":
	template_engine = TemplateEngine()
	index_template = template_engine.get_template("index.html")
	archives_template = template_engine.get_template("archives.html")

	post_loader = PostLoader("_posts")
	posts = post_loader.load_posts()
	posts.sort(key=lambda post: post.datetime, reverse=True)

	with codecs.open("index.html", "w", "utf8") as index_file:
		index_file.write(index_template.render(posts = posts[:3]))

	with codecs.open("archives.html", "w", "utf8") as archives_file:
		archives_file.write(archives_template.render(posts = posts))

	post_compiler = PostCompiler("posts", template_engine, "post.html")

	rss = PyRSS2Gen.RSS2(
		title = "ekardnam's blog",
		link = "https://ekardnam.github.io",
		description = "Latest posts from ekardnam's blog",
		lastBuildDate = datetime.now(),
		items = [PyRSS2Gen.RSSItem(
			title = p.title,
			link = p.get_full_link(),
			description = p.content_md[:20],
			guid = PyRSS2Gen.Guid(p.get_full_link()),
			pubDate = p.datetime
		) for p in posts]
	)

	with open("rss.xml", "w") as f:
		rss.write_xml(f)

	for post in posts:
		post_compiler.compile_post(post)
