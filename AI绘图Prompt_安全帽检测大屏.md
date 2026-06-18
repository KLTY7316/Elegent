# 安全帽智能检测大屏 UI - 完整 AI 绘图 Prompt

## 一、完整 Prompt（中英双语，直接复制使用）

```
A professional construction site safety helmet AI detection monitoring dashboard UI design, 
deep space cosmic background with Earth nebula and starry sky particles, 
dark blue gradient backdrop #0a0e27 to #0f1535, 
blue-tinted frosted glass Glassmorphism UI cards with backdrop-filter blur 20px, 
low-saturation deep sea blue gradient cards rgba(20,45,80,0.35), 
suspended layered large rounded-rectangle cards, 
subtle inner glow thin blue border 1px solid rgba(54,144,255,0.3), 
dark mode B-end industrial monitoring dashboard, 
left fixed vertical sidebar navigation, 
cold tone deep blue gradient overall theme, 
semi-transparent panels, soft shadow floating layers, 
sans-serif thin font, neon light blue highlights #60b8ff, 
business industrial style, low brightness atmosphere, 
backend management monitoring system, 
construction site safety helmet AI detection backend, 
fullscreen web management interface, 
soft diffused shadow, card blurred frosted glass background.

Layout structure:
- Left side: Fixed vertical sidebar navigation menu with icons and labels (Dashboard, Real-time Monitor, Alerts, Statistics, Camera Management, Settings, Logout), dark translucent background, glassmorphism effect, active item highlighted with blue gradient
- Top header: Global breadcrumb navigation + title "工地安全帽智能识别监测系统" + date picker + admin avatar + notification bell + search icon, semi-transparent dark background
- Main area left large card: Real-time AI video surveillance feed showing construction site scene, YOLO object detection overlay with green bounding boxes around workers wearing safety helmets, red bounding boxes around heads without helmets, each box showing confidence score percentage, live video stream preview
- Right side stacked three glass cards:
  * Upper card [Today's Statistics Panel]: Total people detected today, total violations (no helmet), normal wearing count, violation ratio horizontal gradient progress bar, high-risk location stats, circular gauge charts, numbers in large white font with blue neon glow
  * Middle card [Safety Helmet Violation Alerts]: Table format showing alert data (violation time, camera ID, thumbnail snapshot, violation type: no helmet, processing status), new alert notification badge, "View All Records" button, red status tags
  * Lower card [Monthly Violation Trend Activity Chart]: Line-bar mixed Echarts chart, X-axis 1-12 months, Y-axis monthly violation count, blue gradient filled line chart, "Export Report" button, data visualization with glowing blue lines

Color system:
- Primary: deep space blue #0b203d, gradient highlight blue #3690ff
- Card background: semi-transparent deep blue frosted glass rgba(20,45,80,0.35)
- Text: light gray-white #e6edf7, highlight text ice blue #60b8ff
- Violation red #ff4d4f, compliant green #36d399
- Divider: extremely light semi-transparent blue
- Button: blue gradient glowing hover effect
- Overall background: starry sky deep blue gradient base

Global functional buttons: Add New Alert, Filter buttons (Today/This Week/This Month/High Priority), camera device online status mini module, three-dot more options button on card top-right corner.

Technical architecture diagram at bottom: Edge computing device (camera/industrial PC) → Inference Engine → Cloud Platform, YOLO/SSD object detection model flow, connected by glowing blue arrow lines.

Ultra-detailed, 8K, UI/UX design, Figma-style, web dashboard, professional monitoring system interface, cinematic lighting, volumetric fog, tech-noir atmosphere.
```

---

## 二、中文 Prompt 版本

