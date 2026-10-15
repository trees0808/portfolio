# -*- coding: utf-8 -*-
"""Generates the project detail pages from PROJECTS below.
Run:  python3 build_projects.py   (from the site folder)
Edit the text here, re-run, and the HTML pages are regenerated."""
import html, os, re

HEAD = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · 李嘉纬作品集</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%230e0f12'/><text x='50' y='68' font-size='52' text-anchor='middle' fill='%23ffb84d' font-family='sans-serif' font-weight='700'>李</text></svg>">
</head>
<body>
<header class="nav">
  <div class="wrap">
    <a class="brand" href="index.html">JIAWEI<span>.</span>LI</a>
    <button class="nav-toggle" aria-label="菜单">☰</button>
    <ul>
      <li><a href="index.html#projects">项目</a></li>
      <li><a href="blog.html">博客</a></li>
      <li><a href="index.html#experience">经历</a></li>
      <li><a href="index.html#skills">技能</a></li>
      <li><a href="index.html#contact">联系</a></li>
      <li><a href="assets/李嘉纬_技术策划_简历.pdf" target="_blank">简历 PDF</a></li>
    </ul>
  </div>
</header>
"""

FOOT = """
<footer><div class="wrap">© 2026 Jiawei Li · jiaweil8.com</div></footer>
<script src="assets/main.js"></script>
</body>
</html>
"""

def video(src, cap):
    return f'<figure><video src="assets/video/{src}.mp4" poster="assets/video/{src}.jpg" autoplay muted loop playsinline controls></video><figcaption>{cap}</figcaption></figure>'

def gallery(folder, n):
    oe = "onerror=\"this.style.display='none'\""
    imgs = "".join(f'<img src="assets/img/{folder}/{i}.jpg" alt="{folder} 截图 {i}" data-optional {oe}>' for i in range(1, n + 1))
    return f'<div class="gallery">{imgs}</div>'


def img(src, cap="", cls=""):
    return f'<figure class="{cls}"><img src="assets/img/{src}" alt="{cap}"><figcaption>{cap}</figcaption></figure>'

def phone(src, cap):
    return f'<figure><video src="assets/video/aidol/{src}.mp4" poster="assets/video/aidol/{src}.jpg" muted loop playsinline controls preload="metadata"></video><figcaption>{cap}</figcaption></figure>'

def split(mine, team, mine_title="我负责", team_title="团队其他成员负责"):
    a = "".join(f"<li>{i}</li>" for i in mine); b = "".join(f"<li>{i}</li>" for i in team)
    return f'<div class="split"><div><h4>{mine_title}</h4><ul>{a}</ul></div><div><h4 style="color:var(--muted)">{team_title}</h4><ul>{b}</ul></div></div>'

def vid(path, cap, cls=""):
    return f'<figure class="{cls}"><video src="assets/video/{path}.mp4" poster="assets/video/{path}.jpg" autoplay muted loop playsinline controls preload="metadata"></video><figcaption>{cap}</figcaption></figure>'

def T(n): return f"dreams/thesis/{n}.jpg"

PROJECTS = [
  dict(
    file="grey-waves.html", title="Grey Waves《灰色的海浪》",
    sub="一款 3D 叙事解谜游戏：一位中学老师被困在地震当天的校园时间循环里。玩家在 96 秒的循环中寻找救出所有人的最佳方案，并在无时限的废墟“记忆宫殿”中探索线索、拼出每个角色的故事。",
    desc="Grey Waves 灰色的海浪：CMU ETC 研究生小组项目，Unreal Engine 5 叙事解谜游戏。李嘉纬负责玩法系统设计与实现、96 秒限时循环系统、客户端架构。",
    facts=[("时间","2026.01 – 2026.04"),("团队","CMU ETC 研究生小组项目 · 6 人"),("引擎","Unreal Engine 5 · Blueprint · Level Sequence"),("我的角色","玩法程序 / 系统设计 · 客户端架构 · 部分特效")],
    hero=img("greywaves/cover.jpg","Grey Waves") + video("3", "实机录屏：校园废墟中的探索（Unreal Engine 5）"),
    sections=[
      ("项目概述", """<p>《灰色的海浪》是 CMU ETC 2026 春季学期的研究生小组项目，一款 Unreal Engine 5 叙事解谜游戏。主角是一位中学老师，在一次小地震触发创伤后，被困在地震当天的校园里不断重复。游戏由三个空间组成：</p>
<ul>
<li><strong>现实 / 开场</strong>：温暖、安全、写实的校园，一次小地震触发了主角的创伤。</li>
<li><strong>96 秒时间循环</strong>：地震发生的教学楼。每轮只有 96 秒，目标是找到最佳方案、救出所有人。时间耗尽即重置。</li>
<li><strong>废墟 / 记忆宫殿</strong>：灰白、模糊、悲伤的废墟世界，没有时间限制。玩家在这里发现线索、了解每个角色的故事，再把线索带回循环里使用。</li>
</ul>
<p>团队 6 人，包括导演（项目提出人，负责整体剧情）、叙事设计、3D 美术、技术美术和程序。我作为玩法程序与系统设计，负责核心玩法系统的实现；玩法由我与导演共同设计。</p>""" + '<div class="media media-grid">' + img("greywaves/slide11.jpg","三个空间的结构：现实 → 96 秒循环 → 废墟记忆宫殿（最终汇报）") + img("greywaves/slide8.jpg","时间循环（限时、求最优解）与记忆宫殿（无时限、探索故事）") + "</div>" + '<div class="gallery">' + "".join(f'<img src="assets/img/greywaves/{n}.jpg" alt="Grey Waves">' for n in ["reality-classroom","reality-corridor","reality-exterior","ruin-hall","ruin-corridor","ruin-room"]) + "</div><p class='muted'>同一所学校的三种状态：现实（暖、写实）与废墟（灰白、模糊）。场景美术由团队美术同学完成。</p>"),
      ("救援设计：线索如何改变 96 秒", """<p>循环里有两位被困的学生：<strong>郑浩</strong>受伤无法行走，<strong>王旭</strong>被锁在房间里。每个人都有两种救法，这是整个玩法的核心矩阵：</p>
