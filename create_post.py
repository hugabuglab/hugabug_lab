import os
from datetime import datetime

def create_post():
    title = input("Enter post title: ")
    date_str = input("Enter post date (YYYY-MM-DD), or press Enter for today's date: ")
    content = input("Enter post content:\n")

    if date_str:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    else:
        date = datetime.now()

    filename = f"{date.strftime('%Y-%m-%d')}-{title.lower().replace(' ', '-')}.md"
    filepath = os.path.join("_posts", filename)

    with open(filepath, 'w') as f:
        f.write("---\n")
        f.write(f"layout: post\n")
        f.write(f"title: \"{title}\"\n")
        f.write(f"date: {date.strftime('%Y-%m-%d')}\n")
        f.write("---\n\n")
        f.write(content)

    print(f"Post created: {filepath}")
    return filepath

if __name__ == "__main__":
    new_post_path = create_post()
    print(f"\nPost has been created at: {new_post_path}")
    print("Please review the file contents before committing and pushing.")