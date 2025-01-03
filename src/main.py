from flask import Flask
from src.utils import format_with_grouping, friendlytimestamp, friendly_calendar, basename_filter, template_folder, \
    static_folder


def create_app(config):
    """Application factory for creating the Flask app."""
    app = Flask(__name__)
    app.template_folder = template_folder()
    app.static_folder = static_folder()
    app.config['BASE_URK'] = 'https://lickthecat.uk'
    app.config['SECRET_KEY'] = config.SECRET_KEY

    # Application configuration
    with app.app_context():
        from src.routes.home import home_route
        app.register_blueprint(home_route)
        pass

        return app
