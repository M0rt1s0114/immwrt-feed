include $(TOPDIR)/rules.mk

PKG_NAME:=luci-theme-argon
PKG_VERSION:=2.4.3
PKG_RELEASE:=1

PKG_SOURCE_PROTO:=git
PKG_SOURCE_URL:=https://github.com/jerrykuku/luci-theme-argon.git
PKG_SOURCE_VERSION:=v$(PKG_VERSION)
PKG_MIRROR_HASH:=skip

include $(INCLUDE_DIR)/package.mk

define Package/luci-theme-argon
  SECTION:=luci
  CATEGORY:=LuCI
  SUBMENU:=4. Themes
  TITLE:=Argon Theme
  DEPENDS:=+luci
  PKGARCH:=all
endef

define Package/luci-theme-argon/install
	$(INSTALL_DIR) $(1)/etc/uci-defaults
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/root/etc/uci-defaults/* $(1)/etc/uci-defaults/ 2>/dev/null || true
	$(INSTALL_DIR) $(1)/www/luci-static/argon
	$(CP) $(PKG_BUILD_DIR)/htdocs/luci-static/argon/* $(1)/www/luci-static/argon/ 2>/dev/null || true
	$(INSTALL_DIR) $(1)/usr/lib/lua/luci/view/themes/argon
	$(CP) $(PKG_BUILD_DIR)/ucode/template/themes/argon/* $(1)/usr/lib/lua/luci/view/themes/argon/ 2>/dev/null || true
endef

$(eval $(call BuildPackage,luci-theme-argon))
