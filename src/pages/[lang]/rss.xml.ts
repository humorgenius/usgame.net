// RSS 订阅源：/{lang}/rss.xml
//
// 为什么手写而不引 @astrojs/rss：只用一个 channel + 73 个 item，
// 引入依赖换不来什么，反而多一份要跟着升级的东西。输出完全可控。
// 中英各一个 feed —— 语言混在一条 feed 里，读者会收到一半看不懂的条目。
import type { APIRoute } from "astro";
import { getCollection } from "astro:content";
import { articlePath, SITE, type Lang } from "../../i18n";

export async function getStaticPaths() {
  return [{ params: { lang: "en" } }, { params: { lang: "zh" } }];
}

const esc = (s: string) =>
  s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
   .replace(/"/g, "&quot;").replace(/'/g, "&apos;");

export const GET: APIRoute = async ({ params }) => {
  const lang = (params.lang === "en" ? "en" : "zh") as Lang;

  const posts = (await getCollection("articles", ({ data }) => !data.draft && data.lang === lang))
    .sort((a, b) => a.data.order - b.data.order);

  const title = lang === "zh" ? `${SITE.name} · GTA6 新闻与攻略` : `${SITE.name} · GTA6 news and guides`;
  const desc = lang === "zh"
    ? "GTA6 的新闻、攻略与资料。每发一篇新文章，这个订阅源就多一条。"
    : "GTA6 news, guides and reference. Every new article shows up here.";
  const self = `${SITE.origin}/${lang}/rss.xml`;

  const items = posts.map((p) => {
    const url = SITE.origin + articlePath(lang, p.data.section, p.data.slug);
    const when = (p.data.updated ?? p.data.date) as Date;
    return `    <item>
      <title>${esc(p.data.title)}</title>
      <link>${url}</link>
      <guid isPermaLink="true">${url}</guid>
      <description>${esc(p.data.description || p.data.dek || "")}</description>
      <pubDate>${when.toUTCString()}</pubDate>
    </item>`;
  }).join("\n");

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>${esc(title)}</title>
    <link>${SITE.origin}/${lang}/</link>
    <description>${esc(desc)}</description>
    <language>${lang === "zh" ? "zh-CN" : "en"}</language>
    <atom:link href="${self}" rel="self" type="application/rss+xml"/>
${items}
  </channel>
</rss>
`;
  return new Response(xml, {
    headers: { "Content-Type": "application/xml; charset=utf-8" },
  });
};
