from flask import Flask, request, render_template, redirect, session, url_for
import pymysql
import os
import json
import hashlib
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # 配置session的secret_key
base_dir = os.path.abspath(os.path.dirname('__file__'))


# 获取数据库连接
def get_conn():
    conn = pymysql.connect(host='127.0.0.1',
                           port=3306,
                           user='root',
                           passwd='123456',
                           charset='utf8',
                           db='ew')
    return conn


@app.route('/')
def index():
    user = session.get('user')
    return render_template('index.html', user=user)


# 统一定义拦截器
@app.before_request
def before_request():
    # 如果访问登录注册或者是静态资源，放行
    allow_path = ('/', '/goto_login', '/goto_reg', '/user_login', '/regist', '/first_page','/favicon.ico', '/sortByType')
    if request.path in allow_path or re.match(r'^(/static/)|(/video/)*[.][a-z]*$', request.path):
        return None
    user = session.get('user')
    if user:
        return None
    return redirect('/goto_login')


@app.route('/goto_upload')
def goto_upload():
    return render_template('upload.html')

# 跳转到登录页面
@app.route('/goto_login')
def goto_login():
    return render_template('login.html')

#  登陆页面跳转注册
@app.route('/goto_reg')
def goto_regist():
   return render_template('regist.html')

# 实现登录
@app.route('/user_login', methods=['POST'])
def login():
    user_name = request.form.get('user_name')
    user_pass = request.form.get('user_pass')
    msg = "登录失败"
    print(user_name,user_pass)

    # md5加密密码后校验
    m = hashlib.md5()
    m.update(user_pass.encode(encoding='utf-8'))
    md5_pass = m.hexdigest()
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("select uid,uname from user where uname='%s' and upass='%s'" % (user_name, md5_pass))
        user_info = cur.fetchone()
        print(user_info)

    except Exception as e:
        print(e)
        return msg
    finally:
        cur.close()
        conn.close()
    
    # 登录成功将用户ID和用户名存入session
    if user_info:
        session['user'] = user_info
        msg = "登录成功"
        return render_template('index.html',user=session['user'])
    else:
        msg = "登录失败"
        return msg

# 退出登录
@app.route('/unlogin', methods=['GET'])
def unlogin():
    del session['user']
    return redirect(url_for('index'))

# 实现注册
@app.route('/regist', methods=['post'])
def regist():
    reg_name = request.form.get('regist_name')
    reg_pass = request.form.get('regist_pass')
    msg = "注册失败"
    try:
        conn=get_conn()
        cur=conn.cursor()
        
        # md5对密码进行加密
        m = hashlib.md5()
        m.update(reg_pass.encode(encoding='utf-8'))
        m_pass = m.hexdigest()
        print(reg_name,m_pass)
        cur.execute("insert into user(uname, upass) values('%s','%s')" %(reg_name, m_pass))
        conn.commit()
        msg = "注册成功"

    except Exception as e:
        conn.rollback()
        print(e, msg)
    finally:
        cur.close()
        conn.close()

    return msg

# 个人中心
@app.route('/goto_userCenter', methods=['get'])
def user_center():
    uid_args = request.args.get('uid')

    # 判断当前url携带的UID是否为session中的UID，做个人中心的访问控制
    uid = str(session.get('user')[0]) # 类型转换成相同

    if uid == uid_args:
        return '欢迎' + uid
    else:
        return '不可访问他人个人中心'



# 首页自动加载的视频封面
@app.route('/first_page')
def first_page():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('select vid,vtitle,vcoverurl from video')
        covers = cur.fetchall()
        print(covers)
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()
    return render_template('video_cover.html', covers=covers)


# 根据视频类型分类查询
@app.route('/sortByType')
def sort_by_type():
    vtype = request.args.get("type")
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("select vid,vtitle,vcoverurl from video where vtype=%s" %
                    vtype)
        covers = cur.fetchall()
        print(covers)
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()
    return render_template('video_cover.html', covers=covers)


# 根据视频ID查询视频信息,同时查询出该视频的评论信息
@app.route('/video')
def video():
    vid = request.args.get('vid')
    vid = int(vid)
    try:
        conn = get_conn()
        cur = conn.cursor()

        # 查询视频信息
        cur.execute('select * from video where vid=%d' % vid)
        video = cur.fetchone()
        print(video)

        # 查询评论信息
        cur.execute('select * from tb_comment where vid=%d' % vid)
        comments = cur.fetchall()
        comment_count = len(comments)
        print(comments)

    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()
    return render_template('video.html',
                           video=video,
                           comments=comments,
                           comment_count=comment_count)


# 文件的上传
@app.route("/upload", methods=["POST"])
def upload():
    # 设置上传返回消息
    resp_code = ''
    try:
        vtitle = request.form.get("title")

        cover = request.files["cover"]
        cover_name = cover.filename
        cover_path = base_dir + "/video/cover/" + cover_name
        cover.save(cover_path)

        vtype = request.form.get("type")

        video = request.files["video"]
        video_name = video.filename
        video_path = base_dir + "/video/content/" + video_name
        video.save(video_path)

        print(vtitle, cover_path, vtype, video_path)
        conn = get_conn()
        cur = conn.cursor()

        # 从session中获取当前登录用户的UID信息
        uid = session.get('user')[0]
        cur.execute(
            "insert into video(uid,vtitle,vcoverurl,vtype,vurl) values(%d,'%s','%s','%s','%s')"
            % (uid, vtitle, cover_path, vtype, video_path))
        conn.commit()
        resp_code = "上传成功"

    except Exception as e:
        conn.rollback()
        resp_code = "上传失败"
        print(e)
    finally:
        cur.close()
        conn.close()

    return render_template("upload.html", resp_code=resp_code)


# 添加评论信息
@app.route('/add_comment', methods=['POST'])
def add_comment():
    print("hello")
    vid = request.form.get('vid')
    vid = int(vid)
    comment = request.form.get('comment')
    print(vid, comment)

    # 从session中获取当前用户的id和用户名信息、
    user_info = session.get('user')
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "insert into tb_comment(vid,uid,uname,comm) values(%d,%d,'%s','%s')" %
            (vid, user_info[0], user_info[1], comment))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(e)
    finally:
        cur.close()
        conn.close()
    return '添加成功'


if __name__ == "__main__":
    app.run(port=80)
