from setuptools import setup

setup(
    name='nominate',
    packages=['nominate'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
# from nominate import app
#
# if __name__ == "__main__":
#     app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config["DEBUG"])
