from flask import Flask,jsonify
import config

from app import create_app


app = create_app()

# app.config.from_object(config)
# app.register_blueprint(user_bp)

# CORS(app, resources={r'/*': {'origins': '*'}})

#
# if __name__ == '__main__':
#     app.run()
