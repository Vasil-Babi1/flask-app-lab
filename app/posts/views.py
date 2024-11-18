from . import post_bp
from flask import render_template, abort, flash, redirect, url_for, session
from .forms import PostForm
from .utils import load_posts, save_posts

posts_path = 'app/posts/posts.json'

@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        posts = load_posts(posts_path)

        title = form.title.data
        content = form.content.data
        category = form.category.data
        is_active = form.is_active.data
        publication_date = form.publish_date.data
        author = session.get('username', "No author")
        new_post = {
            "id": len(posts) + 1,
            "title": title,
            "content": content,
            "category": category,
            "is_active": is_active,
            "publication_date": publication_date.strftime("%Y-%m-%d"),
            "author": author
        }
        posts.append(new_post)
        save_posts(posts_path, posts)
        flash(f'Post {title} added successfully!', 'success')
        return redirect(url_for('.get_posts'))

    return render_template("add_post.html", form=form)


@post_bp.route('/')
def get_posts():
    posts = load_posts(posts_path)
    return render_template("posts.html", posts=posts)


@post_bp.route('/<int:id>')
def detail_post(id):
    posts = load_posts(posts_path)
    if id < 1 or id > len(posts):
        abort(404)
    post = posts[id - 1]
    return render_template("detail_post.html", post=post)
