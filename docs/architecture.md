# usgame.net — GTA VI 专题站 架构规划

> 状态：待你确认 · 版本：v1 · 日期：2026-09-26
> 目标目录：`D:\【建立网站】\GTA6\usgame.net\`
> 域名：`usgame.net`（已购买）

---

## 0. 结论摘要

| 决策项 | 结论 | 一句话理由 |
|---|---|---|
| 技术栈 | **Astro 7 + Tailwind CSS 4 + 极小量原生 JS 岛** | 与你已上线的 lilink.net 同栈，本机环境已验证；输出纯静态 HTML，正文不依赖 JS，对 AdSense 与 SEO 最友好 |
| 语音路由 | `/en/…` 与 `/zh/…`，`prefixDefaultLocale: true` | 每种语言都有独立可爬路径，hreflang 三向互指 |
| 页面规模 | 路由模板 27 类，首期产出 **约 160 个 HTML 文件**（80 个路由 × 2 语言） | 远超 20 页要求，且每页都有独立关键词，不互相竞争 |
| 交互实现 | 语言切换、主题、筛选、搜索、目录、返回顶部 —— 全部原生 JS，首屏 JS < 30KB | 纯静态约束下无死角 |
| 地图/收集品 | 自绘 SVG 地图 + 坐标数据 JSON | 不依赖任何地图 API 的免费额度与 CORS |
| 广告 | 4 类位置 + 策略化投放 + `ads.txt` + Google CMP | 满足"不隐藏、不堆砌、不误导" |
| 站点体积 | 预算 < 300MB（上限 1GB 的 30%） | 图片走 AVIF/WebP + srcset |
| 站名 | **待你拍板**（见第 12 节） | 影响所有页面 wordmark 与所有 JSON-LD 节点 |

**当前阶段交付**：本规划文档 + `design/` 下 5 个风格不同的首页 HTML 方案。选型确定后才进入写代码阶段。

---

## 1. 站点定位

**一句话**：面向全球玩家的 GTA VI 新闻与攻略站 —— 官方消息、预告片逐帧解析、剧情角色档案、雷欧奈达地图与收集品、载具武器数据、任务攻略、版本更新日志。

**读者与搜索意图**（决定关键词与页面结构）：

| 读者 | 他在搜什么 | 对应页面 |
|---|---|---|
| 未购入的观望者 | "gta 6 release date" / "GTA6 什么时候出" / "gta 6 price" | 首页、新闻、FAQ、价格解析 |
| 刚开服的玩家 | "gta 6 wanted level" / "GTA6 怎么赚钱" / "gta 6 first hours" | 攻略、机制深度、经济 |
| 通关中的收集党 | "gta 6 all collectibles" / "GTA6 收集品位置" | 地图、收集品清单 |
| 剧情与角色粉 | "gta 6 characters" / "GTA6 杰森 露西亚" | 角色库、剧情解析 |
| 数据党 | "gta 6 vehicle stats" / "GTA6 武器数值" | 载具图鉴、武器图鉴 |

**内容基调**：R 星式的自信、具体、带点血腥味。短句、真实数字、有来源标注。**不写**"欢迎来到我们的网站，您的一站式目的地"这类话。

---

## 2. 技术栈确认

### 采用

| 层 | 选型 | 理由 |
|---|---|---|
| 生成器 | **Astro 7**，`output: 'static'` | 零 JS 默认输出；布局/组件可复用；160 个页面靠模板批量生成而不是手写 |
| 样式 | **Tailwind CSS 4**（`@tailwindcss/vite` 插件，免 config 文件） | 与 lilink.net 一致；4.x 用 CSS-first 配置；产物自动裁剪 |
| 内容 | **Astro Content Collections + MDX** | 有 schema 校验，frontmatter 缺字段直接构建失败，避免上线才发现 |
| 交互岛 | **原生 `<script>`（默认）**，必要时 1 个 Preact 岛 | 语言切换/主题/筛选/搜索都不需要框架；引入框架只为几乎没有的状态管理不划算 |
| 地图 | **自绘 SVG + JSON 坐标** | 零依赖、零额度、零 CORS |
| 图片 | `astro:assets` + sharp → **AVIF/WebP + srcset** | 96 张原图 88MB，必须构建期压缩 |
| 站点地图 | `@astrojs/sitemap`（带 i18n 配置） | 自动生成 hreflang 备用链接，不用手维护 160 条 |
| 字体 | **自托管**（`@fontsource/*`），`font-display: swap`，子集化 | 不请求 Google Fonts 域名：更快、更少一次第三方连接、也不会因墙/代理抖动 |
| 校验 | Node 脚本：`check-i18n` / `check-seo` / `check-links` / `verify-pages` | 门禁必须能在构建后跑，不能靠肉眼看 |

### 已否决的方案

| 方案 | 否决理由 |
|---|---|
| Vite + 手写 HTML | 160 个页面 = 160 个手写文件。改一次导航要改 160 处，必然漏改，且导航不一致本身就是低质信号 |
| Next.js 静态导出 | 为内容站引入 React 运行时与更重的构建链，收益为零；`next export` 的 i18n 路由比 Astro 啰嗦 |
| 纯 HTML + 一个 JS 模板在客户端渲染 | 关键内容靠 JS 生成 —— 直接踩你需求里"所有页面均可被搜索引擎独立爬取（无 JS 强制渲染关键内容）"这条红线 |
| 引入 Leaflet/MapLibre 做真地图 | 免费瓦片有额度与条款限制，游戏地图也没有公开瓦片源；自绘 SVG 反而能做出更贴游戏风格的"手绘地图" |

---

## 3. 目录结构

```
usgame.net/
├─ astro.config.mjs            # site、i18n、sitemap、tailwind 插件
├─ package.json                # scripts: dev / build / check:* / verify:*
├─ tsconfig.json
├─ public/
│  ├─ ads.txt                    # ca-pub-9680789453651246
│  ├─ robots.txt                 # 放行全站，声明 sitemap，屏蔽 /search 参数页
│  ├─ llms.txt                   # GEO：中英双语站点摘要 + 页面清单
│  ├─ favicon.svg / icon-192.png / apple-touch-icon.png
│  └─ og/                        # 每页 Open Graph 图（构建期生成或预置）
│
├─ src/
│  ├─ i18n/
│  │  ├─ ui.ts                   # 全部界面字符串 EN/ZH（单一真相）
│  │  ├─ routes.ts               # route key → { en: '/news/', zh: '/zh/news/' }
│  │  │                          #   ← 语言切换与 hreflang 都读它，绝不靠 URL 字符串拼接
│  │  └─ utils.ts                # t() / localePath() / altLinks() / switchLocalePath()
│  │
│  ├─ content/                   # 内容集合，每种语言一个子目录
│  │  ├─ config.ts               # zod schema（title/desc/date/updated/tags/source/cover…）
│  │  ├─ news/{en,zh}/*.mdx
│  │  ├─ guides/{en,zh}/*.mdx
│  │  ├─ characters/{en,zh}/*.mdx
│  │  ├─ map/{en,zh}/*.mdx
│  │  ├─ vehicles/{en,zh}/*.mdx
│  │  ├─ weapons/{en,zh}/*.mdx
│  │  ├─ videos/{en,zh}/*.mdx
│  │  ├─ updates/{en,zh}/*.mdx
│  │  ├─ faq/{en,zh}/*.mdx
│  │  └─ blog/{en,zh}/*.mdx
│  │
│  ├─ data/                      # 非文章型数据
│  │  ├─ site.ts                 # 品牌、域名、AdSense ID、社交、免责声明
│  │  ├─ nav.ts                  # 导航（含二级菜单）
│  │  ├─ quick-entries.ts        # 首页 8 个快速入口
│  │  ├─ stats.ts                # 数字带
│  │  ├─ collectibles.ts         # 收集品坐标 + 分类
│  │  ├─ map-regions.ts          # SVG 区域路径 + 热点
│  │  └─ keywords.ts             # ★ 关键词→页面映射（SEO 单一真相）
│  │
│  ├─ layouts/
│  │  ├─ BaseLayout.astro        # <head> 全套 meta + JSON-LD + skip link
│  │  ├─ IndexLayout.astro       # 列表页
│  │  └─ ArticleLayout.astro     # 文章页（目录 / 相关推荐 / 上下篇 / 广告）
│  │
│  ├─ components/
│  │  ├─ seo/     Meta · Hreflang · Canonical · JsonLd · Breadcrumbs
│  │  ├─ chrome/  Header · Nav · LangSwitch · ThemeToggle · SearchBox · MobileMenu · Footer · BackToTop
│  │  ├─ ads/     AdSlot · AdLabel · AdRail
│  │  ├─ media/   YouTubeFacade · Figure · LazyImage · VideoCard
│  │  └─ content/ NewsCard · GuideRow · CharacterCard · VehicleTable · FaqList · Toc · Related · TagPill · SourceLine
│  │
│  ├─ pages/
│  │  ├─ index.astro             # 语言网关（见 5.2）
│  │  ├─ 404.astro
│  │  ├─ search-index.json.ts    # 构建期生成全站搜索索引
│  │  └─ [locale]/…              # 全部真实页面
│  │
│  ├─ scripts/                   # 客户端：lang · theme · filter · search · toc · backtotop
│  └─ styles/global.css
│
├─ scripts/                      # 构建期门禁
│  ├─ check-i18n.mjs             # 两种语言页面数一致 / 无缺失翻译 / 无残留占位
│  ├─ check-seo.mjs              # title/desc 长度、canonical、hreflang、JSON-LD 可解析
│  ├─ check-links.mjs            # 站内死链、去重
│  ├─ verify-pages.mjs           # 构建产物断言（见第 9 节）
│  └─ optimize-images.mjs        # 原图 → AVIF/WebP + srcset
│
├─ docs/
│  ├─ architecture.md            # 本文档
│  ├─ page-list.md               # 页面清单（含关键词落点）
│  ├─ keyword-map.md             # 关键词→页面映射（SEO 门禁读它）
│  └─ content-plan.md            # 内容生产计划（中文稿 → 英文版）
│
└─ design/                       # 本阶段产物
   ├─ content-pack.json
   ├─ BRIEF-common.md / BRIEF-stances.md
   ├─ assets/img/*.webp
   └─ A-neon-vice/ B-newsroom-editorial/ C-heist-dossier/ D-poster-magazine/ E-bento-portal/
```

---

## 4. 页面清单

**27 个路由模板。首期实际产出约 160 个 HTML 文件**（80 个路由 × 2 语言）。
每页**一个短关键词 + 一个长尾**，且中英文各自独立取词（不是翻译关系 —— 中英文用户的搜索词不同）。

### 4.1 核心页

| # | route key | EN | ZH | 主关键词 EN / ZH |
|---|---|---|---|---|
| 1 | `home` | `/en/` | `/zh/` | `gta 6` / `GTA6` |
| 2 | `newsList` | `/en/news/` | `/zh/news/` | `gta 6 news` / `GTA6 新闻` |
| 3 | `newsDetail` | `/en/news/{slug}/` | `/zh/news/{slug}/` | 每篇一个长尾（如 `gta 6 release date`） |
| 4 | `guidesHub` | `/en/guides/` | `/zh/guides/` | `gta 6 guides` / `GTA6 攻略` |
| 5 | `guidesCategory` | `/en/guides/{cat}/` | `/zh/guides/{cat}/` | `gta 6 {cat}` / `GTA6 {分类}` |
| 6 | `guideDetail` | `/en/guides/{slug}/` | `/zh/guides/{slug}/` | 长尾（如 `gta 6 wanted level`） |
| 7 | `mapHub` | `/en/map/` | `/zh/map/` | `gta 6 map` / `GTA6 地图` |
| 8 | `mapRegion` | `/en/map/{region}/` | `/zh/map/{region}/` | `gta 6 vice city map` / `GTA6 罪恶城 地图` |
| 9 | `collectibles` | `/en/collectibles/` | `/zh/collectibles/` | `gta 6 collectibles` / `GTA6 收集品` |
| 10 | `charactersHub` | `/en/characters/` | `/zh/characters/` | `gta 6 characters` / `GTA6 角色` |
| 11 | `characterDetail` | `/en/characters/{slug}/` | `/zh/characters/{slug}/` | `gta 6 lucia` / `GTA6 露西亚` |
| 12 | `vehiclesHub` | `/en/vehicles/` | `/zh/vehicles/` | `gta 6 vehicles` / `GTA6 载具` |
| 13 | `vehiclesClass` | `/en/vehicles/{class}/` | `/zh/vehicles/{class}/` | `gta 6 boats` / `GTA6 水上载具` |
| 14 | `weaponsHub` | `/en/weapons/` | `/zh/weapons/` | `gta 6 weapons` / `GTA6 武器` |
| 15 | `videos` | `/en/videos/` | `/zh/videos/` | `gta 6 trailer` / `GTA6 预告片` |
| 16 | `updates` | `/en/updates/` | `/zh/updates/` | `gta 6 patch notes` / `GTA6 更新日志` |

### 4.2 内容与信任页（AdSense 审核看的就是这批）

| # | route key | EN | ZH | 说明 |
|---|---|---|---|---|
| 17 | `blogHub` | `/en/blog/` | `/zh/blog/` | 深度长文列表（对 SEO 权重最高的一批） |
| 18 | `blogDetail` | `/en/blog/{slug}/` | `/zh/blog/{slug}/` | 8–12 篇首发 |
| 19 | `faq` | `/en/faq/` | `/zh/faq/` | 30 条问答，`FAQPage` 结构化 |
| 20 | `glossary` | `/en/glossary/` | `/zh/glossary/` | 术语表（GEO 抓手，AI 引擎爱引用定义） |
| 21 | `community` | `/en/community/` | `/zh/community/` | 玩家分享 / 案例（首发占位，后续开放投稿） |
| 22 | `about` | `/en/about/` | `/zh/about/` | 谁在做、怎么做、内容来源与更正政策 —— **AdSense 必看** |
| 23 | `contact` | `/en/contact/` | `/zh/contact/` | 联系与纠错渠道（纯前端表单 + 邮箱） |
| 24 | `privacy` | `/en/privacy/` | `/zh/privacy/` | 含 Cookie / 第三方广告 / GDPR 段 |
| 25 | `disclaimer` | `/en/disclaimer/` | `/zh/disclaimer/` | 非官方、商标归属、攻略不保证 |
| 26 | `search` | `/en/search/` | `/zh/search/` | 站内搜索（`noindex`，不放广告） |
| 27 | `notFound` | `/404` | — | 单页，`noindex`，不放广告 |

### 4.3 与你现有内容的映射（关键：不用从零写）

`D:\【建立网站】\GTA6\GTA6游戏图文内容\` 里已有 **80 篇中文成稿**，可以直接对号入座：

| 内容簇 | 归属页面 | 你已有的稿件（举例） |
|---|---|---|
| 发售与商业 | 新闻 / FAQ / 博客 | 发售时间全解析、价格全解析、预计销量、与 R 星财报信息 |
| 官方消息与爆料 | 新闻 | Rockstar 官方消息汇总、上市前泄露信息汇总、试玩爆料 |
| 预告片 | 视频 | 预告片解析（Trailer 1 → Extended Look）、预告片细节解析 |
| 地图与区域 | 地图 / 地图分区 | 地图介绍、城市街区、沼泽区域、海滩场景、真实原型城市 |
| 剧情与角色 | 角色库 | 全部角色背景一览 + 12 篇单人角色档案（露西亚、杰森、波比·艾克…） |
| 玩法机制 | 攻略 / 机制 | 通缉等级、警察追捕、证人系统、新交互系统、天气系统、体态系统 |
| 犯罪与任务 | 攻略 / 任务 | 犯罪任务详解、抢劫机制、犯罪类型 |
| 载具与武器 | 图鉴 | 载具系统、飞机与直升机、水上载具、武器系统 |
| 经济与资产 | 攻略 / 经济 | 资产系统、房产与安全屋、钱在手里才叫钱、购物与消费 |
| 收集与探索 | 收集品 | 宝藏系统、自由探索奖励 |
| 技术与画质 | 博客 | 画质对比 GTA5、动画技术、面部表情技术、NPC AI、路人 AI |
| 周边话题 | 博客 | MOD 支持、PC 版上线时间、线上模式、评级详解、配置要求 |

**结论**：不是"20 个占位页"，而是"80 篇真实内容 + 完整框架"。这直接决定 AdSense 过审概率。

---

## 5. 双语实现方案

### 5.1 路由与配置

```js
// astro.config.mjs 关键片段
site: 'https://usgame.net',
trailingSlash: 'always',
i18n: {
  defaultLocale: 'en',
  locales: ['en', 'zh'],
  routing: { prefixDefaultLocale: true, redirectToDefaultLocale: false },
},
integrations: [sitemap({
  i18n: { defaultLocale: 'en', locales: { en: 'en', zh: 'zh-Hans' } },
  filter: (p) => !p.includes('404') && !p.endsWith('/search/'),
})],
```

- 每个页面存在两份：`/en/…` 与 `/zh/…`。
- `<head>` 里输出三行备用链接，互相指认：
  `hreflang="en"` → 英文版 · `hreflang="zh-Hans"` → 中文版 · `hreflang="x-default"` → 英文版。
- `canonical` 指向**本语言自己**（不要互相 canonical，否则另一半会被去索引）。

### 5.2 语言判定的三层规则（严格对应需求 7）

| 入口 | 行为 |
|---|---|
| 从搜索引擎进入 `/en/xxx` | 显示英文。**不做任何 JS 重定向** |
| 从搜索引擎进入 `/zh/xxx` | 显示中文。**不做任何 JS 重定向** |
| 进入根 `/` | 一个真正的双语网关页（不是空重定向）：两个大入口 + 站点简介 + `x-default` 指向 `/en/`。页面上有一行脚本，把浏览器语言对应的那个入口高亮，**但不自动跳转**（自动跳转会伤 AdSense 与首屏体验，也让"用户选择的语言"这条需求变得不可控） |

### 5.3 站内语言切换（关键实现）

- 切换按钮是**真 `<a href>`**，不是 `onclick=location=`。这样：JS 挂了也能用、爬虫能跟、右键新窗口能开。
- 目标 URL 由 **route key 反查**得到，不靠字符串替换：

```ts
// src/i18n/routes.ts —— 单一真相
export const routes = {
  home:          { en: '/en/',                zh: '/zh/' },
  newsList:      { en: '/en/news/',           zh: '/zh/news/' },
  newsDetail:    { en: '/en/news/{slug}/',    zh: '/zh/news/{slug}/' },
  guidesHub:     { en: '/en/guides/',         zh: '/zh/guides/' },
  // …每个详情页把 slug 也映射（中英 slug 不同：/gta-6-release-date/ vs /gta6-fashou-shijian/）
} as const;
```

  实现方式：构建时把当前页的 route key + 参数（slug、分类）作为 `data-route` / `data-params` 写在切换链接上，点击时由 `i18n/routes.ts` 同一份映射解析目标。**在中英文都存在的页面上永远不会跳到首页**。
- 点击后写入 `localStorage['usgame.lang']`；根 `/` 的网关页读它做高亮。
- 详情页 slug 本地化：英文站用英文 slug，中文站用拼音或中文 slug。映射表在内容 frontmatter 的 `slugByLocale` 字段里，构建期校验两边都存在。

### 5.4 内容侧规则

- Content Collections 按语言分目录（`content/news/en/`、`content/news/zh/`）。
- `getStaticPaths()` 只为本语言存在的条目生成页面 —— **缺翻译就 404，绝不用另一种语言顶替**。同一页面出现两种语言是明确的低质信号，也是 AdSense 会挑的毛病。
- 构建门禁 `check-i18n.mjs`：逐集合比对两侧条目数，输出缺失清单。允许暂时缺，但数字必须显式打印出来。

---

## 6. SEO 策略

### 6.1 关键词→页面映射（先做，其它都读它）

- 落成文件 `docs/keyword-map.md`，由 `src/data/keywords.ts` 同步，`check-seo.mjs` 读它做校验。
- 每个页面**一个短词 + 一个长尾**，并记录**落在哪个字段**（title / description / h1 / 某个 FAQ 问题 / 结构化数据字段）。只写"这个页面做 gta 6 map"是无法验证的。
- 长尾直接写成**用户真实问法**，放进 FAQ —— 这是 AI 引擎最容易引用的形状，也是长尾词最自然的落点。
- **一页一词**：两个页面抢同一个词会互相稀释，这是内容站最常见的自伤。

### 6.2 Meta 层

- `title`：EN 15–60 字符 / ZH 15–30 个汉字。`description`：EN 70–158 字符 / ZH 50–80 个汉字。门禁脚本卡这个范围，不靠猜。
- 真实搜索词优先于"更工整的词"。用户搜的是 `gta 6 release date`，就不要为了统一风格改成 `Release window analysis`。
- 中英各自一套关键词，不是一套词的翻译。

### 6.3 结构化数据（JSON-LD）

| 范围 | 类型 |
|---|---|
| 全站 | `WebSite`（含 `SearchAction`）+ `Organization` |
| 所有非首页 | `BreadcrumbList` |
| 新闻 / 博客 | `NewsArticle` / `Article`（含 `author`、`datePublished`、`dateModified`、`publisher`） |
| FAQ 页与含 FAQ 的攻略 | `FAQPage` |
| 视频页 / 预告片 | `VideoObject`（含 `thumbnailUrl`、`uploadDate`、`duration`、`embedUrl`） |
| 列表页（新闻、攻略、载具…） | `ItemList` |
| 步骤型攻略 | `HowTo` |
| 术语表 | `DefinedTermSet` |
| 载具 / 武器 | `Product` 不合适（不售卖）→ 用 `Article` + 表格，或自定义 `Dataset` |

**硬规则**：结构化数据里的每一条都必须能在页面上看到。生成器与内容同源（同一份 frontmatter），不允许手写 JSON-LD 字面量。

### 6.4 爬取基础设施

- `sitemap.xml`：`@astrojs/sitemap` + i18n，自动带 `xhtml:link` 备用链接；`lastmod` 取 frontmatter 的 `updated` 字段；过滤 `404` 与 `/search/`。
- `robots.txt`：放行全站，声明 sitemap 绝对地址，屏蔽带参数的搜索页 `Disallow: /*?q=`。
- 每页输出 OG（`og:type` / `og:locale` / `og:locale:alternate` / `og:image` 1200×630）与 Twitter Card（`summary_large_image`）。
- **正文不依赖 JS**：Astro 静态输出天然满足。所有筛选/搜索的**默认态**必须是完整内容（JS 只是增强），并且筛选结果要有对应的静态分类页可被爬。

### 6.5 内链

- 每篇内容页固定 4–6 条相关推荐：同分类 2 条 + 同标签 2 条 + 上位分类页 1 条 + FAQ 1 条。避免孤岛页。
- 每篇攻略顶部有目录（TOC，锚点跳转），底部有"上一篇 / 下一篇"。
- 面包屑在页面可见 + `BreadcrumbList` 结构化，两者同源。

---

## 7. GEO 策略（面向 AI 引擎）

| 手段 | 做法 |
|---|---|
| `llms.txt` | 站点根目录，纯文本：一句话定位、页面清单（URL + 一句说明）、面向谁、联系方式。**中英双语**。零成本、杠杆最高 |
| 答案优先 | FAQ 每条 3–5 句，含数字或具体事实（"11 月 19 日"、"93M 播放"），用搜索者的原话提问 |
| 实体一致性 | 站名、域名、作者名在 canonical / hreflang / sitemap / 页脚 / 每个 JSON-LD 节点里**完全一致**。AI 引擎靠重复消歧，域名改一次就要全部一起改 |
| 可引用表格 | 载具数值、武器数值、收集品清单做成 `<table>`（带 `caption` 和 `scope`）——比散文更容易被引用 |
| 定义型内容 | 术语表页给每个词一条独立定义 + `DefinedTerm`，这是 AI 引擎最稳的引用源 |
| 来源标注 | 每条官方消息带 `来源 + 日期`（页面上可见），这是"值得引用"的信号 |

> **诚实说明**：站外 GEO（维基百科条目、知乎 / Quora / Reddit 讨论、地图商家信息）是**你的工作**，代码这边只能保证站内内容可被引用。这部分我不会假装覆盖。

---

## 8. 核心功能实现路径（逐条对应需求 9）

| # | 功能 | 实现方式 | 备注 |
|---|---|---|---|
| 1 | 语言切换 | 真链接 + `routes.ts` 映射；JS 只记偏好 | 见 5.3 |
| 2 | 站内搜索 | 构建期生成 `search-index.json`（title / 摘要 / 标签 / URL / 语言）；前端 fetch + 加权打分：标题 ×3、标签 ×2、摘要 ×1；命中高亮 | 索引 < 500KB；**中文用 bigram（双字）切分 + 停用词表**，不要逐字拆——你上次在 lilink 上指出过逐字分词会把问句拆成单字、召回噪声句子 |
| 3 | 分类 / 标签筛选 | 数据驱动 + URL query（`?cat=guides`）。筛选态可分享、可后退 | 无 JS 时回退为静态分类页链接 |
| 4 | 暗 / 亮主题 | CSS 变量 + `html[data-theme]` + `localStorage` + `prefers-color-scheme`；默认暗（贴合游戏） | 内联脚本在 `<head>` 顶部设置，防首屏闪白 |
| 5 | 返回顶部 / 平滑滚动 / 汉堡菜单 | 原生 JS，尊重 `prefers-reduced-motion` | 汉堡菜单带 `aria-expanded`、Esc 关闭、焦点锁定 |
| 6 | 图片懒加载 / 预加载 | `loading="lazy"` + `decoding="async"`；hero 图 `fetchpriority="high"` + `<link rel="preload">` | AVIF 优先，WebP 兜底，`srcset` 三档 |
| 7 | 广告位 | `<AdSlot />` 组件 + 策略化投放 | 见第 9 节 |
| 8 | 地图 | **自绘 SVG**：区域路径 + 热区数据 JSON → 点击/悬停显示侧栏详情（含该区域的收集品数、任务数、载具） | 不用地图 API：免费额度、CORS、条款都不可控。SVG 反而更像游戏内地图 |
| 9 | 收集品清单 | 数据表 + 按类别/区域筛选 + 进度打勾（`localStorage` 保存） | 打勾是纯前端，不涉及后端 |
| 10 | 载具 / 武器数值 | 可排序、可筛选的表格；同屏对比 2–3 项 | 这是"数据党"的回访理由 |
| 11 | 视频 | `youtube-nocookie` + **点击式门控**（先显示缩略图，点击才注入 iframe） | 首屏不加载 iframe：性能 + Cookie 合规双赢 |
| 12 | 订阅 / 关注 | 纯前端，按你的要求不接真实邮件服务；提交后显示"前端演示"明确提示 | 不假装能用（不误导是 AdSense 红线） |
| 13 | 版本更新日志 | 内容集合 + 时间线组件 + `dateModified` 同步 | 也是"网站还在更新"的活证据 |

---

## 9. 广告位 —— 已按要求移除

> **2026-09-26 变更**：站主决定**移除全部预留广告位**。以下是当前状态，不是建议。

**已执行：**
- A 方案首页中的 4 个广告容器、`Advertisement / 广告` 标签、对应 CSS（`.ad*` 6 条规则）与
  AdSense 加载脚本**已全部删除**（实测：`adsbygoogle` 0 处、`class="ad` 0 处、正文无 "Advertisement"）。
- 内容页模板从设计之初就不含任何广告容器。
- 因此 `ads.txt`、CMP 同意弹窗、广告位预留高度（CLS 防护）**当前都不需要**，不进入构建。

**由此产生的一个后果（只说一次，决定权在你）：**
没有广告位 = 站点目前没有变现路径。原需求 2 的 AdSense 目标暂时搁置。
代码侧不做任何"暗桩"，等你哪天要开广告，再说要加在哪几个位置 —— 届时就是加组件，不是改架构。

**仍然保留、且与广告无关的合规项：**
- 隐私政策、免责声明、联系方式三页照做（AdSense 需要它们，搜索引擎与用户同样需要）。
- 若将来接入任何统计或第三方脚本，隐私政策里的 Cookie 段再补齐。

**内容质量红线（与广告无关，是内容站本身的门槛）：**
你现有 73 篇中文稿必须经过：**去 AI 味处理 → 事实核对（发售日、价格、平台必须与官方口径一致）
→ 人工过英文语感**。低质、批量感强的内容既过不了审核，也留不住读者。

---

## 10. 性能与体积预算

| 项 | 预算 | 现状 / 手段 |
|---|---|---|
| 首屏 HTML（gzip） | < 60KB | Astro 静态输出 + `inlineStylesheets: 'auto'` |
| 首屏 JS（gzip） | < 30KB | 原生 JS，无框架；只有语言/主题/筛选/搜索 |
| CSS（gzip） | < 40KB | Tailwind 产物自动裁剪 |
| 字体 | < 240KB | 自托管 + 子集化（含中文子集，只收常用字） |
| 单页最大图片 | < 350KB | AVIF + srcset |
| 全站图片 | < 25MB | 现有 96 张原图共 88MB → 构建期压缩 |
| **站点总体积** | **< 300MB** | 上限 1GB，留 3 倍余量 |
| Lighthouse 移动端性能 | ≥ 90 | 广告容器预留高度、iframe 门控、图片懒加载 |
| CLS | < 0.1 | 所有图片/广告/iframe 容器写死宽高比 |

---

## 11. 工作安排

| 阶段 | 内容 | 产出 | 需要你做什么 |
|---|---|---|---|
| 0 ✅ | 需求解析 + 资产盘点 | 资产清单（96 张图 / 80 篇稿 / 2 支预告片） | — |
| **1 ▶ 本轮** | 架构规划 + 5 个首页设计方案 | 本文档 + `design/` 5 个 HTML | **选方案 + 回答第 12 节的 5 个问题** |
| 2 | 设计系统落地：tokens、字体自托管、组件库、布局骨架；首页实现；语言切换 / 主题 / 搜索 / 筛选 四件套 | 可跑通的首页 + 交互演示 | 看效果、提修改 |
| 3 | 全部页面模板 + 路由 + 双语骨架 + 占位内容（≥ 27 类模板） | 约 160 个静态页面 | — |
| 4 | SEO / GEO 层：sitemap、robots、llms.txt、JSON-LD、hreflang、关键词映射 + 门禁脚本 | 通过 `check-seo` / `check-i18n` 的构建 | 审关键词表 |
| 5 | 内容导入流水线（`.doc` × 中英双语 → MDX）+ 首批真实内容 | 首批 20 篇中英成对入库 | **按 `docs/content-ingest-spec.md` 把稿子给我** |
| 6 | ~~广告位接入~~ → 已取消；改为**合规三页**（隐私政策 / 免责声明 / 联系方式）定稿 | 合规就绪 | 审三页文案 |
| 7 | 本地验收：真机 + 各断点 + Lighthouse + 死链 | 一条本地链接，**由你亲自实测** | 实测、报 bug |
| 8 | 部署 GitHub Pages | 线上站点 | 我给点击级手把手（走 GitHub Desktop 图形界面） |

---

## 12. 需要你拍板的 5 件事

### 12.1 站名 / 品牌
域名是 `usgame.net`，但站名不必等于域名。影响：所有页面 wordmark、所有 JSON-LD 的 `Organization.name`、OG 图、页脚。

| 选项 | 站名 | 气质 |
|---|---|---|
| **A（推荐）** | `USGAME` + `GTA VI` 角标 | 干净、可扩展到其它游戏；域名与品牌一致，对 SEO 实体一致性最有利 |
| B | `Leonida Post` | 有新闻机构的可信感，AdSense 审核友好；但与其他游戏无关 |
| C | `Vice Wire` | 短、有记忆点、偏新闻通讯社 |
| D | `GTA6 情报站 / GTA6 Intel` | 中文侧辨识度最高，但把品牌锁死在单一游戏上 |

> 提示：如果你打算让 usgame.net 以后承接**多款游戏**，A 是唯一不会后悔的选项。

### 12.2 首页方案
从 `design/` 的 5 个方案里选一个，或指定混搭（例如"E 的骨架 + A 的配色"）。我会给横向对比表 + 明确推荐。

### 12.3 `x-default` 指向哪种语言
- 推荐 **英文**（`x-default` → `/en/`）：AdSense 的英文流量单价与体量都更好，且你的目标关键词（`gta 6 release date` 等）英文搜索量级远大于中文。
- 中文站仍然完整存在、可被百度/必应/谷歌中文检索到，只是默认兜底给英文。

### 12.4 英文版内容 ✅ 已解决
**你已有 80 篇中文原文 + 80 篇英文版，后续提供。** 那么英文站不需要机翻环节，我需要做的是：

1. **导入流水线**：`.doc` → 结构化 MDX（frontmatter + 正文 + 图片位），中英两份各自入库。
2. **双语配对**：每篇稿子建立 `translationKey`（同一篇文章的中英两版共用），
   详情页由此生成 `hreflang` 与语言切换目标 —— 这是"切换不跳首页"的前提。
3. **交付格式约定**见 `docs/content-ingest-spec.md`（我需要你按什么方式给我，最省你的事）。

**唯一风险转移**：不再是我翻得对不对，而是两版内容是否**严格成对**。
构建门禁 `check-i18n.mjs` 因此升级为**硬失败**：任何只有一个语言版本的条目直接让构建红掉，
而不再是仅打印缺失清单 —— 因为现在没有"暂时缺翻译"的合理情形了。

### 12.5 首发内容量
- **建议**：首批上线 **20 篇中英双语成稿**（覆盖 6 个内容簇）再提交 AdSense 审核，而不是先交一个"框架站"。
- 原因：申请时站点必须是"已建成且有实质内容"。纯占位站几乎必被拒，且被拒一次会增加后续重审的难度。

---

## 13. 明确不在本阶段做的事

- 不填充具体新闻与攻略正文（按你的要求，本阶段只搭框架 + 占位示例）。
- 不做后台、不做数据库、不接真实邮件服务。
- 不做站外 GEO（维基 / 知乎 / Reddit 等外链建设）——那是你的工作。
- 不实现真实地图 API（用自绘 SVG 替代）。

---

## 附：设计资产现状

| 资产 | 位置 | 数量 / 规格 |
|---|---|---|
| 游戏截图与官方素材 | `GTA6游戏图片/` | 96 张，共约 88MB（含 3840×2160 官方宣传图） |
| 已优化草图资产 | `usgame.net/design/assets/img/` | 22 张 WebP，共 1.77MB |
| 中文成稿 | `GTA6游戏图文内容/` | 80 篇 `.doc` |
| 官方预告片 | `GTA6首页嵌入视频链接.txt` | Trailer 1 `QdBZY2fkU-0`(2023-12-04) · Trailer 2 `VQRLujxTm3c`(2025-05-06) |
| AdSense | `Adsense代码.txt` | `ca-pub-9680789453651246` |
