# automate-product-version-release-prepare

将 PRODUCT_VERSION 更新自动化纳入 release-prepare：release-prepare 在校验前自动同步 Web 与小程序 PRODUCT_VERSION 到发布版本，刷新 release metadata/公告版本状态证据，release-publish 只确认不写版本，image-prepare 前强制版本源已对齐。
