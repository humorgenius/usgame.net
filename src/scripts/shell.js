// 站点外壳交互：汉堡菜单、搜索行、首页新闻筛选、订阅表单。
// 与设计稿 A 的 <script> 同源，改了三处：
//   1. 不再有「正文语言落地」这一步。以前首页文案是 data-en/data-zh 双份标记，
//      靠这里在浏览器里换成中文 —— 那等于 /zh/ 的 HTML 源码是英文，爬虫和
//      AdSense 审核员看到的都是英文。现在文案在构建期就按语言渲染好了。
//   2. 删掉 localStorage 记忆：它会让 /en/ 的页面被浏览器渲染成中文（跨语言串味）。
//   3. 所有 getElementById 都加空值判断：文章页没有 #newsGrid/#copyFeed，
//      原来会直接抛错，把后面的脚本一起打断。
(function () {
  'use strict';
/* ---------- 2. 汉堡菜单 ---------------------------------------------- */
  var burger = document.getElementById('burger');
  var mnav = document.getElementById('mobileNav');
  function setMenu(open) {
    if (!burger || !mnav) return;
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    mnav.hidden = !open;
  }
  if (burger && mnav) {
    burger.addEventListener('click', function () {
      setMenu(burger.getAttribute('aria-expanded') !== 'true');
    });
    mnav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { setMenu(false); });
    });
  }

  /* ---------- 3. 搜索行 ------------------------------------------------ */
  var sToggle = document.getElementById('searchToggle');
  var sRow = document.getElementById('searchRow');
  var sInput = document.getElementById('searchInput');
  if (sToggle && sRow && sInput) {
    sToggle.addEventListener('click', function () {
      var open = sToggle.getAttribute('aria-expanded') !== 'true';
      sToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      sRow.hidden = !open;
      if (open) sInput.focus();
    });
  }
  // 搜索表单不再吃掉提交：它现在是原生 GET，提交后跳到 /{lang}/search/?q=…
  // 以前这里只 preventDefault()，所以点「搜索」什么都不会发生 —— 那就是它"不能用"的原因。

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (burger && burger.getAttribute('aria-expanded') === 'true') { setMenu(false); burger.focus(); }
    if (sToggle && sToggle.getAttribute('aria-expanded') === 'true') {
      sToggle.setAttribute('aria-expanded', 'false');
      if (sRow) sRow.hidden = true;
      sToggle.focus();
    }
  });

  /* ---------- 4. 首页新闻筛选 ------------------------------------------ */
  var tabs = [].slice.call(document.querySelectorAll('.tab'));
  var cards = [].slice.call(document.querySelectorAll('#newsGrid .news-card'));
  var count = document.getElementById('newsCount');
  if (tabs.length && count) {
    tabs.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var f = btn.getAttribute('data-filter');
        tabs.forEach(function (b) { b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'); });
        var shown = 0;
        cards.forEach(function (c) {
          var show = f === 'all' || c.getAttribute('data-cat') === f;
          c.hidden = !show;
          if (show) shown++;
        });
        count.textContent = shown;
      });
    });
  }

  /* ---------- 5. 订阅表单（仅前端） ------------------------------------ */
