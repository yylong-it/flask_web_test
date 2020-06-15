from flask import Flask, request, render_template, redirect, session, url_for, flash
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
    allow_path = ('/', '/goto_login', '/goto_reg', '/user_login', '/regist', '/first_page','/favicon.ico', '/sortByType',
                    '/uname_repeat_verify')
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

    try:
        conn = get_conn()
        cur = conn.cursor()

        # 用户状态正常的用户才允许登录
        cur.execute("select uid,uname,user_right from user where uname='%s' and upass='%s' and user_status=0" % (user_name, user_pass))
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

# ajax请求用户名重复性校验
@app.route('/uname_repeat_verify', methods=['post'])
def uname_repeat_verify():

    reg_name = request.form.get('reg_name')
    msg = "验证通过"

    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("select uid from user where uname='%s'"%(reg_name))
        flag = cur.fetchone()

        if flag:
            msg = "用户名重复"
            return msg
            
        return msg
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()    

# 实现注册
@app.route('/regist', methods=['POST'])
def regist():

    reg_name = request.form.get('regist_name')
    reg_pass = request.form.get('regist_pass')

    # # 对输入的数据做校验
    # if len(reg_name) <3 or len(reg_pass)<3:
    #     flash('输入正确的格式')
    #     return redirect(url_for('goto_regist'))
        
    try:
        conn=get_conn()
        cur=conn.cursor()
            
        cur.execute("insert into user(uname, upass) values('%s','%s')" %(reg_name, reg_pass))
        conn.commit()

        # 注册成功后需要自动登录，查询用户ID，用户权限,故需要做用户名唯一性校验
        cur.execute("select uid ,uname,user_right from user where uname='%s'"%(reg_name,))
        user_info = cur.fetchone()
        print(user_info)
        

        # 将用户信息存入session中
        if session.get('user'):
            del session['user']
        session['user'] = user_info

    except Exception as e:
        conn.rollback()
        print(e)
    finally:
        cur.close()
        conn.close()
        
    return redirect(url_for('index'))


# 携带uid跳转个人中心，方便做好访问控制，该方法为中间跳转方法，为了可以从多处携带不通的uid访问
@app.route('/goto_userCenter', methods=['get'])
def user_center():
    uid_args = int(request.args.get('uid'))
    #从session中获取当前登录用户的权限,登录的ID
    u_right = int(session.get('user')[2]) 
    u_id = session.get('user')[0]
    uid_same = 0
    if u_id==uid_args:
        uid_same = 1

    return render_template('/user_center.html', uid = uid_args,u_right=u_right,uid_same=uid_same)


# 首页自动加载的视频封面
@app.route('/first_page')
def first_page():
    # 设置当前的页数，分页查询,存入session
    # 第一次自动请求为1，后面点击一次换页请求+1
    if not session.get("page_num"):
        session['page_num'] = 0
    try:
        conn = get_conn()
        cur = conn.cursor()
        page_num = int(session.get('page_num'))
        print(page_num, type(page_num))
        # 首页自动加载视频状态正常的10条视频,暂且根据点赞数降序筛选
        cur.execute('select vid,vtitle,vcoverurl from video where vstatus=0 order by vup desc limit %d,10'%(10*page_num,))
        page_num += 1
        session['page_num'] = page_num
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
        # 封面在服务器上的存储路径
        cover_path = base_dir + "/static/video/cover/" + cover_name
        # 封面存入数据库的URL，相对地址，避免前端页面找不到路径
        cover_url = os.path.join("../static/video/cover/", cover_name)
        cover.save(cover_path)

        vtype = request.form.get("type")

        video = request.files["video"]
        video_name = video.filename
        # 视频上传的服务器存储路劲
        video_path = base_dir + "/static/video/content/" + video_name
        # 存入数据库的URL
        video_url = os.path.join("../static/video/content/", video_name)
        video.save(video_path)

        print(vtitle, cover_path, vtype, video_path)
        conn = get_conn()
        cur = conn.cursor()

        # 从session中获取当前登录用户的UID信息,用户名信息
        uid = session.get('user')[0]
        uname = session.get('user')[1]
        cur.execute(
            "insert into video(uid,uname,vtitle,vcoverurl,vtype,vurl) values(%d,'%s','%s','%s','%s','%s')"
            % (uid, uname ,vtitle, cover_url, vtype, video_url))
        conn.commit()
        resp_code = "上传成功,等待审核"

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

# 处理用户中心请求
# 处理请求用户信息
@app.route('/req_user_info', methods=['GET'])
def req_user_info():
    # 查询用户的注册信息

    # 获取url携带的uid
    uid = int(request.args.get("uid"))
    # 获取session中的uid
    sess_uid = session.get('user')[0]
    # 判断登录用户和被访问的用户是否为同一个用户
    user_flag = 0
    if sess_uid == uid:
        user_flag = 1
    try:
        conn = get_conn()
        cur = conn.cursor()
        # 访问他人的个人中心，需要先查询他人的隐私设置
        cur.execute("select u_info from tb_pri_setting where uid=%d"%uid)
        res = cur.fetchone()
        # 如果未设置,res 为none,此时也可查询
        if res is None:
            u_info_flag = 0
        else:
            u_info_flag = res[0]
        # 如果隐私设置的可见（0）或者当前登录用户为管理员或自己,才进行后面的操作,
        if u_info_flag == 0 or  session.get('user')[2]==1 or user_flag ==1:
            cur.execute("select uname,regist_time,user_right,user_status from user where uid=%d"%(uid))
            user_info = cur.fetchone()
            return render_template('/user_center_info.html',user_info=user_info,user_flag=user_flag,uid=uid)
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()
    return render_template('/user_center_info.html',msg="抱歉，该主人设置了不开放")

