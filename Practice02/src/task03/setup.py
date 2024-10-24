from setuptools import find_packages, setup

package_name = 'task03'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/task03' + "/launch", ['launch/task03.launch']),
        ('share/task03' + '/config', ['config/task03.yaml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='NOTTODO: Package description',
    license='NOTTODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "service = task03.service:main"
        ],
    },
)
