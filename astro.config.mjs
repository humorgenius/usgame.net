// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// 语言路由：/en/… 与 /zh/… 都带前缀。根路径 / 是一个跳转到 /en/ 的重定向存根
// （src/pages/index.astro），不是内容页，因此也不进 sitemap。
// 中英共用同一套 slug，所以互指链接只是换前缀 —— 不会退回首页。
export default defineConfig({
  site: 'https://usgame.net',
  trailingSlash: 'always',
  build: { format: 'directory' },
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'zh'],
    routing: { prefixDefaultLocale: true, redirectToDefaultLocale: false },
  },
  integrations: [
    sitemap({
      i18n: { defaultLocale: 'en', locales: { en: 'en', zh: 'zh-Hans' } },
      // 搜索页不进 sitemap：它是站内工具，收录了只会跟真正的内容页抢关键词。
      // 404 页同理 —— 错误页被收录，搜索结果里就会出现一条"找不到页面"。
      // 根路径 / 也不进：它是跳转到 /en/ 的重定向存根，sitemap 只该列 200 的规范页。
      filter: (page) => !page.includes('/search/') && !page.includes('404')
        && new URL(page).pathname !== '/',
    }),
  ],
  devToolbar: { enabled: false },

  // 绑定 IPv4。Astro 默认只监听 ::1（IPv6 回环），而验证器/监控/多数探针轮询的是
  // 127.0.0.1，会得到 connection refused —— 表现为「服务起来了但就绪检查一直失败」。
  // 注意：preview 没有对应的配置键（写了会 ts(2353) 报错），预览用 CLI 的 --host。
  server: { host: '127.0.0.1' },
});
