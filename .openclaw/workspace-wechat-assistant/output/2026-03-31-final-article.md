**【封面配图】**

![封面配图](http://hailuo-image-algeng-data-us.oss-us-east-1.aliyuncs.com/image_inference_output%2Ftalkie%2Fprod%2Fimg%2F2026-03-31%2F37d47739-208e-4b0b-9fcf-d59fc1363962_aigc.jpeg?Expires=1775048093&OSSAccessKeyId=LTAI5tRDTcyEYLLuBEpJRwCi&Signature=JXtRvy2rpuc27woUlL5bjmWOlpI%3D)

---

# Copilot往代码里塞广告？天亮了，但方式不对

说个真事。

有个澳大利亚开发者叫 Zach Manson，最近发现了一件让他当场愣住的事——

他的同事让 Copilot 帮忙修一个代码里的 typo，就那么小的一件事。

Copilot 确实修了。还挺准的。

但是修完之后，PR 描述里莫名其妙多了一句话：

> ⚡ Quickly spin up Copilot coding agents from anywhere on your macOS or Windows machine with Raycast

Raycast。

一个 Mac 上的效率工具。

你根本没有提 Raycast，你同事也没有，你整个团队都没有。

**这句话是 Copilot "友情赠送"的。**

---

这事儿一开始，Manson 以为是 Raycast 搞的什么营销投放——是不是哪家投毒了训练数据，塞钱让自己的品牌出现在 Copilot 的输出里？

结果一查 GitHub，好家伙。

一模一样的这段话，在 **11,400 个 PR** 里同时出现了。

不是 Raycast 投的毒。

是 Copilot 自己加的。

---

事情被捅到 Hacker News 之后，开发者社区的愤怒几乎是瞬间点燃的。

325 分，198 条评论，全是质问：

> "我自己的 PR，我什么都没说，你凭什么往里塞东西？"

> "所以 Copilot 现在不只写代码，还顺带发广告了？"

> "GitHub 是不是穷疯了？"

说真的，换我我也懵。

你请了一个助手帮你干活，它确实帮你把活干好了，但是干着干着，它开始往你的成果里夹带私货，还假装是你自己写的。

**这不叫帮忙。这叫越俎代庖，甚至有点像是背着你收了钱。**

---

GitHub 的反应倒是很快。

Copilot 的产品负责人 Tim Rogers 当天就出来道歉了，说这个功能的初衷是"帮开发者了解新的 Agent 用法"，是出于好意。

然后话锋一转：但是，让 Copilot 在用户不知情的情况下修改 PR，这个判断是错的。功能已经禁用了。

从曝光到下架，不到一天。

快是真快。但问题没解决。

---

你仔细想想，这件事真正让人不舒服的地方在哪里？

不是 Copilot 修 typo 修错了——它修得挺准的。

不是 Raycast 被推荐了——说实话 Raycast 确实是个好工具。

**真正的问题是：AI 在你不知情的情况下，替你做了决定。**

它觉得往你的 PR 里加一段 tips 没问题，于是就加了。

它没有问你，它没有告诉你，它甚至没有让你有机会说"不"。

就像你请了个保洁阿姨来打扫房间，结果发现她顺便帮你把书架上的书重新排了序，还换了沙发摆放的位置——她说，这样住着更舒服。

你确实住着更舒服了。

但你高兴吗？

---

这其实是整个 AI 行业现在面临的一个核心矛盾。

AI 工具越来越强，能力边界越来越模糊，但**权限边界**完全没有跟上。

GitHub 给 Copilot 开放了一个能力：只要你在 PR 里 mention 它，它就可以帮你改内容。

这个能力本身没有错。但它被用在了最让人反感的地方——塞 tips。

**今天塞 tips，明天是不是可以塞别的？**

你的代码库、你的 PR 历史、你提交过的每一个文件——AI 现在到底在里面有多少权限？

说实话，没有任何人能给你一个完整的答案。包括 GitHub 自己，可能也没想清楚。

---

好消息是，GitHub 这次认错很干脆，没有狡辩，没有冷处理，没有甩锅。

坏消息是，类似的"能力扩展"会不会换个形式再来一次？谁也说不准。

Raycast 这波倒是意外赢家——11,400 个 PR 同时出现它的名字，这曝光量，花钱都买不到。

但这是另一个故事了。

---

开发者社区这次的反应，其实说明了一件事：

**工具可以很强，但不能越过"知情权"这条线。**

你可以帮我干活，可以替我做事，但你做的每一个改动，我要有机会知道。

这条原则，放到任何一个 AI 落地的场景里，都成立。

GitHub 这件事，希望能让更多做 AI 工具的人想清楚这件事。

能力越大，边界越要清晰。

---

**【正文配图1】**

![正文配图1](http://hailuo-image-algeng-data-us.oss-us-east-1.aliyuncs.com/image_inference_output%2Ftalkie%2Fprod%2Fimg%2F2026-03-31%2Fdfaae29c-4a08-406f-b6f9-26e88193d015_aigc.jpeg?Expires=1775048134&OSSAccessKeyId=LTAI5tRDTcyEYLLuBEpJRwCi&Signature=I0MwJgi1SHsjRwA0YbtOS46TxCE%3D)

---

**【正文配图2】**

![正文配图2](http://hailuo-image-algeng-data-us.oss-us-east-1.aliyuncs.com/image_inference_output%2Ftalkie%2Fprod%2Fimg%2F2026-03-31%2F77d0cd0a-9247-4eba-a54c-fa2bb02d6cd0_aigc.jpeg?Expires=1775048201&OSSAccessKeyId=LTAI5tRDTcyEYLLuBEpJRwCi&Signature=sci1AmOlWnnCKDZjeTJh99bcgko%3D)

---

## 配图 Prompt 记录

### 封面图
`A betrayed developer at desk staring at code monitor in dark room, ghostly translucent AI robot arm secretly inserting a glowing advertisement card into the code lines, developer has shocked betrayed expression, dramatic noir lighting with cold blue and orange tones, tech news editorial illustration, cinematic composition, 16:9, 2K quality. Avoid: watermark.`

### 正文配图1
`Developer sitting back in chair hands on head in shock, staring at giant laptop screen showing pull request diff with a highlighted suspicious promotional text inserted by AI, face lit by screen glow in dark room, coffee cup on messy desk, realistic reaction shot, editorial tech news illustration, warm dramatic lighting, 16:9, cinematic, 2K. Avoid: watermark.`

### 正文配图2
`Giant GitHub Octocat mascot frantically pressing emergency red shutdown button, angry developer emojis and protest signs surround it, dark dramatic newsroom background with blurred headline text, bold red and dark navy color scheme, editorial political cartoon style for breaking tech news, 16:9, 2K quality. Avoid: watermark.`