<table class="mat"><tr><th></th><th>郑浩（受伤）</th><th>王旭（被锁）</th></tr>
<tr><th>蛮力解法<br><span class="muted">耗时，96 秒内很难两个都救</span></th><td>找材料做一个夹板，把他背出去</td><td>——</td></tr>
<tr><th>剧情解法<br><span class="muted">需要先在废墟里找到线索</span></th><td>阻止他回到教学楼</td><td>弄清他为什么被锁，再找到钥匙</td></tr></table>
<p>设计意图是让“了解角色的故事”成为可玩的收益：玩家在废墟里发现的线索，决定了他在 96 秒里能触发哪些事件、能走多短的路线。线索 → 事件状态 → 场景变化与演出，这条链路就是我在技术层面要打通的东西。</p>""" + '<div class="media media-grid">' + img("greywaves/slide12.jpg","救援方案矩阵（最终汇报）") + img("greywaves/slide17.jpg","早期纸面原型：用便签在平面图上推演 96 秒内的路线与事件") + "</div>" + '<div class="media media-grid">' + img("greywaves/floorplan-sketch.jpg","教学楼平面图与玩家出生点") + img("greywaves/concept-art.jpg","概念图：灰色的海浪") + "</div>"),
      ("我负责的部分", split(
        ["<strong>整套 96 秒限时循环系统</strong>（独立实现）：循环计时、重置，以及关键节点完成后对 96 秒场景的对应改变",
         "<strong>NPC 救援玩法</strong>（与导演共同设计）",
         "依据玩家已探索的线索，<strong>动态触发废墟世界中的 Level Sequence</strong>，把剧情演出做成游戏内事件而不是预渲染过场",
         "事件触发器与玩家交互逻辑、物品栏与物品合成、叙事检视（Inspect）系统的一部分，以及试玩后新增的笔记本",
         "客户端架构（GameMode / GameInstance 等框架层）",
         "部分特效与叙事演出的系统层支持"],
        ["整体剧情与导演（项目提出人）","叙事设计","基础 NPC 交互与 NPC 头顶文字系统","3D 美术：模块化场景、道具、角色","技术美术：地震的 Chaos 破碎、Niagara 灰浪与粉尘、材质与后处理"]
      )),
      ("限时循环与场景变化", """<p>96 秒循环是游戏的骨架。我把它实现为一套独立的系统：倒计时、到时重置、每个救援关键节点完成后在 96 秒场景中触发对应的变化。导演可以在这套系统上挂新的节点和演出，而不用改循环本身。</p>
<p>循环场景与废墟场景之间通过传送门切换；下面是两个空间的切换录屏，以及关键节点触发的实机片段。</p>""" + '<div class="media media-grid">' + video("switch_scene","场景切换：从循环中的教学楼进入灰白的废墟世界") + video("TRIGGER","事件触发器：进入区域后触发角色对话与演出") + "</div>" + '<div class="media media-grid">' + video("cutscene","由事件状态触发的 Level Sequence 过场") + video("1","循环中的废墟校园") + "</div>" + '<div class="media media-grid">' + img("greywaves/trigger-debug.jpg","编辑器中的触发区域与事件体积") + img("greywaves/sequencer.jpg","Level Sequence 过场在 Sequencer 中的组织") + "</div>"),
      ("物品、检视与合成", """<p>蛮力解法需要玩家在 96 秒内找材料做夹板。我实现了物品栏、物品检视和合成：在安全公告栏上可以检视到“简易夹板的做法”，再在场景里找到布和尺子，合成出夹板。物品用数据表配置（名称、描述、图标、数量），新增物品不用改逻辑。</p>
<figure class="combo"><img src="assets/img/greywaves/cloth.png" alt="布"><span class="op">+</span><img src="assets/img/greywaves/ruler.png" alt="尺子"><span class="op">→</span><img src="assets/img/greywaves/splint.png" alt="夹板"><figcaption>布 + 尺子 → 夹板（游戏内道具）</figcaption></figure>""" + '<div class="media media-grid">' + video("inspect","检视系统：查看公告栏上的夹板制作说明") + video("key","线索与钥匙：根据对话找到被锁的学生") + "</div>" + '<div class="media media-grid">' + video("inventory","物品栏") + video("splint","救援互动：为受伤的学生上夹板") + "</div>" + '<div class="gallery">' + "".join(f'<img src="assets/img/greywaves/{n}.jpg" alt="Grey Waves">' for n in ["bulletin-board","classroom-desk-interact","locker-lock","door-prompt","door-blocked","inventory-data"]) + "</div><p class='muted'>可交互物件与提示：公告栏、课桌、上锁的柜子、门上的交互提示；右下为物品数据表。</p>"),
      ("试玩问题 → 笔记本", """<p>试玩暴露了三个问题：玩家捡到关键物品后几分钟就忘了它是干什么的；看完废墟里的过场后记不住说了什么、下一步该做什么；单个线索能看懂，但跨场景、跨循环之后线索断了。</p>
<p>我们的解决方案是给玩家一个<strong>笔记本</strong>：把分散在场景、物品和过场里的信息收敛到一个可以随时回看的入口，顺便承担引导的职责。这是我在学期后段实现的系统。</p>""" + '<div class="media media-grid">' + img("greywaves/slide41.jpg","试玩中发现的三个问题") + img("greywaves/notebook-ui.jpg","笔记本界面（按 N 打开）") + "</div>"),
      ("技术证据", '<div class="media media-grid">' + img("greywaves/slide44.jpg","物品栏：编辑器中的结构") + img("greywaves/blueprint-graph.jpg","物品栏相关 Blueprint") + "</div>" + '<div class="media media-grid">' + img("greywaves/slide43.jpg","交互系统：可交互物件与提示图标") + img("greywaves/slide48.jpg","笔记本方案（最终汇报）") + "</div>" + '<div class="gallery">' + "".join(f'<img src="assets/img/greywaves/{n}.jpg" alt="Grey Waves">' for n in ["run-lockers","run-ruin","mainmenu","char-player","assets-kit","fracture-debug"]) + "</div><p class='muted'>主菜单、角色与模块化资产由美术同学制作；地震破碎（Chaos）由技术美术同学制作。</p>"),
      ("回顾", """<div class="note">这学期我们只完成了原定范围的大约三分之一，但做出了一个能玩的原型，把一个抽象的想法变成了可以试玩、可以被推翻的东西。我自己最大的收获是对叙事游戏的看法变了：故事不需要一开始就定死，它应该和玩法一起长出来——交互设计、玩家行为和系统约束会不断改写叙事的方向。另外一个教训是范围控制：我更习惯埋头实现，下次要更早把技术风险和制作周期对上。</div>"""),
    ],
    aside=[("负责内容",["96 秒限时循环系统（独立）","NPC 救援玩法（与导演共同设计）","线索驱动的 Level Sequence 触发","事件触发器 / 物品栏 / 合成 / 检视 / 笔记本","客户端架构","部分特效"]),("工具",["Unreal Engine 5","Blueprint","Level Sequence","Niagara","Perforce"])],
    prev=None, next=("aidol.html","A(i)dol"),
  ),
  dict(
    file="aidol.html", title='A(i)dol <span class="status">开发中</span>',
    sub="“You are not managing an idol. You ARE one.” 一款竖屏单机偶像养成手游：玩家的输入与游戏内选择会影响自己偶像的形象、声音与展示视频，再进入 World 信息流获得粉丝。",
    desc="A(i)dol：CMU ETC 2026 秋季项目，AI 生成驱动的偶像养成手游。李嘉纬负责 Unity 前端、系统规则落地、UI 交互流程与内容配置工具。",
    facts=[("时间","2026.08 – 至今（资料截至 2026.10.13）"),("团队","CMU ETC · 6 人"),("引擎","Unity 6 · URP 2D · C# · UGUI"),("我的角色","Unity 前端 · 系统规则落地 · 内容配置与编辑器工具")],
    hero='<div class="phones">' + phone("a1","Android 真机：启动、加载到开场") + phone("a4","造型室：手指擦雾揭晓新造型") + phone("a2","World：竖滑浏览偶像的视频") + phone("a3","World：评论抽屉与点赞") + "</div>",
    sections=[
      ("项目概述", """<p>A(i)dol 是 CMU ETC 2026 秋季学期项目，面向已经在做二创（剪辑、同人、OC、翻唱）的偶像与动漫粉丝。玩家从一张试镜邀请开始，经过面试、造型、录影，一步步把“自己的偶像”养到出道；AI 生成流水线负责形象、声音、音乐和视频，玩家的输入会影响这些结果。出道后进入叫 <strong>World</strong> 的竖屏信息流，在那里获得粉丝。</p>
