### External imports ###

import glob
import os
from fastapi import FastAPI, UploadFile, File, Request


### Internal imports ###

from brainsignals.utils import NII_to_3Darray
from brainsignals.model_class import Model


### Functions ###

description = """
Brain-Signals API

## Endpoints :

* **/** (_see API status_).
* **/list** (_see all avalaible models_).
* **/model** (_see settings of a selected model_).
* **/predict** (_select a model and make a prediction using a nifti file_).

## GitHub:

Complete documentation on [project's GitHub page](https://github.com/Brain-signals/Brain-Signals_api)
"""

app = FastAPI(title="Brain-Signals API",
              description=description,
              version="1.0.4")


@app.get("/")
def root(request : Request):
    endpoints = {'To view on model specs':f'{request.url}model?model_id=',
                 'To list all avalaible models':f'{request.url}list',
                 'To make a prediction':f'{request.url}predict',
                 'To access FastApi UI':f'{request.url}docs'}

    print('test')

    return {'API_status':'Running',
            'API documentation at':'https://github.com/Brain-signals/Brain-Signals_api',
            'avalaible endpoints': endpoints}


@app.get("/model")
def model(model_id, request : Request):
    try:
        my_modele = Model().load_model(model_id)
        return {'Model_id': my_modele.model_id,
                'Classes' : my_modele.number_of_classes,
                'Dimensions' : my_modele.dimensions,
                'Learning_rate' : my_modele.learning_rate,
                'Slicing_bot':my_modele.slicing_bot,
                'Slicing_top':my_modele.slicing_top,
                'Epochs': my_modele.epochs,
                'Best_epoch': my_modele.best_epoch,
                'Patience': my_modele.patience,
                'Monitor': my_modele.monitor,
                'Batch_size': my_modele.batch_size,
                'Validation_split':my_modele.validation_split,
                'Model_creator':my_modele.model_creator,
                'Creator_comment':my_modele.creator_comment
                }
    except AttributeError:
        return {'error':f'Model {model_id} not found, check available models :' +
                f' {str(request.url)[0:-6]}list'}


@app.get("/list")
def list(request : Request):
    model_list = {}
    for m in sorted(glob.glob(f'{os.environ.get("LOCAL_REGISTRY_PATH")}/*')):
        model_list[m[-20:]] = f'{str(request.url)[0:-5]}/model?model_id={m[-20:]}'
    return {'models_found':model_list}


@app.post("/predict")
async def upload_nii(model_id, request : Request, nii_file: UploadFile=File(...)):
    if not os.path.exists(os.path.join('brainsignals', 'tmp_files')):
        os.mkdir(os.path.join('brainsignals', 'tmp_files'))

    try:
        path = os.path.join('brainsignals', 'tmp_files', nii_file.filename)
        with open(path, 'wb') as f:
            nii_content = await nii_file.read()
            f.write(nii_content)

        vol = NII_to_3Darray(path)

        my_modele = Model().load_model(model_id)
        y_pred = my_modele.predict(vol)
        keys = [k for k, v in y_pred.items() if v > 0.5]

    except AttributeError:
        return {'error':f'Model {model_id} not found, check available models :' +
                f' {str(request.url)[0:-6]}list'}

    except Exception:
        return {'message':'There was an error uploading the file'}

    finally:
        await nii_file.close()
        os.remove(path)

    return keys
