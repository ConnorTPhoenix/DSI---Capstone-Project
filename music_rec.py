import flask
import pickle
import numpy as np
app = flask.Flask(__name__)

with open('linear_model.pkl', 'r') as picklefile:
    PREDICTOR = pickle.load(picklefile)


@app.route('/predict', methods=["GET"])
def predict():
    LotArea = flask.request.args['LotArea']
    OverallQual = flask.request.args['OverallQual']
    OverallCond = flask.request.args['OverallCond']
    YearBuilt = flask.request.args['YearBuilt']
    YearRemodAdd = flask.request.args['YearRemodAdd']
    GrLivArea = flask.request.args['GrLivArea']
    FullBath = flask.request.args['FullBath']
    HalfBath = flask.request.args['HalfBath']
    BedroomAbvGr = flask.request.args['BedroomAbvGr']
    KitchenAbvGr = flask.request.args['KitchenAbvGr']
    YrSold = flask.request.args['YrSold']
    item = [LotArea,  OverallQual,  OverallCond, YearBuilt,
       YearRemodAdd, GrLivArea, FullBath, HalfBath,
       BedroomAbvGr, KitchenAbvGr, YrSold]
    price = PREDICTOR.predict(item)
    results = {'Price': price[0]}
    return flask.jsonify(results)

@app.route('/page')
def page():
   with open("page.html", 'r') as viz_file:
       return viz_file.read()

@app.route('/result', methods=['POST', 'GET'])
def result():
    '''Gets prediction using the HTML form'''
    if flask.request.method == 'POST':
       inputs = flask.request.form
       LotArea = inputs['LotArea']
       OverallQual = inputs['OverallQual']
       OverallCond = inputs['OverallCond']
       YearBuilt = inputs['YearBuilt']
       YearRemodAdd = inputs['YearRemodAdd']
       GrLivArea = inputs['GrLivArea']
       FullBath = inputs['FullBath']
       HalfBath = inputs['HalfBath']
       BedroomAbvGr = inputs['BedroomAbvGr']
       KitchenAbvGr = inputs['KitchenAbvGr']
       YrSold = inputs['YrSold']
       item = [np.log(float(LotArea)),  OverallQual,  OverallCond, YearBuilt,
         YearRemodAdd, np.log(float(GrLivArea)), FullBath, HalfBath,
         BedroomAbvGr, KitchenAbvGr, YrSold]
       item = map(lambda x: float(x), item)
       item = np.array(item)
       price = PREDICTOR.predict(item)
       results = {'Price': price[0]}
       return flask.jsonify(results)

if __name__ == '__main__':
    '''Connects to the server'''
    HOST='127.0.0.1'
    PORT = '4000'

    app.run(HOST, PORT)