<p>我是两名 Unity 前端之一，负责把团队定下的系统规则变成可运行的数据、状态和界面流程，并给内容同学做配置和调试工具；后端与 AI 生成管线由队友负责。项目仍在开发中，本页内容基于 2026 年 10 月 13 日前的工作记录。</p>""" + '<div class="media media-grid">' + img("aidol/slide2.jpg","中期汇报：试镜 → 训练 → 出道 → 粉丝") + img("aidol/slide5.jpg","中期汇报：完整体验流程") + "</div>"),
      ("案例一：玩家流程与状态门控", """<p>游戏是一条有分支的主线：登录 → 面试 → 宿舍 → 造型 → 录影 → 夜间剧情 → World 查看成片。我在 9 月中旬先搭了这一层：</p>
<ul>
<li><strong>进度与持久化架构</strong>：进度枚举、一次性事件标记、本地 JSON / PlayerPrefs 存储、存储接口与后端存储适配，以及统一的 API 请求出口。</li>
<li><strong>场景路由与主线检查点</strong>：剧情场景统一进出口，主线检查点决定玩家能进哪些场景；地图上的地点状态和任务 UI（完成 / 当前 / 锁定）、通知红点都由同一份进度驱动。</li>
<li>9 月 23 日的 V1 把登录、面试、造型、录影、夜间剧情和 World 成片查看串成了第一条可以从头玩到尾的流程；之后的版本在此基础上调整顺序（例如录影改为从宿舍经地图进入）。</li>
</ul>
<div class="note">把“玩家现在在哪、能去哪”收敛成一份状态，是后面所有系统的前提。各界面只读状态、不各自维护进度，之后几次改流程顺序都没有动过界面代码。</div>"""),
      ("案例二：体力与造型规则落地", """<p>团队定了资源规则：Dols（软通货）、Diamonds（硬通货）、Stamina（体力，初始 100）；主线的面试 / 造型 / 录影分别扣 5 / 20 / 20。我负责把规则接进数据配置、UI 状态和后端契约：</p>
<ul>
<li><strong>必扣事件只消费一次</strong>：用一次性标记保证主线消费不重复。</li>
<li><strong>主线体力预留</strong>：可选消费必须给尚未完成的主线留出预算，玩家不会因为在支线花光体力而卡住主线。</li>
<li><strong>造型室状态机</strong>：Intro → TierSelect → Wardrobe → Generating → Ready → Reveal → Feedback → Exit。套装与上下装互斥 / 覆盖、8 槽完成条件（早期版本为 7 槽）、付费解锁确认、Surprise 抽取与收据规则，都由数据表驱动——12 项肤色与 334 项造型来自团队的美术与数据表，我负责目录导入、配置、界面和服务对接。</li>
<li><strong>生成与揭晓</strong>：发起生成请求、异步轮询结果、立绘与头像回填和缓存；完成后进入手指擦雾揭晓（可跳过，擦除阈值是可配置参数），之后可查看立绘大图。</li>
</ul>""" + '<div class="media media-grid">' + img("aidol/slide15.jpg","三种资源：Dols / Diamonds / Stamina（中期汇报）") + img("aidol/slide11.jpg","从美术资产到 UI 系统（中期汇报）") + "</div>"),
      ("案例三：生成等待体验的迭代", """<p>AI 生成有等待时间，需要一个机制盖住这段等待。最初的方案是一个 60 秒三消小游戏，我完成了它的原型：消除组数对应 Low / Mid / High 三档评级，奖励按档位发放，最多 3 局、每局扣 5 体力，多局取最佳评级只补奖励差额。</p>
<p>9 月 29 日对 37 位 K-pop 粉丝做了第一次试玩；10 月 7 日团队决定把 World 扩为核心机制；10 月 8 日的版本<strong>删除了三消</strong>，等待期改为引导玩家浏览 World，生成完成后切换揭晓按钮、状态卡和通知。World 的常规解锁时机也相应从夜间剧情完成调整为造型完成。我按这些决定完成了机制切换。</p>
<div class="note">三消是一个做完、测过、然后被团队决定砍掉的原型。对我来说这是整个项目里最有价值的一次迭代：原型做出来的成本足够低，“换”才能是一个轻松的决定。</div>""" + '<div class="media media-grid">' + img("aidol/slide7.jpg","试玩反馈：玩家想要可带走的东西、正负两面的后果，World 是“WOW moment”") + img("aidol/slide8.jpg","原计划是三消小游戏 → 试玩后改为 World 浏览") + "</div>"),
      ("案例四：内容生产工具", """<ul>
<li><strong>World Studio</strong>：World 是一个可以从任意场景打开的独立预制体，保持页面与播放器状态。World Studio 集中提供账号、视频、评论数据的导入与校验（由数据库和 JSON 管理），预制体构建与迁移，运行时打开 / 关闭、翻页与调试。内容同学不进代码就能填充信息流。</li>
<li><strong>UI 构建工具</strong>：从资源批量构建界面，重建时保留美术手调的布局与引用；后续构建只补缺失的面板和空引用。宿舍主场景 V2 的手调位置就是这样同步回工具的。</li>
<li><strong>主题换皮配置</strong>：礼包页与合同页需要按不同公司（SOM / ERIS）换底图，原来文本是死坐标。我把文字、签名、印章、条款区域做成归一化配置，按底图比例布置，并提供预览 / 重排的编辑器工具。</li>
<li><strong>Login 与邮件导出前端</strong>：玩家名字 / 可选邮箱输入与本地校验、会话参数、成片 ready 后的导出入口与请求状态反馈；邮件发送服务由后端负责。</li>
</ul>""" + '<div class="media media-grid">' + img("aidol/slide12.jpg","两家虚拟经纪公司 ERIS / SOM 的视觉识别——礼包页与合同页需要按公司换皮") + img("aidol/slide16.jpg","学期交付：可玩原型 + AI 开发手册") + "</div>"),
      ("交互与多端适配", """<ul>