```
专业工地安全帽AI检测监控大屏UI设计，深空宇宙星空+地球星云背景，
暗蓝色渐变底色 #0a0e27 到 #0f1535，
蓝调磨砂玻璃Glassmorphism UI卡片，backdrop-filter模糊20px，
低饱和深海蓝渐变卡片 rgba(20,45,80,0.35)，
悬浮分层大圆角矩形卡片，微弱内发光细蓝边 1px solid rgba(54,144,255,0.3)，
暗黑B端工业监控Dashboard，左侧固定垂直导航侧边栏，
整体冷调深蓝渐变，半透明面板，柔和阴影悬浮层级，
无衬线纤细字体，霓虹浅蓝高光 #60b8ff，商务工业风，
低亮度氛围感，后端管理监控系统，工地安全帽AI检测后台，
全屏web管理界面，柔和弥散阴影，卡片虚化毛玻璃背景。

布局结构：
- 左侧：固定垂直侧边导航菜单，带图标和文字（Dashboard首页、实时监控、告警记录、统计报表、摄像头设备管理、系统设置、退出登录），深色半透明背景，玻璃态效果，选中项蓝色渐变高亮
- 顶部栏：全局面包屑导航 + 标题"工地安全帽智能识别监测系统" + 日期选择框 + 管理员头像 + 消息通知铃铛 + 搜索图标，半透明深色背景
- 左侧超大主卡片：实时AI视频监控画面，显示工地场景，YOLO目标检测叠加层，绿色包围框标注佩戴安全帽工人，红色包围框标注未佩戴安全帽人头，每个框显示置信度分数百分比，视频流实时预览
- 右侧三层堆叠玻璃卡片：
  * 上层【今日数据统计面板】：今日在岗检测总人数、未佩戴安全帽违规总数、正常佩戴人数、违规占比横向渐变进度条、今日高危点位统计，圆形仪表盘，大号白色数字带蓝色霓虹光
  * 中层【安全帽违规告警记录】：表格形式展示告警数据（违规发生时间、监控摄像头编号、抓拍截图缩略图、违规类型：未佩戴安全帽、处理状态），新增告警提醒红色标签、查看全部记录按钮、红色状态标签
  * 下层【月度违规趋势Activity图表】：折线柱状混合图表，横轴1-12月份，纵轴月度违规次数，蓝色渐变填充折线、导出报表按钮，发光蓝色线条数据可视化

色彩体系：
- 主色：深空深蓝 #0b203d、渐变高亮蓝 #3690ff
- 卡片底色：半透深蓝毛玻璃 rgba(20,45,80,0.35)
- 文字：浅灰白 #e6edf7、高亮文字冰蓝 #60b8ff
- 违规红色 #ff4d4f、合规绿色 #36d399
- 分割线：极浅半透蓝色
- 按钮：蓝渐变发光hover效果
- 整体背景：星空深蓝渐变底色

全局功能按钮：新增告警、筛选按钮（今日/本周/本月/高优先级违规）、摄像头设备在线状态小模块、卡片右上角三点更多操作按钮。

底部技术架构图：边缘计算设备（摄像头/工控机）→ 推理引擎 → 云端平台，YOLO/SSD目标检测模型流程，发光蓝色箭头连线。

超精细、8K、UI/UX设计、Figma风格、web仪表盘、专业监控系统界面、电影级光照、体积雾、科技暗黑氛围。
```

---

## 三、关键视觉元素清单

| 元素 | 描述 | 颜色/样式 |
|------|------|----------|
| 背景 | 深空宇宙+地球星云+星空粒子 | #0a0e27 → #0f1535 渐变 |
| 侧边栏 | 固定垂直导航，玻璃态 | rgba(15,30,60,0.6) + blur |
| 顶部栏 | 标题+日期+头像+通知+搜索 | 半透明深色 |
| 主视频卡片 | 实时YOLO检测画面 | 绿色框(合规) / 红色框(违规) |
| 统计卡片 | 今日数据仪表盘 | 大号数字 + 进度条 |
| 告警卡片 | 告警记录表格 | 红色标签 + 缩略图 |
| 趋势卡片 | 月度违规折线图 | 蓝色渐变填充 |
| 架构图 | 边缘→推理→云端 | 发光蓝色箭头 |
| 按钮 | 全局功能按钮 | 蓝渐变发光hover |

---

## 四、使用建议

1. **Midjourney**: 使用上述英文 Prompt，添加 `--ar 16:9 --v 6 --style raw`
2. **DALL-E 3**: 使用英文 Prompt，强调 "UI design mockup, no text distortion"
3. **Stable Diffusion**: 使用中文或英文 Prompt + ControlNet (dashboard layout)
4. **即梦/可灵/通义万相**: 使用中文 Prompt，选择 "UI设计" 或 "网页设计" 风格
