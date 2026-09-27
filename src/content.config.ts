import { defineCollection } from "astro:content";
import { z } from "astro/zod";
import { glob } from "astro/loaders";

/**
 * 73 篇稿件由 scripts/ingest.py 从 .docx 生成，中英各一份，同名不同目录。
 * 路径 src/content/articles/<lang>/<slug>.md —— 所以 id 形如 "zh/gta-6-wanted-level"，
 * lang 与 slug 都能从 id 推出来，不必在 frontmatter 里重复声明成两处真相。
 */
const articles = defineCollection({
  // generateId 必须带上目录，否则 en/foo.md 与 zh/foo.md 会算出同一个 slug
  // ——glob loader 默认只看文件名，中英同名的稿子会互相冲突（astro sync 会报警告）。
  loader: glob({
    pattern: "**/*.md",
    base: "./src/content/articles",
    generateId: ({ entry }) => entry.replace(/\.md$/, ""),
  }),
  schema: z.object({
    title: z.string(),
    description: z.string(),   // SEO，≤158 字，句末截断
    dek: z.string(),           // 页面上显示的导语，完整首段
    lang: z.enum(["zh", "en"]),
    slug: z.string(),
    section: z.string(),
    subcategory: z.string().nullable(),
    order: z.number(),         // 原稿序号：date 全部相同，排序只能靠它
    date: z.coerce.date(),
    updated: z.coerce.date(),
    cover: z.string(),
    sourceFile: z.string(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { articles };
