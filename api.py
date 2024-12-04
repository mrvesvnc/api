from flask import Flask, jsonify, request, render_template, url_for, redirect
import requests

app = Flask(__name__, template_folder='.')

# Örnek kullanıcı veritabanı
users = [
    {"id": 1, "name": "Merve", "age": 21, "email": "merve@example.com"},
    {"id": 2, "name": "Taha", "age": 22, "email": "taha@example.com"}
]


@app.route("/")
def home():
    print("WELCOME HOME PAGE")
    return render_template("template.html", users=users)

# Kullanıcıyı eklemek için bir POST isteği
@app.route("/add_user", methods=["POST"])
def add_user():
    # Kullanıcı formdan alınan veriyi işliyoruz
    name = request.form.get("name")
    age = request.form.get("age")
    email = request.form.get("email")

    if name and age and email:
        new_user = {
            "id": len(users) + 1,
            "name": name,
            "age": int(age),
            "email": email
        }
        users.append(new_user)
        return jsonify({"message": "User added successfully", "user": new_user}), 201
    else:
        return jsonify({"error": "Missing user data"}), 400


# Show All Users route
@app.route("/show_users", methods=["GET"])
def show_users():
    print("SHOWING ALL USERS")
    # Pass the list of users to the template
    return render_template("template.html", users=users)


@app.route("/delete_user/<int:user_id>", methods=["GET"])
def delete_user(user_id):
    global users
    print(f"DELETING USER WITH ID: {user_id}")

    # Find the user with the given ID, and delete it if exists
    user_to_delete = next((user for user in users if user['id'] == user_id), None)

    if user_to_delete:
        # User found, delete it
        users = [user for user in users if user['id'] != user_id]
        print(f"User {user_to_delete['name']} deleted.")
    else:
        # User not found
        print(f"User with ID {user_id} not found.")

    # Redirect back to the home page after deletion
    return jsonify({"message": "User deleted successfully", "user id": user_id}), 201

@app.route("/")
def index():
    return render_template("template.html", users=users)

# Kullanıcıyı güncelleme
@app.route("/update_user/<int:user_id>", methods=["GET", "POST"])
def update_user(user_id):
    user_to_update = next((user for user in users if user["id"] == user_id), None)

    if request.method == "POST":
        # Form verilerini alıp güncelleme
        user_to_update["name"] = request.form["name"]
        user_to_update["age"] = int(request.form["age"])
        user_to_update["email"] = request.form["email"]
        return redirect(url_for("index"))

    return render_template("template.html", user_to_update=user_to_update, users=users)


# Flask uygulaması
if __name__ == "__main__":
    # Sunucuyu bir thread üzerinde çalıştırın ki test fonksiyonu paralel çalışabilsin
    app.run(debug='True')