<li>World 的竖滑翻页、暂停、按钮 / 双击点赞、评论抽屉；评论点赞与本局发送的评论为本地状态，不是多人服务。Following、搜索、Shop、发布等入口在当前版本仍是占位。</li>
<li>手机与平板采用不同的视频适配策略避免拉伸；RootHeightFitter 与独立的 World 缩放策略处理两种比例的布局。测试基线为 Pixel 手机与 Samsung 平板。</li>
<li>对 Pixel 6 的触屏输入、安全区域、Canvas 缩放等做过一轮审查并列出真机测试清单；Web 发布与 iOS 内测做过可行性评估，尚未实施。</li>
</ul>
<p class="muted">开发过程中使用了 AI 辅助编码。项目主页：<a href="https://projects.etc.cmu.edu/aidol" target="_blank" rel="noopener">projects.etc.cmu.edu/aidol</a></p>"""),
    ],
    aside=[("负责内容",["进度持久化 / 场景路由 / 主线检查点","体力、造型与抽取规则落地","三消原型 → World 浏览机制切换","World Studio / UI 构建工具 / 换皮配置","World 交互与手机 / 平板适配","Login、邮件导出等服务对接前端"]),("团队负责",["后端与 AI 生成管线","经济与造型规则来源、数据表","美术资产与 UI 视觉","宿舍通知栏等其他前端模块"]),("工具",["Unity 6 · URP 2D","C# / UGUI / 新 Input System","Editor 工具链","JSON 数据配置","Perforce"])],
    prev=("grey-waves.html","Grey Waves"), next=("bbr.html","Beat Battle Royale"),
  ),
  dict(
    file="bbr.html", title="Beat Battle Royale《节奏舞台》",
    sub="一款 2v2 节奏派对游戏：两支乐队在同一个舞台上踩着节拍对战，谁的连击更稳、音符更多，舞台的灯光、大屏和音乐就倒向谁。CMU ETC「构建虚拟世界」（BVW）第 4 轮，两周完成。",
    desc="Beat Battle Royale 节奏舞台：CMU ETC BVW Round 4 两周项目，Unity 2v2 节奏对战派对游戏。李嘉纬共同设计节奏对战机制，负责玩家 3C、节拍判定、计分与领先方舞台切换。",
    facts=[("时间","2025.11 · 两周"),("团队","CMU ETC BVW · 5 人（2 程序 / 2 美术 / 1 音乐）"),("引擎","Unity · C# · 键盘 / Xbox 手柄"),("我的角色","共同设计 · 程序：3C / 节拍判定 / 计分 / 舞台切换")],
    hero='<div class="media media-grid">' + img("bbr/highscore.jpg","正式版舞台：两支乐队、七个竞技圈与中央大屏") + img("bbr/multiplayer.jpg","四名玩家同时在场") + "</div>",
    sections=[
      ("项目概述", """<p>BVW 是 ETC 第一学期的核心课程：每两周换一次队伍、换一个命题，从零做出一个可玩的世界。第 4 轮我们做了 Beat Battle Royale——一款 2v2 的节奏对战派对游戏，一局 3 分 26 秒，支持键盘和 Xbox 手柄。</p>
<p>玩家分成 Pop 队和 Red Devil 队，在同一个舞台上踩着歌曲的节拍打出连击来争夺音符；比分领先的一方会“接管”舞台——大屏切成自己的画面，背景音乐也淡入自己乐队的版本。设计由全组共同完成，我和另一位程序分工实现。</p>"""),
      ("核心机制", """<ul>
<li><strong>节拍判定</strong>：按歌曲的时间戳生成收缩的圆圈，玩家在圆圈闭合时按键；Perfect 窗口 0.15 秒、Good 0.3 秒，每一拍每人只判一次。</li>
<li><strong>竞技圈</strong>：舞台上有 7 个圈，每 15 秒随机激活 2 个。进圈后比连击：先打到目标连击数的一方赢得这个音符。音符的分值分三段递增（10 → 15 → 20），后期的争夺更值钱。</li>
<li><strong>偷音符</strong>：跑到对方舞台上发起 Steal——进攻方要 6 连击、防守方只要 4 连击；输的人被传送出场并锁定 5 秒。</li>
<li><strong>Aura 增益</strong>：定时刷新的道具，捡到后 10 秒内连击翻倍。</li>
<li><strong>领先方接管舞台</strong>：每 5 秒按比分判断领先方，交叉淡入对应乐队的 BGM，并切换中央大屏的舞台视频。</li>
</ul>""" + '<div class="phones" style="grid-template-columns:repeat(auto-fit,minmax(220px,1fr))">' + vid("bbr/earnanote","进圈比连击，赢得音符") + vid("bbr/boost","Aura 增益：10 秒连击翻倍") + vid("bbr/gainnote","音符结算与比分") + "</div>" + img("bbr/boost.jpg","Aura 特效")),
      ("我负责的部分", split(
        ["与全组共同设计节奏对战机制","玩家 3C：移动、镜头、按键反馈","节拍判定：按时间戳生成圆圈，Perfect / Good 判定窗，每拍每人只判一次","计分系统：三段式分值与音符归属","领先方切换：按比分交叉淡入 BGM、切换舞台大屏"],
        ["竞技圈激活、Steal 与传送锁定、Aura 道具等其他玩法逻辑（另一位程序）","角色、舞台与特效（2 位美术）","两支乐队的两版配乐与音效（音乐）"]
      )),
      ("从原型到正式版", """<p>第一周先在灰盒舞台上把“踩拍 → 连击 → 抢音符”的循环跑通：粉色圆台、收缩的判定圈、头顶的 HIT 连击条；确认好玩之后第二周再换上正式的舞台、角色与灯光。</p>""" + vid("bbr/programming","第一周的灰盒原型：节拍判定与计分已经可玩") + '<div class="gallery">' + "".join(f'<img src="assets/img/bbr/{n}.jpg" alt="BBR">' for n in ["1","2","3","4","5","midnote"]) + "</div><p class='muted'>上：原型阶段的判定圈与 HIT 连击条；下：正式版的舞台与音符。</p>"),
    ],
    aside=[("负责内容",["共同设计","玩家 3C","节拍判定","计分","领先方舞台 / 音乐切换"]),("工具",["Unity","C#","Xbox 手柄输入","Git"])],
    prev=("aidol.html","A(i)dol"), next=("starfisher.html","StarFisher"),
  ),
  dict(
    file="starfisher.html", title="StarFisher",
    sub="海底主题的多人对抗游戏，为 Xbox Adaptive Controller 设计：操控一条鱼伸出鱼钩钓水母，钓到的水母像贪吃蛇一样跟在身后，送回海葵基地得分；钩到别人的链子就能把它打断。CMU ETC BVW 第 3 轮，两周完成。",
    desc="StarFisher：CMU ETC BVW Round 3 两周项目，面向 Xbox Adaptive Controller 的 Unity 多人对抗游戏。李嘉纬共同设计黄金矿工 × 贪吃蛇机制，负责两名玩家的移动与抓取。",
    facts=[("时间","2025.10 · 两周"),("团队","CMU ETC BVW · 5 人（2 程序 / 2 美术 / 1 音乐）"),("引擎","Unity · URP · Xbox Adaptive Controller"),("我的角色","共同设计 · 程序：玩家移动与抓取")],
    hero=img("starfisher/cover.jpg","StarFisher 标题画面"),
    sections=[
      ("项目概述", """<p>BVW 第 3 轮的命题是为 <strong>Xbox Adaptive Controller</strong>（面向行动不便玩家的无障碍手柄）设计游戏：输入只有少数几个大按钮和扳机，所以玩法必须简单到用两三个输入就能玩，又要在 2–4 人同场时有足够的对抗。</p>
