from setuptools import find_packages, setup


with open('README.md', 'rb') as f:
    LONG_DESCRIPTION = f.read().decode('utf-8')


setup(
    name="airflow-docker-notifier",
    version="0.1.0",
    description='A cli for notifying success and failure of airflow tasks.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='airflow airflow-docker slack notification notifier',
    url='https://github.com/airflowdocker/airflow-docker-notifier',
    license='MIT',
    author='Dan Cardin',
    author_email='ddcardin@gmail.com',
    package_dir={
        "": "src"
    },
    packages=find_packages("src"),
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
    install_requires=[
        "click==7.0",
        "slackclient==1.3.1",
    ],
    extras_require={
        'testing': [
            'pytest',
            'pytest-cov',
        ],
        'linting': [
            'isort',
            'black',
        ],
        'dev': [
            'releasely',
        ]
    },
    entry_points={
        'console_scripts': [
            'airflow-docker-notifier = airflow_docker_notifier.cli:main',
        ]
    },
)
