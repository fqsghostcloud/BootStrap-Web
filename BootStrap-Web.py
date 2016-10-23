from apps import create_app
from apps.models.User import login_manager

app = create_app('videodata')

if __name__ == '__main__':
    app.secret_key = "super secret key"
    login_manager.init_app(app)

    app.run(debug=True)
