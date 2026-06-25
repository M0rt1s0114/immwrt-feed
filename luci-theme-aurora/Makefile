include $(TOPDIR)/rules.mk

PKG_NAME:=luci-theme-aurora
PKG_VERSION:=1.0.0
PKG_RELEASE:=1

PKG_SOURCE_PROTO:=git
PKG_SOURCE_URL:=https://github.com/eamonxg/luci-theme-aurora.git
PKG_SOURCE_VERSION:=v1.0.0
PKG_MIRROR_HASH:=skip

include $(INCLUDE_DIR)/package.mk

define Package/luci-theme-aurora
  SECTION:=luci
  CATEGORY:=LuCI
  SUBMENU:=4. Themes
  TITLE:=Aurora Theme
  DEPENDS:=+luci
  PKGARCH:=all
endef

define Package/luci-theme-aurora/install
	$(INSTALL_DIR) $(1)/etc/uci-defaults
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/root/etc/uci-defaults/* $(1)/etc/uci-defaults/ 2>/dev/null || true
	$(INSTALL_DIR) $(1)/www/luci-static/aurora
	$(CP) $(PKG_BUILD_DIR)/htdocs/luci-static/aurora/* $(1)/www/luci-static/aurora/ 2>/dev/null || true
	$(INSTALL_DIR) $(1)/usr/lib/lua/luci/view/themes/aurora
	$(CP) $(PKG_BUILD_DIR)/ucode/template/themes/aurora/* $(1)/usr/lib/lua/luci/view/themes/aurora/ 2>/dev/null || true
endef

$(eval $(call BuildPackage,luci-theme-aurora))