<p>我们把“黄金矿工”和“贪吃蛇”合在了一起：玩家是一条鱼，用 LT / RT 转向，按 A 伸出可伸缩的鱼钩钓水母；钓到的水母串成一条链跟在身后，带回海葵基地就得分。链子越长分越多，但也越容易被别人钩断——攒到 3 只以上还能按 B 换一颗星星炸弹，把周围的对手炸晕。一局 120 秒，每 20 秒刷新一批水母。</p>"""),
      ("规则一览", '<div class="gallery">' + "".join(vid(f"starfisher/{i}",c) for i,c in [(1,"2–4 支队伍，用手柄控制你的鱼"),(2,"LT / RT 左右转向"),(3,"按 A 伸出鱼钩，钓到的水母串在身后"),(4,"海葵会收走你的水母并计分"),(5,"钩到别人的链子就能打断它"),(6,"3 只以上水母 → 按 B 换星星炸弹，炸晕对手")]) + "</div>"),
      ("我负责的部分", split(
        ["与全组共同设计“黄金矿工 × 贪吃蛇”的核心机制","两名玩家的移动：适配 Adaptive Controller 的转向与推进","鱼钩的伸出、收回与抓取判定"],
        ["水母链的蛇形跟随（位置历史跟随）与计分、炸弹（另一位程序）","海底场景、角色与 Shader Graph 水面 / 水波（2 位美术）","音乐与音效（音乐）"]
      ) + """<div class="note">给 Adaptive Controller 做设计是这一轮最有意思的约束：输入少，所以每个输入都得“一按就有事发生”。鱼钩是唯一的进攻和采集手段，转向是唯一的移动——玩法的全部深度都压在这两个动作的时机上。</div>"""),
    ],
    aside=[("负责内容",["共同设计","玩家移动","鱼钩伸缩与抓取"]),("工具",["Unity · URP","C#","Xbox Adaptive Controller","Git"])],
    prev=("bbr.html","Beat Battle Royale"), next=("fishing.html","《捕鱼大作战》"),
  ),
  dict(
    file="fishing.html", title="《捕鱼大作战》BOSS 玩法与策划工具",
    sub="途游游戏线上商业项目实习：根据策划文档落地 3 个正式上线的 BOSS 玩法，并为策划与开发团队做了鱼类路径编辑器与 GM 调试工具。",
    desc="途游游戏《捕鱼大作战》游戏客户端开发实习：BOSS 玩法落地、鱼类路径编辑器、GM 工具、协议对接。",
    facts=[("时间","2024.02 – 2024.11"),("公司","途游游戏"),("引擎","Unity · C#"),("职位","游戏客户端开发实习生（玩法方向）")],
    hero=img("tuyoo/logo.jpg","途游游戏") + '<div class="note">线上商业项目，受保密约定限制，本页只描述工作内容，不展示内部截图、工具界面与代码。</div>',
    sections=[
      ("BOSS 玩法落地", """<ul>
<li>根据策划文档实现具有新玩法的 BOSS，与美术、后端、测试协作完成版本更新。</li>
<li>实习期间累计完成 <strong>3 个正式上线的 BOSS</strong>，单个开发周期约 4–5 周，覆盖从需求评审、实现、联调到上线回归的完整流程。每个 BOSS 基于统一的 BOSS 效果基类扩展：登场、结算演出、得分展示、倍率与最终收益的表现都走同一套事件流程，新 BOSS 只需要覆写自己的演出部分。</li>
<li>这段经历让我习惯了站在策划需求和程序实现之间做翻译：先把规则拆成状态和数值，再谈怎么实现。</li>
</ul>"""),
      ("策划工具：鱼类路径编辑器", """<ul>
<li>独立开发鱼类路径编辑器，策划可以<strong>可视化配置鱼群的移动轨迹</strong>，并直接导入本体项目，服务关卡与玩法内容制作。</li>
<li>原本需要程序改参数、重新打包验证的流程，变成策划自己就能迭代的流程。</li>
</ul>"""),
      ("GM 工具与数据上报", """<ul>
<li>维护 GM 调试工具：开发者在游戏内输入命令 ID 和参数，就能快速调用特定功能——例如用自定义数据（获得的金币数等）直接触发一次 BOSS 击杀结算，或者立即查看某段 CG。策划和测试不用打到对应环节就能验收内容。</li>
<li>与后端对接协议，上报低帧率、设备过热和玩家行为等信息，为性能优化和玩法调优提供数据。</li>
</ul>"""),
    ],
    aside=[("负责内容",["3 个上线 BOSS 玩法","鱼类路径编辑器（独立）","GM 工具维护","后端协议对接与数据上报"]),("工具",["Unity","C#","Editor 扩展","Git"])],
    prev=("starfisher.html","StarFisher"), next=("vr-dunhuang.html","VR Dunhuang"),
  ),
  dict(
    file="vr-dunhuang.html", title="VR Dunhuang《敦煌艺术》",
    sub="面向 Meta Quest 的 VR 探索游戏：玩家在莫高窟 302 窟里挑选一件艺术品，用手抓起它、走进它想象出的世界——九色鹿、金刚经、倒塔中心柱——用手势与场景互动、传送。",
    desc="VR Dunhuang：Unity + Meta Quest 的手势交互 VR 探索游戏，北京工业大学本科小组项目。李嘉纬负责手势追踪交互程序与场景交互设计。",
    facts=[("时间","2025.02 – 2025.04"),("团队","北京工业大学 · 本科小组项目"),("引擎","Unity · Meta Quest（Oculus / Meta XR SDK）"),("我的角色","程序 · 交互设计")],
    hero=img("dunhuang/cave-hero.jpg","莫高窟洞窟：写实风格复现壁画与中心柱"),
    sections=[
      ("项目概述", """<p>VR Dunhuang 是一款面向 Meta Quest 的 Unity VR 探索游戏，没有传统的胜负条件，目标是让玩家通过与艺术品的互动理解和体验敦煌艺术。游戏虚拟重建了三件经典作品：<strong>九色鹿本生</strong>、<strong>金刚经变</strong>和<strong>莫高窟 302 窟的倒塔中心柱</strong>。玩家先在写实复现的洞窟里挑选一件作品，用手抓起它放到指定位置，就会进入这件作品“想象出来的”场景；每个场景都有独特的交互元素，解锁更多关于作品的信息和文化故事。</p>""" + '<div class="media media-grid">' + img("dunhuang/pick-scene.jpg","洞窟中挑选作品") + img("dunhuang/enter-scene.jpg","抓起作品，放到指定位置进入场景") + "</div>" + '<div class="media media-grid">' + img("dunhuang/imaginary-302.jpg","302 窟倒塔中心柱的想象场景，附作品介绍") + img("dunhuang/title.jpg","标题画面") + "</div>"),
      ("三个想象场景", """<p>洞窟采用写实风格忠实还原壁画细节；作品内部的想象场景则采用绘画风格，把壁画里的关键元素——九色鹿与层叠的山、金刚经变里的佛与山水——变成可以走进去的三维空间。</p>""" + '<div class="gallery">' + "".join(f'<img src="assets/img/dunhuang/{n}.jpg" alt="VR Dunhuang">' for n in ["art-deer","art-sutra","art-pillar","scene-deer","scene-sutra","scene-pillar"]) + "</div><p class='muted'>上：原作；下：游戏中对应的想象场景。</p>"),
      ("手势交互：我的工作", """<p>游戏的交互全部基于 Oculus 的<strong>手部追踪手势识别</strong>，这是整个项目最大的技术挑战，也是我负责的核心部分：</p>
