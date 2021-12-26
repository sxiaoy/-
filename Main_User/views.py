import time

from Utils.tools import *
from Utils.network import *
from DataBase.models import *


def login(request):
    """用户登录"""
    request = post_request(request)
    user = User.objects.filter(user_username=request["username"], user_password=request["password"]).first()
    if user:
        return success(message="登陆成功")
    return fail(message="登陆失败,无此用户")


def test(request):
    time.sleep(60)
    print(request.headers)
    return success(data={"aa": "bb"})


def initialization(request):
    ShowUser(user_username='SY', user_img='https://img0.baidu.com/it/u=4032337027,2558925021&fm=26&fmt=auto&gp=0.jpg',
             user_type='躺尸中......', user_email='m18873925326@163.com', user_motto='希望自己能永远保持着一颗乐观的心').save()
    Article(article_title='修复 WordPress 5.1 评论回复按键失效问题（记一次痛苦的寻找bug之旅）', article_browse='0',
            article_image='https://shawnzeng.com/wp-content/uploads/2018/12/66568021_p0.jpg', article_hits='0',
            article_is_delete="0", article_content="""
            前几天在更新主题的时候，有童鞋LF112表示Memory主题升级到5.1之后，评论回复按钮会产生失效的问题，并给了我一个解决方案（修复 WordPress 5.1 评论回复按键失效问题）我简单看了下发现可行，于是就兴冲冲地换上了，结果LF112又告诉我评论回复是有效了，但是评论无法提交了(￣ε(#￣) Σ（我的内心是拒绝的）。
            于是我就开始了痛苦的寻找bug之旅，首先我把我的测试站点也升级到了wp5.1，测试了下评论功能，发现正常，说明不是版本的原因，然后我有看了下评论提示的代码，发现是由于评论状态为空的原因导致评论失败，于是就去其数据库里看了下对应文章的评论状态，发现也是没问题的。
            那么问题来了，问题到底在哪（╯‵□′）╯︵┴─┴?
            在LF112的站点，又切换到了其他主题试了一下，发现可以正常评论，说明是Memory的原因∠( ᐛ 」∠)＿，于是我又开始了漫漫的排查过程，最后在审查元素的时候，发现LF112评论提交的文章id都是1（黑人问号脸），于是我又去看了下我的PHP文件代码，没问题呀？最终怀疑到了新添加的解决评论回复按键失效问题的代码上。原博主给出的代码为：
            ``` js
            $('body').on('click', '.comment-reply-link', function(){
                addComment.moveForm( "comment-"+$(this).attr('data-commentid'), $(this).attr('data-commentid'), "respond", "1" );
                return false;  // 阻止 a tag 跳转，这句千万别漏了
            });
            ```
            在看到最后一个参数1的一瞬间，我感觉到了不对，这不是文章id吗？看了下moveForm函数，果然，于是便有了下面的代码：
            ``` js
            // 修复wp5.1评论回复bug
            $(document).on('click', '.comment-reply-link', function(){
                var postId = document.getElementById('comment_post_ID').value;
                addComment.moveForm( "comment-"+$(this).attr('data-commentid'), $(this).attr('data-commentid'), "respond", postId );
                return false;  // 阻止 a tag 跳转，这句千万别漏了
            });
            ```
            试了一下，果然没问题了，再想想之前我测试站没问题LF112站点有问题的原因，我的没有问题是因为我文章id为1的文章还在，LF112的有问题是因为他的那篇文章删了，而评论提交的文章id也是id为1的，该文章不存在，自然也就会报错了(-_-#)。
            虽然问题最终得到了解决，但这个故事告诉我们，用别人的代码也不要无脑用，好歹看懂了再用，这样来日找bug才不会这么吐血_(:3」∠)_
            """).save()
    Music(music_name='误红妆',
          music_img='http://127.0.0.1:8000/Static/Music/%E8%AF%AF%E7%BA%A2%E5%A6%86/%E8%AF%AF%E7%BA%A2%E5%A6%86.jpg',
          music_url='http://127.0.0.1:8000/Static/Music/%E8%AF%AF%E7%BA%A2%E5%A6%86/%E8%AF%AF%E7%BA%A2%E5%A6%86.mp3').save()
    return success()
