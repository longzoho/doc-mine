import os
import sys

import connexion
from dotenv import load_dotenv

from util import FirebaseUtils

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api('swagger.yaml', arguments={'title': 'Doc Mine API'})


if __name__ == '__main__':
    load_dotenv()
    FirebaseUtils.firebase_initialize()
    # Get the secret key from the environment variable
    app.app.secret_key = os.getenv("APP_SECRET_KEY")
    app.run(debug=True)
