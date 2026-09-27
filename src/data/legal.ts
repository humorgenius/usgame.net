import type { Lang } from "../i18n";

/**
 * 三页合规文案：隐私政策 / 免责声明 / 联系我们。
 * 中英各自撰写，不做逐句直译 —— 法律文本直译反而两个语言都读不懂。
 *
 * ⚠ 两处只能由站点运营者确认的事实，集中在这里，改一处三页同步：
 *   1. CONTACT_EMAIL —— 必须是真实能收信的邮箱。审核时联系不上会直接影响结果。
 *   2. 广告那一段 —— 必须与站上实际投放的广告方案一致（现在按 Google AdSense 写）。
 */
export interface Block { h: string; p: string[] }
export interface LegalMeta { title: string; description: string; h1: string; lede: string }

export const CONTACT_EMAIL = "guweiicy@gmail.com";
export const LEGAL_UPDATED = "2026-09-26";

export const PRIVACY_META: Record<Lang, LegalMeta> = {
  en: {
    title: "Privacy policy",
    description: "What USGAME does with information when you read it: no accounts, no tracking of our own, and how Google AdSense cookies work here.",
    h1: "Privacy policy",
    lede: "What this site does with information when you read it — and what it deliberately does not do.",
  },
  zh: {
    title: "隐私政策",
    description: "读 USGAME 时本站会怎么处理信息：没有账号、不运行自己的统计，以及 Google AdSense 的 Cookie 在这里是怎么运作的。",
    h1: "隐私政策",
    lede: "你阅读本站时，我们会怎么处理信息 —— 以及我们刻意不做什么。",
  },
};

export const DISCLAIMER_META: Record<Lang, LegalMeta> = {
  en: {
    title: "Disclaimer",
    description: "USGAME is an unofficial fan resource: trademark notice, how we use game footage, and what our guides do and do not promise.",
    h1: "Disclaimer",
    lede: "An unofficial site, and what that means about ownership, accuracy and the material we use.",
  },
  zh: {
    title: "免责声明",
    description: "USGAME 是非官方爱好者站点：商标声明、游戏素材的使用方式，以及本站攻略承诺什么、不承诺什么。",
    h1: "免责声明",
    lede: "这是一个非官方站点 —— 这句话在版权、准确性、素材使用上各自意味着什么。",
  },
};

export const CONTACT_META: Record<Lang, LegalMeta> = {
  en: {
    title: "Contact",
    description: "How to reach USGAME for corrections, rights holder requests, and what we cannot help with.",
    h1: "Contact",
    lede: "One address for corrections, rights holder requests and everything else.",
  },
  zh: {
    title: "联系我们",
    description: "如何联系 USGAME：纠错、权利人请求，以及我们帮不上的事。",
    h1: "联系我们",
    lede: "纠错、权利人请求，以及其余事务，都走同一个地址。",
  },
};