<ul>
<li><strong>手势控制系统</strong>：用手直接抓取艺术品并放置到指定位置；用手指点选 UI（例如 Back 按钮）。给手加上 Grabber、给物体加上 Grabbable 组件并设定抓取手势；抓取功能做成独立的子物体以便维护。为了避免雕像在手里“漂浮”或者手像抓着空气，雕像没有用更省资源的 Cube Collider，而是用了贴合模型的碰撞体。</li>
<li><strong>传送系统</strong>：用特定手势在场景间传送。传送逻辑分成两部分——挂在玩家身上发起交互的 Teleport Interactor，和挂在目标位置接收交互的 Teleport Interactable。</li>
<li>场景中的交互逻辑设计与实现。遇到的问题主要靠官方文档和示例工程解决。</li>
</ul>""" + '<div class="gallery">' + "".join(f'<img src="assets/img/dunhuang/{n}.jpg" alt="VR Dunhuang">' for n in ["grab","select","teleport","grab-inspector","teleport-interactor","hierarchy"]) + "</div><p class='muted'>抓取与放置、手指点选、手势传送；Grabbable / HandGrabInteractable 组件配置、传送目标点、Hand Interactor 层级。</p>"),
      ("分工与回顾", split(
        ["手势追踪交互（抓取、点选、传送）","场景中的交互逻辑设计与实现"],
        ["场景规划、白盒与美术搭建","三维模型与贴图（中心柱从白模到完成）"]
      ) + '<div class="media media-grid">' + img("dunhuang/pillar-models.jpg","中心柱：白模 → 雕刻 → 上色") + img("dunhuang/unity-editor.jpg","Unity 工程中的场景") + "</div>" + """<div class="note">团队分成交互设计和美术设计两部分，从场景规划和白盒开始，逐步用模型和细节填满每个场景。这个项目让我学会了用官方文档和示例工程解决实际问题，尤其是手势控制和 VR 交互，也加深了我对 VR 交互设计的理解。</div>"""),
    ],
    aside=[("负责内容",["手势追踪交互：抓取 / 点选 / 传送","场景交互逻辑"]),("工具",["Unity","Meta XR / Oculus Integration SDK","C#","Meta Quest 3"])],
    prev=("fishing.html","《捕鱼大作战》"), next=("dreams-dont-die.html","Dreams Don't Die"),
  ),
  dict(
    file="dreams-dont-die.html", title="Dreams Don't Die《不想死的游戏人》",
    sub="“I see blue in your eyes, but I also see the light.” 一款围绕独立游戏开发者心理历程的沉浸式情绪叙事游戏：4 个玩法关卡与 5 个叙事场景交替推进，用空间、光影、漂浮文字和音乐带玩家走过迷茫、困境、焦虑、崩溃到希望。我的本科毕业设计。",
    desc="Dreams Don't Die 不想死的游戏人：Unity HDRP 第一人称情绪叙事游戏，李嘉纬的本科毕业设计。独立完成游戏设计、场景设计与制作、玩法实现与 HDRP 渲染。",
    facts=[("时间","2024.05 起 · 2025.05 完成毕业设计"),("团队","个人项目 · 两位同学协助美术"),("引擎","Unity · HDRP · Shader Graph"),("我的角色","发起者 · 游戏设计 · 场景与渲染 · 玩法程序 · UI")],
    hero=img("dreams/cover.jpg","Dreams Don't Die：游戏机墓地"),
    sections=[
      ("项目概述", """<p>灵感来自 B 站纪录片《不想死的游戏人》——独立开发者在资金、市场和自我怀疑中挣扎的真实处境。我想把开发者的压力源（创作挫败、过劳、焦虑）编码成可以走进去的空间和可以破解的谜题，让从业者在游玩中完成一次象征性的释放，也让圈外人通过亲身体验理解创作的复杂。</p>
<p>这是我发起并主导的项目：整体设计、全部场景的设计与制作、玩法都由我完成，两位同学帮忙制作了部分美术资产。项目最初作为课程小组作业开始，之后由我继续完善，成为我的本科毕业设计《面向情感氛围营造的沉浸式游戏设计与开发》（北京工业大学，2025 年 5 月）。</p>
<p>游戏采用 Unity + HDRP 开发，发布于 Windows PC。第一人称视角，<strong>4 个玩法关卡与 5 个叙事场景交替穿插</strong>，按“寻找 — 追逐 — 释怀”的心理节奏排列：每个关卡之后接一个情绪场景，形成“行为体验 → 内心共鸣 → 情绪转折”的三段式循环。</p>""" + img(T("structure"),"游戏结构与流程：关卡与叙事场景交替（论文图 4.1）")),
      ("设计：一条情绪曲线", """<p>整个游戏的策划核心是“情绪递进与氛围营造”。我先定下一条情绪曲线，再为每一段分配一种玩法或一个场景，并用场景关键词约束美术与音乐：</p>
<table class="mat"><tr><th>顺序</th><th>类型</th><th>情绪阶段</th><th>设计关键词</th></tr>
<tr><td>关卡 1</td><td>第一人称迷宫</td><td>迷茫</td><td>寻找 / 方向感缺失 / 遗迹感</td></tr>
<tr><td>场景 1</td><td>游戏机墓地（幻想）</td><td>失落</td><td>失败记忆 / 荒凉沙滩 / 沉寂感</td></tr>
<tr><td>关卡 2</td><td>倾斜玩具迷宫</td><td>困境</td><td>无力操控 / 微调失败 / 精疲力竭</td></tr>
<tr><td>场景 2</td><td>昏暗办公室（现实）</td><td>压力</td><td>窒息空间 / 独白文字 / 重复性</td></tr>
<tr><td>关卡 3</td><td>井字格追逐</td><td>焦虑</td><td>节奏紧迫 / 控制反应 / 紧张感</td></tr>
<tr><td>场景 3</td><td>医院走廊（现实）</td><td>崩溃</td><td>线性空间 / 微光 / 病态感</td></tr>
<tr><td>场景 3.5</td><td>海上车站（过渡）</td><td>重启</td><td>安静车站 / 列车鸣笛 / 梦境转折</td></tr>
<tr><td>关卡 4</td><td>飞行收集光球</td><td>希望</td><td>飞行自由 / 空旷空间 / 光感流动</td></tr>
<tr><td>场景 4</td><td>回到海滩（幻想）</td><td>愈合</td><td>开阔视野 / 阳光海滩 / 明朗色彩</td></tr></table>
<p>每一段都用四类符号协同工作：<strong>物理符号</strong>决定玩家“在哪儿”感受情绪（场景构造、道具）；<strong>角色符号</strong>决定“以谁的身份”感受（第一人称、角色状态——例如医院里失去奔跑与跳跃）；<strong>视听符号</strong>决定“如何感觉”（色调光影、音乐、雾效）；<strong>叙事符号</strong>决定“感受到什么”（漂浮文字）。</p>"""),
      ("五个叙事场景", """<ul>
