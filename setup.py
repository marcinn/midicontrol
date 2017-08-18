from setuptools import setup

setup(name='midicontrol',
      version='0.1',
      description='Control any application shortcuts with midi controller',
      url='http://github.com/marcinn/midicontrol',
      author='Marcin Nowak',
      author_email='marcin.j.nowak@gmail.com',
      license='BSD',
      packages=['midicontrol'],
      scripts=['bin/midicontrol'],
      include_package_data=True,
      package_data = {
          'midicontrol': ['data/devices/*.ini'],
          },
      zip_safe=False)