export const PRIVACY: Record<Lang, Block[]> = {
  en: [
    { h: "What this policy covers", p: [
      "This page explains what USGAME does with information when you read it. It applies to usgame.net and to both language versions of the site." ] },
    { h: "What we collect", p: [
      "Nothing that identifies you. USGAME has no accounts, no login and no comment system, so reading an article asks for no personal information and leaves us none.",
      "We run no analytics or tracking scripts of our own. The only data that leaves your browser is what the third parties described below receive." ] },
    { h: "Email and subscriptions", p: [
      "This site does not collect email addresses. There is no newsletter, no sign-up form and no mailing list.",
      "New articles are announced through an RSS feed at usgame.net/en/rss.xml. RSS is a plain file that your own reader fetches on its own schedule, and it works without giving us any address or account. Nothing about your subscription is stored on our side." ] },
    { h: "Advertising and cookies", p: [
      "USGAME displays advertising supplied by Google AdSense. That advertising is what pays for the site.",
      "Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this and other websites.",
      "Google's use of advertising cookies enables it and its partners to serve ads to you based on your visits to this site and to other sites on the internet.",
      "You can opt out of personalised advertising in Google's Ads Settings at google.com/settings/ads. You can also opt out of some third-party vendors' use of cookies for personalised advertising at aboutads.info.",
      "If you are in the EEA, the UK or Switzerland, we ask for consent through a Google-certified consent management platform before any personalised advertising cookie is set. Decline and you will still see advertising, but it will not be personalised." ] },
    { h: "Embedded video", p: [
      "Trailers are embedded from youtube-nocookie.com. In that mode YouTube sets no cookies until you press play. Once you press play, YouTube's and Google's own privacy policies govern what is collected." ] },
    { h: "Server logs", p: [
      "Our hosting provider may keep standard access logs — IP address, browser type, pages requested, timestamp — for security and troubleshooting. We do not use them to identify individual readers." ] },
    { h: "Children", p: [
      "This site is written for a general audience and is not directed at children under 13. We do not knowingly collect personal information from them." ] },
    { h: "Your rights", p: [
      "Depending on where you live, you may be entitled to access, correct or delete personal information held about you, to object to processing, or to opt out of personalised advertising.",
      "We hold no reader accounts, so in most cases there is no identifiable data about you for us to act on. Requests about advertising cookies are handled through the Google links above. Write to us and we will answer honestly about what we do and do not have." ] },
    { h: "Changes to this policy", p: [
      "If this policy changes, the date at the top of this page changes with it. Substantive changes are described on the page itself, not slipped in quietly." ] },
    { h: "Contact", p: [
      `Questions about this policy: ${CONTACT_EMAIL}` ] },
  ],
  zh: [
    { h: "本政策管什么", p: [
      "这一页说明：你阅读 USGAME 时，本站会怎么处理信息。适用范围是 usgame.net 及其两个语言版本。" ] },
    { h: "我们收集什么", p: [
      "不收集能识别你身份的信息。本站没有账号、没有登录、没有评论系统，读一篇文章不需要提供任何资料，也不会留下任何资料。",
      "本站不运行自己的统计或追踪脚本。离开你浏览器的数据，只有下面列明的第三方会收到。" ] },
    { h: "邮箱与订阅", p: [
      "本站不收集邮箱地址。没有邮件列表，首页也没有订阅表单。",
      "新文章通过 RSS 订阅源发布，地址是 usgame.net/zh/rss.xml。RSS 就是一个静态文件，由你自己的阅读器按自己的节奏去取，不需要提供邮箱或账号，我们这边不保存任何订阅信息。" ] },
    { h: "广告与 Cookie", p: [
      "本站展示 Google AdSense 提供的广告。广告收入是本站的运营来源。",
      "包括 Google 在内的第三方广告商，会使用 Cookie 根据你此前访问本站及其他网站的情况投放广告。",
      "Google 通过广告 Cookie，使其自身及其合作伙伴能够基于你访问本站和／或其他网站的情况向你投放广告。",
      "你可以在 Google 广告设置（google.com/settings/ads）里关闭个性化广告；也可以在 aboutads.info 关闭部分第三方广告商的个性化 Cookie。",
      "如果你位于欧洲经济区、英国或瑞士，我们会在写入任何个性化广告 Cookie 之前，通过 Google 认证的同意管理平台征求你的同意。拒绝的话仍然显示广告，但不做个性化。" ] },
    { h: "嵌入的视频", p: [
      "预告片以 youtube-nocookie.com 域名嵌入。这种模式下，你点击播放之前 YouTube 不写入 Cookie；点击播放之后，收集什么由其自身及 Google 的隐私政策决定。" ] },
    { h: "服务器日志", p: [
      "托管服务商可能保留常规访问日志：IP 地址、浏览器类型、访问的页面、时间戳，用于安全与故障排查。我们不用它识别具体的读者。" ] },
    { h: "儿童", p: [
      "本站面向一般受众，不面向 13 岁以下儿童，也不会主动收集其个人信息。" ] },
    { h: "你的权利", p: [
      "依据你所在地区的法律，你可能有权访问、更正或删除我们持有的关于你的个人信息、反对处理，或退出个性化广告。",
      "本站不保存读者账号，因此在多数情况下我们手上并没有你的可识别数据。涉及广告 Cookie 的请求，请通过上面的 Google 链接处理。你也可以来信问，我们会如实告知有什么、没有什么。" ] },
    { h: "政策变更", p: [
      "本政策如有修改，页面顶部的日期会同步更新。实质性变更会在页面上写清楚，不悄悄改。" ] },
    { h: "联系方式", p: [
      `与本政策相关的问题：${CONTACT_EMAIL}` ] },
  ],
};

