[app]

# (str) Title of your application
title = Professor Valera English

# (str) Package name
package.name = profvaleraen

# (str) Package domain (needed for android packaging)
package.domain = org.valera

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,json,mp3

# (list) List of patterns to allow matching for source include
source.include_patterns = Mp3/*,Texts/*,vocabulary.json

# (str) Application versioning
version = 1.1

# (list) Application requirements
# ffpyplayer потрібен для відтворення mp3 на Android
requirements = python3,kivy==2.2.1,pillow,ffpyplayer

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# (list) Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup
android.allow_backup = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1