from flask_cors import CORS

def configure_cors(app):
    """
    Configuración detallada de CORS para la aplicación Flask
    """
    # Configuración CORS más específica y robusta
    CORS(app, 
         resources={
             r"/*": {
                 "origins": ["*"],  # Permite cualquier origen
                 "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
                 "allow_headers": [
                     "Content-Type", 
                     "Authorization", 
                     "X-Requested-With",
                     "Accept",
                     "Origin",
                     "Access-Control-Request-Method",
                     "Access-Control-Request-Headers"
                 ],
                 "expose_headers": [
                     "Content-Type",
                     "X-Total-Count",
                     "X-Page",
                     "X-Per-Page"
                 ],
                 "supports_credentials": True,
                 "max_age": 86400  # Cache preflight requests for 24 hours
             }
         }) 