# 处理请求查看评论的信息
@app.route('/req_user_comm', methods=['GET'])
def req_user_comm():
    uid = int(request.args.get('uid'))
    log_id = session.get("user")[0]
    log_uright = session.get('user')[2]
    # 当前登录的用户为管理员,所有内容可见

    try:
        conn = get_conn()
        cur = conn.cursor()
        # 查询当前被访问用户的评论权限
        cur.execute("select u_comm from tb_pri_setting where uid=%d"%uid)
        res = cur.fetchone()
        # res为none，表明未设置过隐私，此时应为默认可见
        if res is None:
            comm_flag = 0
        else:
            comm_flag = res[0]
        # 权限公开（0）,未设置none，或者登录用户为管理员或者自己，才可查看
        if comm_flag == 0 or log_id == uid or log_uright==1:
            cur.execute("select vid,comm,commtime,commstatus from tb_comment where uid=%d"%uid)
            user_comms = cur.fetchall()
            return render_template('/user_center_comm.html',user_comms=user_comms,log_right=log_uright)
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()
    return render_template('/user_center_comm.html',msg="抱歉，该主人设置了不开放")

# 处理请求查看点赞的请求
@app.route('/req_user_good', methods=['GET'])
def req_user_good():
    msg = "我的精彩的点赞"
    return render_template('/user_center_good.html', msg=msg)

# 处理请求收藏的请求
@app.route('/req_user_coll', methods=['GET'])
def req_user_coll():
    msg = "我的收藏夹"
    return render_template('/user_center_coll.html', msg=msg)

# 处理查看投稿信息的请求
@app.route('/req_user_upload', methods=['GET'])
def req_user_upload():
    msg = "我的投稿信息"
    return render_template('/user_center_upload.html', msg=msg)

# 处理请求关注列表的请求
@app.route('/req_user_sub', methods=['GET'])
def req_user_sub():
    msg = "我的关注列表"
    return render_template('/user_center_sub.html', msg=msg)

# 处理请求粉丝列表的请求
@app.route('/req_user_fans', methods=['GET'])
def req_user_fans():
    msg = "我的粉丝列表"
    return render_template('/user_center_fans.html', msg=msg)

# 处理查看浏览记录表
@app.route('/req_user_visits', methods=['GET'])
def req_user_visits():
    msg = "我的浏览记录"
    return render_template('/user_center_visits.html', msg=msg)

# 管理员查看投稿审核
@app.route('/req_mgr_vid', methods=['GET'])
def req_manager_visits():
    msg = "我的待审核稿件"
    return render_template('/user_mgr_vid.html', msg=msg)

# 管理员处理举报信息
@app.route('/req_mgr_reports', methods=['GET'])
def req_mgr_reports():
    msg = "我的待处理举报"
    return render_template('/user_mgr_reports.html', msg=msg)

# 跳转隐私设置页面
@app.route("/goto_user_setting" ,methods=['GET'])
def goto_user_setting():
        return render_template('user_center_setting.html')


# 隐私设置
@app.route("/req_user_privacy" ,methods=['GET'])
def req_user_privacy():

    #获取路径带的参数，分发设置
    req_path = request.args.get('path')
    #获取当前登录用户的ID
    log_id = session.get('user')[0]
    try:
        #获取数据库连接
        conn =get_conn()
        cur = conn.cursor()
        # 查询该登录用户是否设置过隐私设置
        cur.execute("select u_info from tb_pri_setting where uid=%d"%log_id)
        exist_flag = cur.fetchone()

        #分发设置
        #请求设置个人信息
        if req_path == "u_info":
            new_value = request.args.get("new_info")
            if new_value == "show":
                # 设置查询不为空，说明已经设置过了
                if exist_flag:
                    cur.execute("update tb_pri_setting set u_info=0 where uid=%d"%log_id)
                else:
                    # 首次设置，做插入操作
                    cur.execute("insert into tb_pri_setting(uid,u_info) values(%d,0)"%(log_id))
            elif new_value == "hide":
                if exist_flag:
                    cur.execute("update tb_pri_setting set u_info=1 where uid=%d"%log_id)
                else:
                    # 首次设置，做插入操作
                    cur.execute("insert into tb_pri_setting(uid,u_info) values(%d,1)"%(log_id))
            else:
                return "设置出错"    
            conn.commit()
            return "设置成功"
        
        # 请求设置评论设置
        if req_path == "u_comm":
            new_value = request.args.get("new_comm")
            if new_value == "show":
                # 设置查询不为空，说明已经设置过了
                if exist_flag:
                    cur.execute("update tb_pri_setting set u_comm=0 where uid=%d"%log_id)
                else:
                    # 首次设置，做插入操作
                    cur.execute("insert into tb_pri_setting(uid,u_comm) values(%d,0)"%(log_id))
            elif new_value == "hide":
                if exist_flag:
                    cur.execute("update tb_pri_setting set u_comm=1 where uid=%d"%log_id)
                else:
                    # 首次设置，做插入操作
                    cur.execute("insert into tb_pri_setting(uid,u_comm) values(%d,1)"%(log_id))
            else:
                return "设置出错"    
            conn.commit()
            return "设置成功"

    except Exception as e:
        conn.rollback()
        print(e)
    finally:
        cur.close()
        conn.close()




if __name__ == "__main__":
    app.run(port=80)
