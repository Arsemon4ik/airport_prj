from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def main_page(request):
    """ Dashboard function returns a template with subjects and tasks from DB based on user """
    # articles = Article.objects.all().order_by('-id')
    return render(request, 'airport_app/main.html', context={})


@login_required()
def articles_by_user_page(request):
    """ Dashboard function returns a template with subjects and tasks from DB based on user """
    pass


@login_required()
def edit_article_page(request, article_id):
    """ Subject function returns a template with subjects and tasks from DB based on user """
    article = Article.objects.filter(id=article_id, user=request.user).first()

    form = ArticleForm(instance=article)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles_by_user')
        else:
            messages.error(request, f'Виникла помилка під час редагування, спробуйте ще раз\n{form.errors} ')
    return render(request, 'airport_app/edit_article.html', {'form': form, 'article': article})


@login_required()
def delete_article(request, article_id):
    """ Dashboard function returns a template with subjects and tasks from DB based on user """
    article = Article.objects.filter(id=article_id, user=request.user).first()
    if article:
        article.delete()
        return redirect('articles_by_user')
    else:
        return redirect('articles_by_user')