<li><strong>游戏机墓地</strong>：荒凉海滩上散落着锈蚀、屏幕破裂、倾倒的复古街机——梦想崩塌的墓碑。傍晚斜照 + HDRP 体积雾压低视野；没有任务提示，玩家靠地面触发点推进，漂浮文字像回忆碎片一样逐字升起。</li>
<li><strong>昏暗办公室</strong>：窄长的开放式办公室，只有尽头一盏吊灯亮着。进入后玩家失去跳跃与奔跑、移速下降，模拟“心理迟滞”；文字悬浮在桌椅、投影幕和键盘上方——“为何没有人给予反馈”“我逐渐开始讨厌点开评论区”。</li>
<li><strong>医院</strong>：抽象化的手术台与走廊，没有窗户与自然光。这是全游戏控制力最弱的一段：移速再降、镜头有轻微延迟、路径线性、没有选择，让玩家代入“无力反抗现实”。文字出现在高空、墙角、地面甚至前进路径上，带漂移动画。</li>
<li><strong>海上车站</strong>：走到医院走廊尽头，一扇门缓缓打开——门后不是走廊，而是海面上的木质站台和驶来的列车。两段在同一个 Unity Scene 里，靠后处理体积切换、音乐淡入淡出和控制变化完成从“压抑”到“重启”的跳变，不加载新场景。文字从“你的身体正在死去”变成反问“它们还是你的梦魇吗？”。</li>
<li><strong>希望的海滩</strong>：与第一个场景同样的地形与构图，但换成明亮的沙粒贴图、晴空天空盒和带波纹反射的海面；游戏机墓碑整齐安静地留在沙丘里——失败被接纳，成为记忆的一部分。首尾呼应成一个圆环。</li>
</ul>""" + '<div class="gallery">' + "".join(f'<img src="assets/img/{T(n)}" alt="Dreams Dont Die">' for n in ["s1-beach-text","s2-office-text","s3-hospital-wake","s3-door-transition","s3-station","s4-hope-beach"]) + "</div><p class='muted'>游戏机墓地 → 办公室 → 医院醒来 → 走廊尽头的门 → 海上车站 → 希望的海滩。</p>"),
      ("四个玩法关卡", """<ul>
<li><strong>关卡 1 · 第一人称迷宫（迷茫）</strong>：多层交错的圆形迷宫，中心有一道垂直光柱——目标清晰、路径混沌。左下角有实时小地图辅助定位；路边陈列着倾倒的办公桌、游戏机外壳、被踩踏的开发文档。</li>
<li><strong>关卡 2 · 玩具迷宫（困境）</strong>：玩家不控制角色，而是用鼠标拖拽或 WASD 倾斜整个迷宫底板，让小球滚到终点。小球有加速度与惯性，需要不断微调、反复尝试；没有背景音乐，只有滚动与碰撞声。</li>
<li><strong>关卡 3 · 井字格追逐（焦虑）</strong>：九宫格场地里追一颗会逃的光球。光球只能前后左右移动、优先往玩家反方向逃、在外圈按逆时针规则绕圈；唯一的通关方法是先走到光球对侧最远处，再沿直线逼它进出口。场景是办公地毯 + 玻璃隔断 + 办公桌——在现实框架里追逐梦想。</li>
<li><strong>关卡 4 · 飞行收集（希望）</strong>：操控飞行器穿越一座上下颠倒的梦境城市，收集空中的光球。没有敌人、没有时限，只有飞向、收集、再飞向。</li>
</ul>""" + '<div class="gallery">' + "".join(f'<img src="assets/img/{T(n)}" alt="Dreams Dont Die">' for n in ["l1-maze","l2-toy-maze","l3-grid-layout","l3-office-chase","l4-inverted-city","l4-flight"]) + "</div>"),
      ("实现：HDRP 渲染与情绪过渡", """<ul>
<li><strong>室外</strong>：Physically Based Sky + Volume Fog，按场景调太阳角度、雾密度与散射色——墓地压低曝光、加浓雾；希望海滩降雾提曝光。Screen Space Reflection 强化水面与湿沙反射，Contact / Micro Shadows 补细节阴影。</li>
<li><strong>室内</strong>：主光源 + 局部点光源（台灯、吊灯、手术灯）分区照明；Light Probe / Reflection Probe + 静态物体 Baked GI，既保证间接光质量又降低运行时开销；局部后处理体积调低曝光、冷却色温、降饱和。</li>
<li><strong>情绪过渡</strong>：在医院与车站的交界处放两个基于世界空间的后处理体积，玩家进入触发区时自动切换 Color Grading / Exposure / Bloom / Fog——雾降、曝光升、色调转亮——不加载场景就完成情绪跳变。飞行关卡里不同高度的体积再做雾与色调的微调。</li>
</ul>""" + '<div class="media media-grid">' + img(T("post-volumes"),"两个基于世界空间的后处理体积") + img(T("same-scene-two-renders"),"同一场景的两种渲染：医院走廊与海上车站") + "</div>" + '<div class="media media-grid">' + img(T("hdrp-sky-fog"),"Sky and Fog Global Volume") + img(T("baked-gi"),"烘焙光照与反射探针") + "</div>"),
      ("实现：漂浮文字、溶解光球与各关卡系统", """<ul>
<li><strong>空间文字系统（SentenceController）</strong>：自制特效文字预制体，脚本获取子节点的所有 TextMeshPro，用协程逐字渐现、绕 Y 轴旋转（速度按动画曲线从快到慢）、达到旋转次数上限后缩放淡出并禁用；SetStartWithEffect() 可按场景触发或重启，让叙事节点与玩家进度同步。</li>
<li><strong>光球溶解（Shader Graph）</strong>：Simple Noise + Step 做遮罩，Alpha Clip Threshold 输出剔除，脚本在收集事件时缓慢推高 Clip 值；保留自发光通道，溶解中仍有微光。海滩与飞行关卡的光球共用。</li>
<li><strong>小地图</strong>：迷宫上方一台正交摄像机只渲染 UI 层，输出到 RenderTexture 绑定到 RawImage；玩家头顶一个跟随 Sphere 作为位置标记。</li>
<li><strong>玩具迷宫</strong>：鼠标拖拽或 WASD 累加旋转增量，X / Z 轴钳制在 ±23°，灵敏度参数可调。</li>
<li><strong>井字格追逐</strong>：Pos1–Pos9 九个碰撞盒记录玩家所在格；光球 Target 脚本在玩家进入触发器时调用 GameManager.MoveTarget()，按逃逸规则算下一格并用 Lerp 平滑移动；玩家在 Pos1、光球在 Pos9 时判定通关，播放逃逸音效并切换场景。</li>
<li><strong>飞行关卡</strong>：基于 Asset Store 的飞行工具包搭建，接入项目自己的拾取判定与 UI 计数；收集完毕触发结局。</li>
</ul>""" + '<div class="media media-grid">' + img(T("text-effect"),"漂浮文字：渐现、旋转、淡出") + img(T("dissolve-shadergraph"),"光球溶解的 Shader Graph") + "</div>" + '<div class="media media-grid">' + img(T("dissolve-demo"),"溶解过程（Clip 值变化）") + img(T("minimap-overlay"),"小地图：正交摄像机与迷宫重合放置") + "</div>" + '<div class="media media-grid">' + img(T("grid-hierarchy"),"井字格：Pos1–Pos9 检测点与 Target") + img(T("flight-kit"),"飞行工具包的接入") + "</div>"),
      ("成果", '<div class="gallery">' + "".join(f'<img src="assets/img/{T(n)}" alt="Dreams Dont Die">' for n in ["r1-maze","r2-beach","r3-toy-maze","r4-office","r5-chase","r6-hospital","r7-station","r8-flight","r9-final-beach"]) + "</div><p class='muted'>按游玩顺序：迷宫 → 游戏机墓地 → 玩具迷宫 → 办公室 → 井字格追逐 → 医院 → 海上车站 → 飞行 → 回到海滩。</p>" + '<div class="gallery">' + "".join(f'<img src="assets/img/dreams/{n}.jpg" alt="Dreams Dont Die">' for n in ["main-menu","pause-menu","6"]) + "</div>"),
      ("回顾", """<p>功能测试覆盖了小地图同步、迷宫旋转手感、光球逃逸逻辑、飞行拾取、音乐过渡、文字特效与关卡切换，均达到预期。后续想做的：丰富局部美术细节、给迷宫加时限或给追逐加光球分裂等可选挑战、给小地图加朝向标识。</p>
