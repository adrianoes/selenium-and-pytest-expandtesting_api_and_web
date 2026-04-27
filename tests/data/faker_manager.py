from faker import Faker

fake = Faker()

def generate_user_data():
    return {
        "user_name": fake.name(),
        "user_email": fake.lexify(text='??').lower() + fake.company_email().replace("-", ""),
        "user_password": fake.password(length=12, special_chars=False, digits=True, upper_case=True, lower_case=True),
        "company": fake.company()[:24],
        "phone": fake.bothify(text='############'),
        "token": None
    }

def generate_note_data():
    return {
        "title": fake.sentence(4),
        "description": fake.sentence(5),
        "category": fake.random_element(elements=("Home", "Personal", "Work")),
    }

def generate_note_update_data():
    return {
        "title": fake.sentence(4),
        "description": fake.sentence(5),
        "completed": fake.boolean(),
    }

def generate_password():
    return fake.password(length=12, special_chars=False, digits=True, upper_case=True, lower_case=True)
