from django.shortcuts import render
import markdown
from math import ceil
from collections import Counter
from Blog import models
import jieba
import synonyms


def detail(request, article_id):
    try:
        article = models.Articles.objects.get(id=int(article_id))
    except:
        return render(request, 'blog/404.html', {'context': [dict(get_tags_dict()), ]})
    article.正文内容 = markdown.markdown(article.正文内容,
                                     extensions=[
                                         'markdown.extensions.extra',
                                         'markdown.extensions.codehilite',
                                         'markdown.extensions.toc',
                                     ])
    context = {'context': [dict(get_tags_dict()), article]}
    return render(request, 'blog/article_content.html', context)


def index(request):
    articles_num_per_page = 6
    articles_num = models.Articles.objects.count()
    total_page = ceil(articles_num / articles_num_per_page)
    page_num_need = request.GET.get('page')
    if type(page_num_need) != str:  # 需要更改为 为空时
        page_num_need = 1
    try:
        page_num_need = int(page_num_need)
    except:
        return render(request, 'blog/404.html', {'context': [dict(get_tags_dict()), ]})
    if page_num_need > total_page:
        return render(request, 'blog/404.html', {'context': [dict(get_tags_dict()), ]})
    articles = []

    if articles_num > articles_num_per_page:
        for id in range(0, articles_num_per_page):
            a = articles_num - (id + (page_num_need - 1) * articles_num_per_page)
            if a > 0:
                a = a
                article = models.Articles.objects.get(id=a)
                articles.append(article)
            else:
                break
    else:
        for id in range(1, articles_num + 1):
            id = id
            article = models.Articles.objects.get(id=int(id))
            articles.append(article)
    page_result = get_page_result(page_num_need, total_page)
    context = {'context': [dict(get_tags_dict()), articles, page_result, page_num_need, total_page, page_num_need - 1,
                           page_num_need + 1]}

    return render(request, 'blog/article_list.html', context)


def get_page_result(now, total):
    if now < 6 and total < (now + 5):
        return list(range(1, total + 1))

    elif now < 6 and total >= (now + 5):
        begin = list(range(1, now + 3))
        begin.append(0)
        begin.append(total - 1)
        begin.append(total)
        return begin

    elif now == total and total < 6:
        return list(range(1, total + 1))
    elif now == total and total >= 6:
        return [1, 2, 0, total - 2, total - 1, total]

    elif now == total - 1 and total < 7:
        return list(range(1, total + 1))
    elif now == total - 1 and total >= 7:
        return [1, 2, 0, total - 3, total - 2, total - 1, total]

    elif now == total - 2 and total < 8:
        return list(range(1, total + 1))
    elif now == total - 2 and total >= 8:
        return [1, 2, 0, total - 4, total - 3, total - 2, total - 1, total]

    elif now == total - 3 and total < 9:
        return list(range(1, total + 1))
    elif now == total - 3 and total >= 9:
        return [1, 2, 0, total - 5, total - 4, total - 3, total - 2, total - 1, total]

    elif now == total - 4 and total < 10:
        return list(range(1, total + 1))
    elif now == total - 4 and total >= 10:
        return [1, 2, 0, total - 6, total - 5, total - 4, total - 3, total - 2, total - 1, total]

    else:
        return [1, 2, 0, now - 2, now - 1, now, now + 1, now + 2, 0, total - 1, total]


def get_tags_dict():
    tags = models.Tag.objects.values('标签')
    tags_list = []
    for tag in tags:
        tags_list.append(tag['标签'])

    a = Counter(tags_list)
    return a


def search(request):
    keyword_search = request.GET.get('keyword')
    if len(keyword_search) == 0:
        keyword_search = "空"
        return render(request, 'blog/search_404.html', {'context': [dict(get_tags_dict()), keyword_search, ]})
    else:
        articles_match = []
        articles_num = models.Articles.objects.count()
        for i in range(1, articles_num + 1):
            article = models.Articles.objects.get(id=i)
            if match_judge(keyword_search, article):
                articles_match.append(article)

        articles_num_per_page = 6
        articles_num = len(articles_match)
        total_page = ceil(articles_num / articles_num_per_page)
        page_num_need = request.GET.get('page')
        if type(page_num_need) != str:  # 需要更改为 为空时
            page_num_need = 1
        try:
            page_num_need = int(page_num_need)
        except:
            return render(request, 'blog/404.html', {'context': [dict(get_tags_dict()), keyword_search, ]})
        if page_num_need > total_page:
            return render(request, 'blog/search_404.html', {'context': [dict(get_tags_dict()), keyword_search, ]})
        articles = []

        if articles_num > articles_num_per_page:
            for id in range(0, articles_num_per_page):
                a = articles_num - (id + (page_num_need - 1) * articles_num_per_page)
                if a > 0:
                    article = articles_match[a - 1]
                    articles.append(article)
                else:
                    break
        else:
            for id in range(0, articles_num):
                article = articles_match[id]
                articles.append(article)
        page_result = get_page_result(page_num_need, total_page)
        context = {'context': [dict(get_tags_dict()), articles, page_result,
                               page_num_need, total_page, page_num_need - 1,
                               page_num_need + 1, keyword_search]}

        return render(request, 'blog/search_result.html', context)


def match_judge(keyword, article):
    keyword_list = "/".join(jieba.cut(keyword, cut_all=True)).split('/')
    tags = models.Tag.objects.filter(contact_id=article.id)

    # 检查标签
    for key_word in keyword_list:
        for tag in tags:
            if synonyms.compare(key_word, tag.标签, seg=True) > 0.7:
                return True

    article_标题们 = "/".join(jieba.cut(article.文章标题, cut_all=True)).split('/')
    for key_word in keyword_list:
        for article_标题 in article_标题们:
            if synonyms.compare(key_word, article_标题, seg=True) > 0.7:
                return True

    article_摘要们 = "/".join(jieba.cut(article.文章摘要, cut_all=True)).split('/')
    for key_word in keyword_list:
        for article_摘要 in article_摘要们:
            if synonyms.compare(key_word, article_摘要, seg=True) > 0.7:
                return True
    return False


def tag(request):
    tag = request.GET.get('tag')
    total_tags = models.Tag.objects.count()
