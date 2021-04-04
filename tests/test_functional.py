
import os
from os.path import isfile, join
import json
import re

class TestFunctional:
	def test_hero_images_exist(self):
		missing_images = []
		hero_path = join(os.getcwd(), 'hero')
		img_path = join(os.getcwd(), 'images', 'heroes')

		for hero_file in [file for file in os.listdir(hero_path) if isfile(join(hero_path, file))]:
			with open(join(hero_path, hero_file), 'r') as file:
				hero_json = json.load(file)
			if not isfile(join(img_path, hero_json['icon'])):
				missing_images.append(hero_json['icon'])

		assert not missing_images, 'hero images missing:\n{}'.format('\n'.join(missing_images))

	def test_talent_images_exist(self):
		missing_images = []
		hero_path = join(os.getcwd(), 'hero')
		img_path = join(os.getcwd(), 'images', 'talents')

		for hero_file in [file for file in os.listdir(hero_path) if isfile(join(hero_path, file))]:
			with open(join(hero_path, hero_file), 'r') as file:
				hero_json = json.load(file)
			for d in [hero_json['abilities'], hero_json['talents']]:
				missing_images.extend(
					[a_t['icon'] for v in d.values() for a_t in v if not isfile(join(img_path, a_t['icon']))])

		assert not set(missing_images), 'talent images missing:\n{}'.format('\n'.join(set(missing_images)))

	def test_hero_in_readme(self):
		hero_path = join(os.getcwd(), 'hero')

		with open('README.md', 'r') as readme:
			readme_heroes = [line[31:-3] for line in readme if re.match('^<a class="img-wrap"', line)]
		hero_files = [file for file in os.listdir(hero_path) if isfile(join(hero_path, file))]

		assert not set(hero_files).difference(readme_heroes), 'heroes missing from README:\n{}'.format(
			'\n'.join(set(hero_files).difference(readme_heroes)))
		assert not set(readme_heroes).difference(hero_files), 'README heroes missing hero json:\n{}'.format(
			'\n'.join(set(readme_heroes).difference(hero_files)))