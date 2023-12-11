import hashlib
import json
import os
import getpass
import random
import string

PASSWORD_FILE = "passwords.json"

def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

def load_passwords():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'r') as file:
            try:
                passwords = json.load(file)
            except json.JSONDecodeError:
                passwords = {}
    else:
        passwords = {}
    return passwords

def save_passwords(passwords):
    with open(PASSWORD_FILE, 'w') as file:
        json.dump(passwords, file, indent=4)

def generate_random_password():
    characters = string.ascii_letters + string.digits + '!@#$%^&*'
    password = ''.join(random.choice(characters) for _ in range(12))
    return password

def is_password_duplicate(passwords, hashed_password):
    return any(existing_password == hashed_password for existing_password in passwords.values())

def add_password(passwords, service):
    while True:
        generated_password = generate_random_password()
        hashed_generated_password = hash_password(generated_password)

        if not is_password_duplicate(passwords, hashed_generated_password):
            break

    print(f"Mot de passe généré pour {service} : {generated_password}")
    user_input = input("Voulez-vous utiliser ce mot de passe ? (o/n) : ")

    if user_input.lower() == 'o':
        passwords[service] = hashed_generated_password
        save_passwords(passwords)
        print(f"Mot de passe pour {service} ajouté avec succès.")
    else:
        print("Génération de mot de passe annulée.")

def display_passwords(passwords):
    if not passwords:
        print("Aucun mot de passe enregistré.")
    else:
        print("Mots de passe enregistrés :")
        for service, _ in passwords.items():
            print(f"{service}")

if __name__ == "__main__":
    passwords = load_passwords()

    while True:
        print("\n1. Ajouter un nouveau mot de passe")
        print("2. Afficher les mots de passe enregistrés")
        print("3. Quitter")

        choice = input("Choisissez une option (1/2/3) : ")

        if choice == "1":
            service = input("Entrez le nom du service : ")
            if service in passwords:
                print(f"Un mot de passe pour {service} est déjà enregistré.")
            else:
                add_password(passwords, service)
        elif choice == "2":
            display_passwords(passwords)
        elif choice == "3":
            break
        else:
            print("Option invalide. Veuillez réessayer.")