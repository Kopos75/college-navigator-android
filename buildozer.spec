[app]
title = College Navigator
package.name = collegenavigator
package.domain = org.test
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,ttf,xml

version = 0.1

# Твой проект на Kivy + KivyMD
requirements = python3,kivy,kivymd

orientation = portrait
fullscreen = 1

# Точка входа — твой main.py
entrypoint = main.py

# Можно позже включить иконку:
# icon.filename = %(source.dir)s/images/logo.png
# presplash.filename = %(source.dir)s/images/logo.png

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
android.api = 31
android.minapi = 21
android.sdk = 35
android.ndk = 25c
android.archs = arm64-v8a
android.build_tools_version = 35.0.0
