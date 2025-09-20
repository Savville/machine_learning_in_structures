from setuptools import setup, find_packages

setup(
    name='soil-xgboost-regression',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A machine learning project for regression analysis on soil dataset using XGBoost.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pandas',
        'numpy',
        'xgboost',
        'scikit-learn',
        'matplotlib',
        'seaborn',
        'shap'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)