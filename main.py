from website import create_app #__init__.py makes folder a python package

app = create_app()

if __name__ == '__main__': #only if we run THIS file will the app run
    app.run(debug=True) #everytime you make a change, the web server re-runs