<div class="note">这个项目让我真正学会了 HDRP，也让我第一次系统地用“情绪曲线”来组织一整款游戏的玩法与场景。它也让我意识到视觉叙事和玩法之间需要平衡——后来在 Grey Waves 里我把更多精力放在了“玩法如何推动叙事”上。</div>"""),
    ],
    aside=[("负责内容",["项目发起与整体游戏设计","情绪曲线与关卡 / 场景规划","全部场景设计与制作、HDRP 渲染","漂浮文字 / 溶解 Shader / 小地图 / 迷宫 / 追逐 AI 等玩法实现","UI 与 PC 端发布"]),("团队协助",["部分美术资产（两位同学）"]),("工具",["Unity HDRP","C#","Shader Graph","TextMeshPro","Unity Input System"])],
    prev=("vr-dunhuang.html","VR Dunhuang"), next=("goddess.html","Goddess"),
  ),
  dict(
    file="goddess.html", title="Goddess",
    sub="一款等距视角的 2D 动作 Roguelike，运行在老师提供的 TypeScript + HTML 自研引擎框架上。引擎只有底层接口和类似 Unity 的 MonoBehaviour 结构，没有动画系统和 UI 系统——UI 系统是我从零写的。",
    desc="Goddess：基于课程自研引擎（TypeScript + HTML）的 2D 动作 Roguelike。李嘉纬负责游戏设计与从零搭建 UI 系统。",
    facts=[("时间","2024.06 – 2024.07"),("团队","北京工业大学 · 课程项目 · 3 人"),("引擎","课程自研引擎框架 · TypeScript · HTML"),("我的角色","游戏设计 · UI 系统程序")],
    hero=img("goddess/logo.jpg","Goddess 开始界面") + '<div class="media media-grid">' + img("goddess/gameplay.jpg","等距视角的战斗") + img("goddess/blessings.jpg","祝福选择面板") + "</div>",
    sections=[
      ("项目概述", """<p>Goddess 是一款 2D 动作冒险 Roguelike：玩家在不断变化的地下遗迹里八方向移动、攻击、闪避（带无敌帧）、使用技能；每关击败一定数量的敌人后进入下一关，战斗中和关卡之间可以获得临时强化或“祝福”符文。敌人有快速小怪、重甲守卫、施法者等不同类型，对应不同的战斗策略。</p>
<p>课程的目的是用最原始的引擎框架做一款完整的游戏，在过程中理解引擎的原理：场景和预制体在代码层面是怎么组织的、引擎核心组件是怎么协作的。没有可视化编辑器，场景和预制体都是手写的 YAML / JSON，要在控制台里启动游戏才能看到效果。</p>""" + '<div class="media media-grid">' + img("goddess/editor.jpg","开发环境：完全用代码编辑游戏") + img("goddess/prefab-yaml.jpg","手写的预制体：Transform、RigidBody、BoxCollider 与子节点") + "</div>"),
      ("从零搭建 UI 系统", """<p>引擎只能显示图片和文字，没有点击检测，更没有 UI 组件。这是我遇到的最大挑战，也是我负责的核心部分：</p>
<ul>
<li>先实现<strong>点击检测</strong>：用逆矩阵把屏幕坐标换算到各节点的局部坐标系，判断点击是否落在指定范围内。</li>
<li>参考 Unity 的结构实现 <strong>Canvas 组件</strong>，作为 UI 层的基类；在它之上做出 Button、Image、Text 等组件，以及祝福面板、重开按钮、相机跟随等具体界面。</li>
<li>血条、菜单、祝福选择面板等所有游戏内 UI 都建立在这套系统上。</li>
</ul>""" + '<div class="media media-grid">' + img("goddess/ui-files.jpg","UI 系统源码：Canvas、Button、UILayer、BlessPanel 等") + img("goddess/blessings.jpg","祝福选择面板") + "</div>"),
      ("美术流程", """<p>2D 素材其实来自 3D 模型：在 Blender 里用像素风 Shader 渲染，从固定视角抓取循环帧生成角色动画；场景也是 Blender 渲染出来的一张图。</p>""" + '<div class="media media-grid">' + img("goddess/blender.jpg","Blender 中渲染的场景") + img("goddess/escaped.jpg","通关画面") + "</div>"),
      ("分工与回顾", split(
        ["游戏设计","UI 系统（点击检测、Canvas、按钮 / 图片 / 文字组件）","性能相关：场景与对象预加载、内存管理"],
        ["引擎框架（老师提供）","核心玩法逻辑（主程）","美术资产与优化"]
      ) + """<div class="note">这个项目让我对引擎底层的理解变得具体：现在看一个 Unity 的 prefab 文本文件，大致就能读懂它在做什么。</div>"""),
    ],
    aside=[("负责内容",["游戏设计","UI 系统（从零实现）","预加载与内存管理"]),("工具",["TypeScript","HTML / Canvas","Blender（像素风渲染）","飞书（需求文档与开发日志）"])],
    prev=("dreams-dont-die.html","Dreams Don't Die"), next=None,
  ),
]

def render(p):
    facts = "".join(f'<div class="fact"><div class="k">{k}</div><div class="v">{v}</div></div>' for k, v in p["facts"])
    body = ""
    for h, c in p["sections"]:
        body += f"<h2>{h}</h2>\n{c}\n"
    aside = ""
    for h, items in p["aside"]:
        aside += f'<div class="aside-box"><h3>{h}</h3><ul>' + "".join(f"<li>{i}</li>" for i in items) + "</ul></div>"
    prev = f'<a href="{p["prev"][0]}"><small>← 上一个</small>{p["prev"][1]}</a>' if p["prev"] else "<span></span>"
    nxt = f'<a href="{p["next"][0]}" style="text-align:right"><small>下一个 →</small>{p["next"][1]}</a>' if p["next"] else "<span></span>"
    return (HEAD.format(title=html.escape(re.sub(r"<[^>]+>", "", p["title"]).strip()), desc=html.escape(p["desc"])) + f"""
<section class="proj-hero">
  <div class="wrap">
    <a class="back" href="index.html#projects">← 返回项目列表</a>
    <h1>{p["title"]}</h1>
    <p class="sub">{p["sub"]}</p>
    <div class="facts">{facts}</div>
  </div>
</section>
<section class="proj-body">
  <div class="wrap">
    <div class="media">{p["hero"]}</div>
    <div class="cols">
      <div>{body}</div>
      <aside>{aside}</aside>
    </div>
    <div class="proj-nav">{prev}{nxt}</div>
  </div>
</section>
""" + FOOT)

here = os.path.dirname(os.path.abspath(__file__))
for p in PROJECTS:
    with open(os.path.join(here, p["file"]), "w", encoding="utf-8") as f:
        f.write(render(p))
    print("wrote", p["file"])
