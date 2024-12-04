from . import post_bp
from flask import render_template, abort, flash, redirect, url_for, session
from .forms import PostForm
from .utils import load_posts, save_posts
from .models import Post
from app import db

posts_path = 'app/posts/posts.json'

@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        category = form.category.data
        is_active = form.is_active.data
        publication_date = form.publish_date.data
        author = session.get('username', None)
        new_post = Post(
            title=title,
            content=content,
            category=category,
            is_active=is_active,
            posted=publication_date,
            author=author
        )
        db.session.add(new_post)
        db.session.commit()

        flash(f'Post {title} added successfully!', 'success')
        return redirect(url_for('.get_posts'))

    return render_template("add_post.html", form=form)


@post_bp.route('/')
def get_posts():
    posts = Post.query.order_by(Post.posted.desc()).all()
    return render_template("posts.html", posts=posts)


@post_bp.route('/<int:id>')
def detail_post(id):
    post = Post.query.get(id)
    return render_template("detail_post.html", post=post)

@post_bp.route('/delete/<int:id>')
def delete_post(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    flash(f'Post {post.title} deleted successfully!', 'success')
    return redirect(url_for('.get_posts'))

@post_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.get(id)
    form = PostForm(obj=post)
    form.publish_date.data = post.posted
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = form.is_active.data
        post.posted = form.publish_date.data
        db.session.commit()
        flash(f'Post {post.title} edited successfully!', 'success')
        return redirect(url_for('.get_posts'))
    return render_template("edit_post.html", form=form)
