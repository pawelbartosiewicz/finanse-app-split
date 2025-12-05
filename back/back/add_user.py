from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash
from datetime import datetime

# --- KONFIGURACJA DANYCH UŻYTKOWNIKA ---
USERNAME = "admin123"
HASLO = "admin123"
EMAIL = "test@test.test"
# ---------------------------------------

app = create_app()

with app.app_context():
    if User.query.filter_by(username=USERNAME).first():
        print(f"❌ Błąd: Użytkownik z mailem {USERNAME} już istnieje!")
        exit()

    hashed_password = generate_password_hash(HASLO)

    new_user = User(
        username=USERNAME,
        password_hash=hashed_password,  
        created_at=datetime.now(),
        email=EMAIL
    )

    # 4. Dodaj do bazy
    try:
        db.session.add(new_user)
        db.session.commit()
        print
    except Exception as e:
        db.session.rollback()
        print(f"Wystąpił błąd bazy danych: {e}")