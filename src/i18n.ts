/**
 * 站点语言与栏目表 —— 全站唯一真相。
 * 中英共用同一套 slug（scripts/ingest.py 用英文 slug 给两种语言命名），
 * 也共用同一套栏目键，所以「换语言」只是换 URL 前缀，落到的是同一篇文章。
 */
export const LANGS = ["en", "zh"] as const;
export type Lang = (typeof LANGS)[number];

export const isLang = (v: string | undefined): v is Lang =>
  v === "en" || v === "zh";

export interface Sub { k: string; en: string; zh: string }
export interface Sec { k: string; en: string; zh: string; subs?: Sub[] }

/** 顺序 = 页头导航顺序（照抄设计稿 A，不动它的视觉节奏） */
export const SECTIONS: Sec[] = [
  { k: "news", en: "News", zh: "新闻" },
  {
    k: "guides", en: "Guides", zh: "攻略",
    subs: [
      { k: "systems",    en: "Systems",         zh: "机制" },
      { k: "crime",      en: "Crime & Wanted",  zh: "犯罪与通缉" },
      { k: "story",      en: "Story",           zh: "剧情解析" },
      { k: "world",      en: "World",           zh: "世界生态" },
      { k: "activities", en: "Activities",      zh: "活动探索" },
    ],
  },
  { k: "map",        en: "Map & Collectibles", zh: "地图与收集" },
  { k: "characters", en: "Characters",         zh: "角色" },
  { k: "vehicles",   en: "Vehicles",           zh: "载具" },
  { k: "weapons",    en: "Weapons",            zh: "武器" },
  { k: "videos",     en: "Videos",             zh: "视频" },
  { k: "faq",        en: "FAQ",                zh: "常见问题" },
];

export const SITE = { name: "USGAME", origin: "https://usgame.net" };

/**
 * AdSense 发布商 ID —— 全站唯一。模板里别再散写这串字符串。
 * 用法只有一处（Base.astro 的 <head>）：一条 adsbygoogle 标签 + 一个归属校验 meta。
 * 本站不设任何广告位，广告靠账号里的「自动广告」投放。
 */
export const ADSENSE_CLIENT = "ca-pub-9680789453651246";

export const secOf = (k: string) => SECTIONS.find((s) => s.k === k);
export const sectionLabel = (k: string, lang: Lang) => secOf(k)?.[lang] ?? k;
export const sectionPath = (lang: Lang, k: string) => `/${lang}/${k}/`;
export const articlePath = (lang: Lang, k: string, slug: string) =>
  `/${lang}/${k}/${slug}/`;

export function subLabel(sec: string, sub: string | null, lang: Lang) {
  const s = secOf(sec)?.subs?.find((x) => x.k === sub);
  return s ? s[lang] : "";
}

/**
 * 换语言的 URL。因为 slug 与栏目键中英一致，换前缀 = 同一篇文章/同一个栏目页，
 * 绝不会退回首页（lilink 踩过的坑）。
 */
export function switchLang(pathname: string, to: Lang) {
  return /^\/(en|zh)(\/|$)/.test(pathname)
    ? pathname.replace(/^\/(en|zh)/, `/${to}`)
    : `/${to}/`;
}

/** 栏目页的导语与 SEO 文案 */
export const SECTION_INTRO: Record<string, { en: string; zh: string }> = {
  news:     { en: "Everything officially confirmed about GTA6: dates, platforms, pricing and announcements.", zh: "关于《GTA6》已被官方确认的一切：时间、平台、定价与公告。" },
  guides:   { en: "Systems, crime, story and the open world, broken down system by system.", zh: "机制、犯罪、剧情与开放世界，逐系统拆解。" },
  map:      { en: "Leonida region by region: districts, wetlands, beaches and what is buried in them.", zh: "雷欧奈达州逐区拆解：街区、湿地、海滩，以及埋在里面的东西。" },
  characters:{ en: "Who is who in Vice City — the full cast, their motives and where they fit.", zh: "罪恶城里谁是谁——全部角色、他们的动机与位置。" },
  vehicles: { en: "Cars, boats, aircraft: how driving, tuning and flight actually work.", zh: "车、船、飞行器：驾驶、改装与飞行到底怎么运作。" },
  weapons:  { en: "The weapon system, from infinite pockets to deliberate loadouts.", zh: "武器系统：从无限口袋到需要取舍的配装。" },
  videos:   { en: "Official trailers and footage, frame by frame.", zh: "官方预告片与影像，逐帧解析。" },
  faq:      { en: "The questions readers ask most, answered plainly.", zh: "读者最常问的问题，直给答案。" },
};

