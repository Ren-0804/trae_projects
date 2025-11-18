
# 司机与车辆管理平台（前端）README

## 项目概述
- 核心功能与目标
  - 提供司机、车辆、排班、证书、安全监控等业务模块的前端管理界面
  - 支持数据统计与趋势图展示（司机总数、活跃率、热门线路、员工司机分布等）
  - 通过可视化图表与数据表，帮助运营人员快速掌握业务状况
  - 连接后端 REST API，完成增删改查与业务操作（分配司机、维护提醒、证书续期等）
- 适用用户与场景
  - 物流企业运营人员：司机资料维护、车辆管理、排班安排、证书管理
  - 风控与安全监控人员：GPS轨迹、驾驶行为、紧急警报
  - 管理员：用户管理、权限控制、数据统计与审查
- 技术栈与主要依赖
  - 前端框架：Vue 3（`^3.5.22`）、Vite（`^7.1.11`）
  - UI 组件：Ant Design Vue（`^4.2.6`）
  - 状态管理：Pinia（`^3.0.3`）
  - 路由：Vue Router（`^4.6.3`）
  - 工具库：@vueuse/core、axios、dayjs
  - 图表：ECharts（`^5.4.3`） + `vue-echarts`（`^6.6.1`）
  - 开发工具与质量保障：TypeScript（`~5.9.0`）、ESLint（`^9.37.0`）、Prettier（`3.6.2`）

---

## 部署指南
- 环境要求
  - Node.js：`^20.19.0` 或 `>=22.12.0`（见 `package.json engines`）
  - 包管理器：npm（项目内提供 npm scripts）
  - 浏览器：现代浏览器（Chrome/Edge/Firefox 最新版）
- 本地开发环境搭建
  1. 安装 Node.js（建议 20 LTS 或 22.x）
  2. 拉取代码：`git clone <repo-url>`
  3. 安装依赖：`npm install`
  4. 配置环境变量（见下文）
  5. 启动开发：`npm run dev`，访问 `http://localhost:5173/` 或根据终端提示端口
  6. 类型检查：`npm run type-check`
  7. 代码规范与修复：`npm run lint`、`npm run format`
- 生产环境部署流程
  - 标准构建
    - 设置环境变量（特别是后端 API 地址）
    - 构建产物：`npm run build`
    - 预览构建：`npm run preview`（默认端口 4173）
    - 将 `dist/` 目录部署至静态服务器（Nginx/Apache/或云静态托管）
  - Docker 部署（示例）
    - Dockerfile（示例，基于 Nginx 提供静态资源）：
      ```dockerfile
      # 1. Build stage
      FROM node:20-alpine AS builder
      WORKDIR /app
      COPY package.json package-lock.json ./
      RUN npm ci
      COPY . .
      # 设置后端 API 地址（构建时注入）
      ARG VITE_API_BASE_URL
      ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}
      RUN npm run build

      # 2. Serve stage
      FROM nginx:alpine
      COPY --from=builder /app/dist /usr/share/nginx/html
      # 自定义 Nginx 配置（启用 SPA 回退）
      COPY nginx.conf /etc/nginx/conf.d/default.conf
      EXPOSE 80
      CMD ["nginx", "-g", "daemon off;"]
      ```
    - Nginx 配置（`nginx.conf`）：
      ```nginx
      server {
        listen 80;
        server_name _;
        root /usr/share/nginx/html;

        location / {
          try_files $uri $uri/ /index.html;
        }
      }
      ```
    - 构建镜像：
      - `docker build --build-arg VITE_API_BASE_URL="https://api.example.com/api/v1" -t driver-mgmt-frontend:latest .`
    - 运行容器：
      - `docker run -d -p 8080:80 driver-mgmt-frontend:latest`
- 环境变量说明
  - `VITE_API_BASE_URL`：后端 API 基地址（默认 `http://localhost:8000/api/v1`，见 `src/api/auth.ts:4`）
  - 说明：Vite 会在构建时将 `VITE_` 前缀变量注入到客户端代码；请于构建前正确设置

---

## 代码结构说明
- 目录结构
  - `src/api/`：后端 API 封装（统一 axios 实例，认证与重试拦截器）
  - `src/assets/`：静态资源与样式文件
  - `src/components/`：通用组件与图表组件
    - `components/charts/`：`BarChart.vue`、`LineChart.vue`、`PieChart.vue`、`index.ts`
  - `src/layouts/`：布局组件（`Layout.vue`）
  - `src/router/`：路由配置（`index.ts`）
  - `src/stores/`：Pinia 状态管理（`auth.ts`、`drivers.ts`、`statistics.ts`）
  - `src/types/`：TypeScript 类型定义（`vehicle.ts`、`safety.ts`、`schedule.ts` 等）
  - `src/utils/`：工具方法（图表数据格式化等）
  - `src/views/`：页面模块（分子目录组织）
    - `drivers/`：司机模块（`List.vue`、`Create.vue`、`Edit.vue`、`Detail.vue`）
    - `vehicles/`：车辆模块（`List.vue`、`Create.vue`、`Edit.vue`、`AssignDriver.vue`、`MaintenanceReminders.vue` 等）
    - `schedules/`：排班模块（`List.vue`、`Create.vue`、`Calendar.vue`）
    - `certificates/`：证书模块（`List.vue`、`Create.vue`、`Detail.vue`）
    - `safety/`：安全模块（`Dashboard.vue`、`Alerts.vue`、`Emergency.vue`）
    - 其他页面：`Login.vue`、`Statistics.vue`、`Profile.vue` 等
  - 根文件：`App.vue`、`main.ts`
