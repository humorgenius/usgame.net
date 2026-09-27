# USGAME — GTA6 新闻 · 攻略 · 情报

面向中英双语读者的 GTA6 资料站，静态生成，无后端。

- 线上域名：<https://usgame.net>（`www` 301 跳 apex）
- 技术栈：Astro + 原生 CSS/JS，全站单份 `src/styles/theme.css`；除 AdSense 与 YouTube 嵌入外不引任何第三方脚本或访问统计
- 内容：73 篇中英双语文章（`src/content/articles/{zh,en}/`），由 `scripts/ingest.py` 从原始文稿入库
- 语言路由：`/zh/…` 与 `/en/…` 各自带前缀，根路径 `/` 是不自动跳转的双语网关

## 本地开发

```bash
npm install
npm run dev        # http://127.0.0.1:4321/
```

## 自检与构建

```bash
npm run check      # Astro 类型与内容检查
npm run build      # 产出 dist/（含 sitemap）
npm run links      # 链接审计：站内链接可达、锚点存在、链接文字能对上目标页标题
```

`npm run links` 是产物级检查，必须排在 `build` 之后。它抓的是"看着能点、其实点不到文章"的假链接。

## 部署

推送到 `main` 即由 `.github/workflows/deploy.yml` 构建并发布到 GitHub Pages。
仓库 Settings → Pages → Source 需选 **GitHub Actions**。

## 许可与声明

Grand Theft Auto、GTA 与 Rockstar Games 是 Take-Two Interactive Software, Inc. 的商标。
本站为非官方爱好者站点，与 Take-Two 及 Rockstar Games 无隶属或授权关系。
