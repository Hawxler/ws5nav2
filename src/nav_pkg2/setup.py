from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'nav_pkg2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # launch
        (os.path.join(
            'share', package_name, 'launch'
        ),
            glob('launch/*.launch.py')
            + glob('launch/*.launch.xml')
        ),
        # description
        (os.path.join(
            'share', package_name, 'description'
        ),
            glob('description/*')
        ),
        # worlds
        (os.path.join(
            'share', package_name, 'worlds'
        ),
            glob('worlds/*')
        ),
        # maps
        (os.path.join(
            'share', package_name, 'maps'
        ),
            glob('maps/*')
        ),
        # config
        (os.path.join(
            'share', package_name, 'config'
        ),
            glob('config/*')
        ),
        # rviz
        (os.path.join(
            'share', package_name, 'rviz'
        ),
            glob('rviz/*')
        ),
        
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hawx',
    maintainer_email='oppaha9@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