/** 界面文案（页头、文章页、页脚） */
export const UI = {
  skip:      { en: "Skip to content",          zh: "跳到正文" },
  search:    { en: "Search",                   zh: "搜索" },
  searchPh:  { en: "Search news, guides, weapons…", zh: "搜索新闻、攻略、武器…" },
  searchH1:  { en: "Search the site",           zh: "站内搜索" },
  searchHint:{ en: "Type a word. Titles, summaries and in-page section headings are all searched. Leave it empty to browse every article in order.",
               zh: "输入关键词即可，标题、摘要和文中的小标题都会被搜到。留空则按原稿顺序浏览全部文章。" },
  searchFound:{ en: "{n} matching articles",    zh: "找到 {n} 篇" },
  searchNone:{ en: "No article matches “{q}”. Try a shorter word, or browse the list below.",
               zh: "没有匹配“{q}”的文章。换个短一点的词，或直接在下面的列表里翻。" },
  searchNoJs:{ en: "Filtering needs JavaScript. Below is the full list of articles.",
               zh: "关键词过滤需要 JavaScript。下面是全部文章的完整列表。" },
  menu:      { en: "Menu",                     zh: "菜单" },
  language:  { en: "Language",                 zh: "语言" },
  home:      { en: "Home",                     zh: "首页" },
  about:     { en: "About",                    zh: "关于" },
  articles:  { en: "articles",                 zh: "篇文章" },
  onThisPage:{ en: "On this page",             zh: "本页目录" },
  mostRead:  { en: "Most read",                zh: "最多人读" },
  keepReading:{ en: "Keep reading",            zh: "继续阅读" },
  allIn:     { en: "All",                      zh: "全部" },
  previous:  { en: "Previous",                 zh: "上一篇" },
  next:      { en: "Next",                     zh: "下一篇" },
  published: { en: "Published",                zh: "发布于" },
  updated:   { en: "Updated",                  zh: "更新于" },
  minRead:   { en: "min read",                 zh: "分钟阅读" },
  staff:     { en: "USGAME staff",             zh: "USGAME 编辑部" },
  latest:    { en: "Latest",                   zh: "最新" },
  backToTop: { en: "Back to top",              zh: "返回顶部" },
  notFound:  { en: "Page not found",           zh: "页面不存在" },
  browse:    { en: "Browse all sections",      zh: "浏览全部栏目" },
  related:   { en: "More in",                  zh: "同栏目更多" },
  site:      { en: "Site",                     zh: "关于本站" },
  privacy:   { en: "Privacy policy",           zh: "隐私政策" },
  disclaimer:{ en: "Disclaimer",               zh: "免责声明" },
  contact:   { en: "Contact",                  zh: "联系我们" },
  legalUpdated: { en: "Last updated",          zh: "最近更新" },
} as const;

export type UIKey = keyof typeof UI;
export const t = (key: UIKey, lang: Lang) => UI[key][lang];

/**
 * 阅读时长。中文按字、英文按词 —— 同一套公式套两种语言会得出离谱数字。
 * 首页卡片和文章页共用这一份。
 */
export function readingMinutes(body: string | undefined, lang: Lang) {
  const raw = (body ?? "").replace(/[#>*`|!\[\]()\-]/g, " ");
  const cjk = [...raw].filter((c) => {
    const n = c.charCodeAt(0);
    return n > 0x2e80 && n < 0xa000;
  }).length;
  const words = raw.trim().split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.round(lang === "zh" ? cjk / 450 : words / 220));
}

/** 面包屑/标签用的「栏目 · 子类」 */
export const crumbTag = (sec: string, sub: string | null, lang: Lang) =>
  [sectionLabel(sec, lang), subLabel(sec, sub, lang)].filter(Boolean).join(" · ");
