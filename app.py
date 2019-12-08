from src.services.search_service import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1998, debug=True)
