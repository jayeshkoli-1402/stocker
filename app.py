import matplotlib
matplotlib.use('Agg')
from app import CREATE_APP

app = CREATE_APP()


if __name__ == '__main__':
    app.run(debug=True)