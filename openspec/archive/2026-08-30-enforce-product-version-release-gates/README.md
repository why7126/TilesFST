# enforce-product-version-release-gates

强化发布流程产品版本号门禁：release-prepare 必须对齐 Web 与小程序 PRODUCT_VERSION，release-publish 不允许用户可见版本号不一致时发布，并要求版本号变更后重跑 image-prepare/image-build。