/* ---------- 复制网址（收藏夹面板用）---------------------------------- */
  // 读者要把网址存下来或发给别人，点一下复制比手动选中省事。
  // navigator.clipboard 只在「安全上下文」（https 或 localhost）可用，
  // http 下要有退路，否则按钮看着是活的、点了没反应。
  var copyBtn = document.getElementById('copyUrl');
  if (copyBtn) copyBtn.addEventListener('click', function () {
    var path = copyBtn.getAttribute('data-copy') || '/';
    var url = new URL(path, location.origin).href;
    var done = copyBtn.getAttribute('data-copied') || '已复制';
    var orig = copyBtn.textContent;
    var flash = function () {
      copyBtn.textContent = done;
      setTimeout(function () { copyBtn.textContent = orig; }, 2000);
    };
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(url).then(flash, flash);
    } else {
      // 非安全上下文（比如用局域网 IP 打开 http 页面）没有剪贴板 API。
      // 不硬来：网址就印在面板里，直接提示读者手动选中即可 ——
      // 比为了兼容这一种情况去调用已弃用的 execCommand 更干净。
      copyBtn.textContent = copyBtn.getAttribute('data-manual') || '手动复制网址';
      setTimeout(function () { copyBtn.textContent = orig; }, 3000);
    }
  });

  /* ---------- 6. 视频停靠：播放中的视频滚出视口后，自动浮到右下角继续播放 ------ */
  /* 两道技术关，都是先在浏览器里做实验验证过才这么写的：
     ① 不能搬 DOM。iframe 一旦被 appendChild 搬到别的父节点，浏览器会把它重新
        加载一遍，视频从头开始 —— 所以只换定位方式（position:fixed），元素始终
        留在原来那个父节点里，播放进度不受影响。
     ② 跨域 iframe 读不到播放状态，只能用 postMessage 向播放器问。播放器只对带
        enablejsapi=1 的嵌入回应（已写进源码，入库脚本里也兜住了）。
        握手时传进去的 id 会被播放器原样带回来，一页有多个播放器时靠它分辨来源。 */
  (function videoDock() {
    var frames = [].slice.call(document.querySelectorAll(
      'iframe[src*="youtube-nocookie.com/embed"], iframe[src*="youtube.com/embed"]'));
    if (!frames.length || !window.postMessage || !window.requestAnimationFrame) return;

    var players = [], docked = null, closeBtn = null, ticking = false;
    var isZh = (document.documentElement.getAttribute('lang') || '').indexOf('zh') === 0;

    frames.forEach(function (frame, i) {
      // 首页那种被 .vid-frame 包着的，停靠外层容器（里面的 iframe 是绝对定位铺满的）；
      // 文章正文里的裸 iframe，就停靠它自己。
      var host = (frame.parentElement && frame.parentElement.classList.contains('vid-frame'))
        ? frame.parentElement : frame;
      players.push({ frame: frame, host: host, id: 'vdock' + i, state: null, spacer: null });
    });

    function hello(p) {
      try {
        p.frame.contentWindow.postMessage(
          '{"event":"listening","id":"' + p.id + '","channel":"widget"}', '*');
      } catch (e) { /* 播放器可能还没就绪，load 之后再试一次 */ }
    }
    players.forEach(function (p) {
      hello(p);
      p.frame.addEventListener('load', function () { hello(p); });
    });

    /* 播放器回报的状态：-1 未开始 / 0 播完 / 1 播放中 / 2 暂停 / 3 缓冲 / 5 已就绪
       坑（实测踩过）：真播放器的状态**不是**用 onStateChange 报的 —— 那是 IFrame API
       那个库自己从轮询里合成出来的。裸 postMessage 通道收到的是
       {"event":"infoDelivery","info":{"playerState":1,"currentTime":…}}，
       而且它会**周期性重复上报**（同一状态每秒来好几条）。
       所以两种事件都认，并且只在状态**变化**时才动作。 */
    window.addEventListener('message', function (e) {
      if (e.origin !== 'https://www.youtube-nocookie.com' &&
          e.origin !== 'https://www.youtube.com') return;
      if (typeof e.data !== 'string') return;
      var msg;
      try { msg = JSON.parse(e.data.replace(/^[^{]*/, '')); } catch (err) { return; }
      if (!msg || !msg.event) return;
      var st = null;
      if (msg.event === 'onStateChange') {
        st = msg.info;
      } else if (msg.event === 'infoDelivery' && msg.info &&
                 typeof msg.info.playerState === 'number') {
        st = msg.info.playerState;
      }
      if (typeof st !== 'number') return;
      var p = null;
      for (var i = 0; i < players.length; i++) {
        if (players[i].id === msg.id && players[i].frame.contentWindow === e.source) { p = players[i]; break; }
      }
      if (!p || st === p.state) return;               // 只认变化，忽略重复上报
      p.state = st;
      if (st === 1) {                                 // 开始播放
        if (docked && docked !== p) undock();          // 同一时刻只留一个浮窗
        sync();
      } else if (st === 0 || st === 2 || st === 5 || st === -1) {
        if (docked === p) undock();
      }
      /* 3（缓冲）什么都不做：网络抖一下不该让浮窗闪进闪出 */
    });

    /* 量「这个视频还有多少露在视口里」。
       坑：一旦浮起来，host 是 position:fixed，它的 rect 读出来是右下角那个位置、
       永远"完全可见" —— 拿它判断可见性会立刻得出"已经回到视野"，浮窗刚浮起就把
       自己撤回，来回打架。所以浮起状态下必须量原位那个占位元素（它才是留在文档流里
       的那个），撤回后再回到量 host 本身。 */
    function seen(p) {
      var el = (docked === p && p.spacer) ? p.spacer : p.host;
      var r = el.getBoundingClientRect();
      var vis = Math.min(r.bottom, window.innerHeight) - Math.max(r.top, 0);
      return { h: r.height, part: r.height ? vis / r.height : 0 };
    }

    function sync() {
      var target = null;
      for (var i = 0; i < players.length; i++) {
        if (players[i].state === 1) { target = players[i]; break; }
      }
      if (!target) { undock(); return; }
      var m = seen(target);
      if (docked === target) {
        if (m.part > 0.65) undock();                   // 又滚回视口里了，撤回原位
        else place();
      } else {
        undock();
        if (m.part < 0.4) dock(target, m.h);           // 被遮住一大半才浮起来
      }
    }

    function dock(p, h) {
      var sp = document.createElement('div');          // 原位占位，防止内容往上跳
      sp.className = 'vid-dock-spacer';
      sp.style.height = h + 'px';
      // 正文里从 Word 带过来的嵌入是**行内** iframe：行盒在基线以下还留一段间隙，
      // 占位若用块级元素会矮掉约 10px，浮起时下方内容仍会轻微上移。
      // 让占位跟着原元素的 display 走、宽度照抄，行盒才算得一模一样。
      if (getComputedStyle(p.host).display === 'inline') {
        sp.style.display = 'inline-block';
        sp.style.width = p.host.getBoundingClientRect().width + 'px';
      }
      p.host.parentNode.insertBefore(sp, p.host);
      p.spacer = sp;
      p.host.classList.add('is-docked');
      if (!closeBtn) {
        closeBtn = document.createElement('button');
        closeBtn.type = 'button';
        closeBtn.className = 'vid-dock-close';
        closeBtn.textContent = '\u00D7';
        var label = isZh ? '关闭浮窗（同时暂停视频）'
                         : 'Close the floating player (also pauses the video)';
        closeBtn.setAttribute('aria-label', label);
        closeBtn.title = label;
        document.body.appendChild(closeBtn);
      }
      closeBtn.hidden = false;
      closeBtn.onclick = function () {
        try {
          p.frame.contentWindow.postMessage(
            '{"event":"command","func":"pauseVideo","args":""}', '*');
        } catch (e) {}
        if (p.state === 1) p.state = 2;   // 否则下一帧又判定成"播放中"，浮窗立刻弹回来
        undock();
      };
      docked = p;
      place();
    }

    function undock() {
      if (!docked) return;
      docked.host.classList.remove('is-docked');
      if (docked.spacer && docked.spacer.parentNode) {
        docked.spacer.parentNode.removeChild(docked.spacer);
      }
      docked.spacer = null;
      docked = null;
      if (closeBtn) closeBtn.hidden = true;
    }

    /* 关闭按钮贴浮窗右上角。浮窗高度由宽度换算，让 JS 量一次比在 CSS 里推公式稳。 */
    function place() {
      if (!docked || !closeBtn) return;
      var r = docked.host.getBoundingClientRect();
      closeBtn.style.right = (window.innerWidth - r.right + 6) + 'px';
      closeBtn.style.top = (r.top - 15) + 'px';
    }

    function onScroll() {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(function () { ticking = false; sync(); });
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', function () { sync(); if (docked) place(); });
  })();

})();