- 核心文件用途
  - `src/api/auth.ts`：axios 实例与认证拦截器；`login`、`getCurrentUser` 方法
  - `src/router/index.ts`：路由与导航守卫（认证与管理员权限校验）
  - `src/stores/auth.ts`：用户认证状态与方法（`login`、`fetchUser`、`logout`）
  - `src/views/Statistics.vue`：统计仪表板视图，调用 `useStatisticsStore` 与图表组件展示统计数据
  - `src/utils/chartUtils.ts`：图表数据格式化与处理

---

## 功能清单
- 用户与认证
  - 登录、鉴权（Token 持久化、本地存储）
  - 权限控制（管理员可访问统计与用户管理）
- 司机管理
  - 列表、详情、新增、编辑、删除
  - 照片上传与最近照片展示
  - 主要线路选择（树形选择器，支持手动输入）
- 车辆管理
  - 列表、详情、创建、更新、删除
  - 分配司机、结束分配
  - 维护记录与到期提醒、保险到期提醒
- 排班管理
  - 列表、创建、更新、删除
  - 日历视图、冲突检测、司机可用时段查询
- 证书管理
  - 列表、创建、更新、删除
  - 即将到期提醒、续期、文件上传
  - 司机证书汇总
- 安全监控
  - GPS 轨迹记录与车辆轨迹查询
  - 驾驶行为记录（急刹/超速/急转弯），汇总与处理
  - 紧急警报列表与处理，活跃警报汇总
  - 安全统计与近期警报
- 数据统计（Statistics）
  - 数据概览、司机总数/活跃率/新增数据
  - 热门线路分布、员工司机分布
  - 增长趋势与活跃率趋势图
- 关联关系举例
  - 司机与车辆：分配关系（主/临时）
  - 司机与证书：证书类型、到期与续期关联
  - 排班与司机/车辆：任务安排与冲突检测
  - 安全与司机/车辆：行为与警报数据映射

---

## API 文档（前端已使用的后端端点）
- 认证与用户
  - `POST /auth/login`：登录
    - 请求体：`{ username: string, password: string }`
    - 响应：`{ token: string, user: { id, username, role, ... } }`
  - `GET /auth/me`：获取当前用户
  - `GET /auth`：获取用户列表（分页模拟）
  - `GET /auth/:id`、`PUT /auth/:id`、`DELETE /auth/:id`
  - `POST /auth/register`：创建用户
- 司机
  - `GET /drivers`：列表（参数：`page`, `page_size`, `keyword`, `route`, `status`）
    - 响应：`{ data: Driver[], total, page, page_size }`
  - `GET /drivers/:id`：详情
  - `POST /drivers/`：新增（字段见 `DriverCreate`）
  - `PUT /drivers/:id`：更新（字段见 `DriverUpdate`）
  - `DELETE /drivers/:id`：删除
  - `GET /drivers/:id/photos`：照片列表
  - `GET /drivers/photos/:photoId`：照片内容（Blob）
  - `POST /drivers/:id/photos`：上传照片（`multipart/form-data`）
- 车辆
  - `GET /vehicles`、`GET /vehicles/:id`、`POST /vehicles`、`PUT /vehicles/:id`、`DELETE /vehicles/:id`
  - 司机分配：`POST /vehicles/:id/assign-driver`、`PUT /vehicles/:id/assignments/:assignmentId/end`
  - 维护记录：`GET /vehicles/:id/maintenance-records`、`POST /vehicles/:id/maintenance-records`
  - 维护与保险提醒：`GET /vehicles/maintenance/upcoming`、`GET /vehicles/insurance/expiring`
  - 分配查询：`GET /vehicles/assignments`
- 排班
  - `GET /schedules`、`GET /schedules/:id`、`POST /schedules`、`PUT /schedules/:id`、`DELETE /schedules/:id`
  - 日历：`GET /schedules/calendar/:year/:month`
  - 冲突检测：`GET /schedules/conflicts/check`
  - 司机可用性：`GET /schedules/drivers/:driverId/availability`
- 证书
  - `GET /certificates`、`GET /certificates/:id`、`POST /certificates`、`PUT /certificates/:id`、`DELETE /certificates/:id`
  - 到期提醒：`GET /certificates/expiring-soon`
  - 续期：`POST /certificates/:id/renew`
  - 文件上传：`POST /certificates/:id/upload-file`（`multipart/form-data`）
  - 司机证书汇总：`GET /certificates/drivers/:driverId/summary`
