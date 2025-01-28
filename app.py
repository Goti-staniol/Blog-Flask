from flask import Flask, render_template, request

app = Flask(__name__)

registered_users = {}

has_posts = True

@app.route('/', methods=['GET', 'POST'])
def register():
    # if request.method == 'POST':
    #     username = request.form.get('username')
    #     email = request.form.get('email')
    #     password = request.form.get('password')
    #
    #     if username in registered_users:
    #         return "User already exists! Please log in."
    #
    #     registered_users[username] = {"email": email, "password": password}
    #     print(f"Registered users: {registered_users}")
    #     return f"User {username} registered successfully!"

    if has_posts:
        return render_template('available_posts_main.html')

    return render_template('no_posts_main.html')

if __name__ == '__main__':
    app.run(debug=True)