export const DISCLAIMER: Record<Lang, Block[]> = {
  en: [
    { h: "Not affiliated with Rockstar", p: [
      "USGAME is an independent fan resource. It is not affiliated with, authorised by, sponsored by, or endorsed by Rockstar Games or Take-Two Interactive Software, Inc." ] },
    { h: "Trademarks", p: [
      "Grand Theft Auto, GTA, Rockstar Games and their associated logos are trademarks or registered trademarks of Take-Two Interactive Software, Inc. We use these names only to describe and discuss the games." ] },
    { h: "Footage and artwork", p: [
      "Trailer footage, screenshots and promotional artwork remain the property of their rights holders. We use them for commentary, reporting and news.",
      "If you hold the rights to a piece of material and object to how it is used here, write to us with the URL and we will remove or replace it." ] },
    { h: "Accuracy", p: [
      "Release dates, platforms and pricing are whatever Rockstar officially announces. None of that is ours to decide, and it can change.",
      "Our guides and analysis rest on confirmed information, official materials and public reporting. They can be overtaken before or after launch.",
      "We do not warrant that anything here is complete, free of error, or right for your particular situation." ] },
    { h: "Spoilers", p: [
      "Some articles discuss story, missions or endings. We try to flag that in the title or the opening lines, but we cannot promise to catch every one." ] },
    { h: "External links", p: [
      "We link out to third-party sites. We are not responsible for their content, their privacy practices, or whether they stay online." ] },
    { h: "Not professional advice", p: [
      "Everything here is game coverage and player experience. It is not legal, financial or any other kind of professional advice." ] },
    { h: "Takedown requests", p: [
      `Send requests to ${CONTACT_EMAIL} with the URL and the material in question.` ] },
  ],
  zh: [
    { h: "与 Rockstar 无隶属关系", p: [
      "USGAME 是独立运营的爱好者资料站，与 Rockstar Games 及 Take-Two Interactive Software, Inc. 无隶属、授权、赞助或背书关系。" ] },
    { h: "商标", p: [
      "Grand Theft Auto、GTA、Rockstar Games 及相关标识，是 Take-Two Interactive Software, Inc. 的商标或注册商标。本站仅出于介绍与讨论游戏的目的使用这些名称。" ] },
    { h: "游戏素材与美术资源", p: [
      "预告片画面、截图与宣传图的版权归其权利人所有。本站以评论、报道与资讯为目的使用。",
      "如果你是某项素材的权利人、不同意本站的用法，来信附上链接，我们会移除或替换。" ] },
    { h: "内容准确性", p: [
      "发售日期、平台与定价以 Rockstar 官方公告为准。这些不是本站能决定的，而且会变。",
      "本站的攻略与解析基于已确认信息、官方素材与公开报道，发售前后都可能被新消息推翻。",
      "我们不保证站上内容完整、没有错误，或适用于你的具体情况。" ] },
    { h: "剧透", p: [
      "部分文章会讨论剧情、任务或结局。我们会尽量在标题或开头提示，但没法保证每一处都标到。" ] },
    { h: "外部链接", p: [
      "本站会链向第三方网站。对其内容、隐私做法，或它们是否还在线，我们不负责任。" ] },
    { h: "非专业意见", p: [
      "站上所有内容都是游戏资讯与玩家经验，不构成法律、财务或任何其他专业意见。" ] },
    { h: "下架请求", p: [
      `请将请求发至 ${CONTACT_EMAIL}，附上链接与涉及的素材。` ] },
  ],
};

export const CONTACT: Record<Lang, Block[]> = {
  en: [
    { h: "Corrections", p: [
      `Spotted a mistake? Write to ${CONTACT_EMAIL} with the page. Errors are corrected in place, and the date we changed them is noted.` ] },
    { h: "Rights holders", p: [
      "If you hold rights to material used here and want it changed or removed, use the same address and include the URL. These are handled first." ] },
    { h: "What we cannot help with", p: [
      "We do not supply game keys, accounts, mods, cracks or cheats, and we do not pass on leaked material. Requests of that kind get no reply." ] },
    { h: "Response times", p: [
      "The site is run by a small number of people, so a reply can take a few working days. We read everything; we cannot promise an answer to every message." ] },
  ],
  zh: [
    { h: "纠错", p: [
      `发现错误？把页面链接发到 ${CONTACT_EMAIL}。我们在原文处改正，并标注修改日期。` ] },
    { h: "权利人", p: [
      "如果你是站上某项素材的权利人、希望修改或移除，走同一个地址，附上链接即可。这类请求优先处理。" ] },
    { h: "我们帮不上的事", p: [
      "本站不提供游戏激活码、账号、MOD、破解或外挂，也不转手泄露素材。这类请求不会回复。" ] },
    { h: "回复时效", p: [
      "本站由少数几个人维护，回复可能需要几个工作日。每一封我们都会看；但没法保证每一封都回。" ] },
  ],
};
