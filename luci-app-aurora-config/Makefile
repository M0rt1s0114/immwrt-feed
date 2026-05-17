include $(TOPDIR)/rules.mk

PKG_NAME:=luci-app-aurora-config
PKG_VERSION:=0.3.0
PKG_RELEASE:=1

PKG_SOURCE_PROTO:=git
PKG_SOURCE_URL:=https://github.com/eamonxg/luci-app-aurora-config.git
PKG_SOURCE_VERSION:=v$(PKG_VERSION)
PKG_MIRROR_HASH:=skip

include $(INCLUDE_DIR)/package.mk

define Package/luci-app-aurora-config
  SECTION:=luci
  CATEGORY:=LuCI
  SUBMENU:=Applications
  TITLE:=Aurora Theme Config
  DEPENDS:=+luci-theme-aurora
  PKGARCH:=all
endef

define Package/luci-app-aurora-config/install
	$(INSTALL_DIR) $(1)/etc/uci-defaults
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/root/etc/uci-defaults/* $(1)/etc/uci-defaults/ 2>/dev/null || true
	$(INSTALL_DIR) $(1)/www/luci-static/resources/view/aurora
	$(CP) $(PKG_BUILD_DIR)/htdocs/luci-static/resources/view/aurora/* $(1)/www/luci-static/resources/view/aurora/ 2>/dev/null || true
	$(INSTALL_DIR) $(1)/usr/lib/lua/luci/controller
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/root/usr/lib/lua/luci/controller/* $(1)/usr/lib/lua/luci/controller/ 2>/dev/null || true
	$(INSTALL_DIR) $(1)/usr/lib/lua/luci/model/cbi
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/root/usr/lib/lua/luci/model/cbi/* $(1)/usr/lib/lua/luci/model/cbi/ 2>/dev/null || true
endef

$(eval $(call BuildPackage,luci-app-aurora-config))