- 安全监控
  - GPS：`POST /safety/gps-records`、`GET /safety/gps-records`
  - 车辆轨迹：`GET /safety/vehicles/:vehicleId/track`
  - 驾驶行为：`POST /safety/driving-behaviors`、`GET /safety/driving-behaviors`、`PUT /safety/driving-behaviors/:id`、`GET /safety/driving-behaviors/summary`
  - 警报：`POST /safety/emergency-alerts`、`GET /safety/emergency-alerts`、`PUT /safety/emergency-alerts/:id`、`GET /safety/emergency-alerts/stats`
  - 警报流：`GET /safety/alerts/recent`、`GET /safety/alerts`、`PUT /safety/alerts/:id/process`
  - 安全统计：`GET /safety/stats`、`GET /safety/emergency-alerts/active-summary`
- 地区数据
  - 中国省份：`GET /regions/china/provinces?q=...`
  - 中亚国家与城市：`GET /regions/central-asia/countries?q=...`
- 请求/响应示例
  - 司机创建请求（`POST /drivers/`）：
    ```json
    {
      "name": "张三",
      "phone": "13800000000",
      "id_card": "110101199001010011",
      "license_number": "X1234567",
      "license_type": "B2",
      "main_route": "中国-北京→中国-上海;哈萨克斯坦-阿拉木图→乌兹别克斯坦-塔什干",
      "vehicle_type": "厢式货车",
      "price_per_km": 3.5,
      "experience_years": 5,
      "status": "active",
      "emergency_contact": "李四",
      "emergency_phone": "13900000000",
      "remark": "长途经验丰富"
    }
    ```
  - 统计响应（`GET /statistics`）：
    ```json
    {
      "total_drivers": 120,
      "active_drivers": 86,
      "new_drivers_this_month": 8,
      "drivers_by_route": [
        { "route": "中国-北京", "count": 22 },
        { "route": "中国-上海", "count": 18 }
      ],
      "drivers_by_user": [
        { "user_id": 1, "username": "admin", "count": 80 },
        { "user_id": 2, "username": "ops", "count": 40 }
      ]
    }
    ```
- 错误代码与状态
  - 401 未授权：清理 Token 并跳转登录（见 `src/api/auth.ts` 拦截器）
  - 422 验证错误：控制台输出具体字段信息（见拦截器）
  - 网络错误自动重试：最多 2 次间隔退避（见拦截器）
  - 统一错误日志：URL、方法、状态码、响应内容、错误码、消息（见拦截器）

---

## 开发指南
- 代码贡献规范
  - 提交信息建议采用 Conventional Commits（如 `feat:`、`fix:`、`docs:`）
  - 新功能请在独立分支开发并创建 Pull Request
  - 保持类型完备与严格（TypeScript），避免 `any`
- 测试方法
  - 类型检查：`npm run type-check`
  - 代码质量：`npm run lint`、`npm run format`
  - 本地预览与手动测试：`npm run dev`、`npm run preview`
- 代码风格要求
  - ESLint + Prettier 统一风格（`npm run lint` / `npm run format`）
  - 组件命名与文件组织遵循现有目录风格
  - 避免在代码中输出敏感信息（Token/密钥）
- 分支管理策略
  - 推荐 GitFlow 或简化策略：
    - `main`：稳定发布分支
    - `develop`：日常开发分支
    - `feature/*`：功能分支
    - `hotfix/*`：紧急修复分支

---

## 其他信息
- 项目许可证
  - 建议使用 MIT 许可证（可根据公司政策调整）
- 联系方式
  - 运营支持、技术支持联系人请根据公司内部信息补充
- 已知问题与修复建议
  - Ant Design Vue 表单项限制：同一 `a-form-item` 仅能收集一个字段
    - 表现为：`Warning: [ant-design-vue: Form.Item] FormItem can only collect one field item...`
    - 解决方案：将额外交互控件移至 `a-form-item-rest`，保留一个隐含字段或唯一输入作为收集对象（已在 `src/views/drivers/Create.vue` 修复）
  - Vue 模板标签闭合错误
    - 表现为：`Element is missing end tag`
    - 解决方案：修正错误的 `</div>` 为 `</a-row>`（见 `src/views/Statistics.vue`）
- 未来规划
  - 引入自动化测试（Vitest + Vue Testing Library）
  - 更完善的国际化支持（中文/英文）
  - 更多图表维度与报表导出
  - 更细粒度的权限控制与审计日志

---

## 安全与隐私
- 不在日志中打印用户鉴权 Token
- 所有请求通过 axios 拦截器附带 `Authorization: Bearer <token>`
- 用户 Token 存储于 `localStorage`（可按需要改为更安全的机制）

---

## 快速命令
- 开发：`npm run dev`
- 构建：`npm run build`
- 预览：`npm run preview`
- 类型检查：`npm run type-check`
- 规范修复：`npm run lint`、`npm run format`

如需将本 README 内容保存为仓库文件，请告知我使用的目标路径与文件名（默认 `README.md`），我将为你创建并提交变更。