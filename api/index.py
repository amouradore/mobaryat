from app import app

# Export Flask app pour Vercel
application = app

# Pour Vercel Serverless Functions
def handler(request):
    return application(request)
