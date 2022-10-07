import firebase_admin

app = firebase_admin.initialize_app()

if __name__ == "__main__":
    print(app)